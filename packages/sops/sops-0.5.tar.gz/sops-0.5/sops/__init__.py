#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Contributor: Julien Vehent <jvehent@mozilla.com> [:ulfr]
# Contributor: Daniel Thornton <daniel@relud.com>
# Contributor: Alexis Metaireau <alexis@mozilla.com> [:alexis]
# Contributor: Rémy Hubscher <natim@mozilla.com> [:natim]

from __future__ import print_function, unicode_literals
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from base64 import b64encode, b64decode
from textwrap import dedent

import boto3
import ruamel.yaml
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, modes, algorithms


DESC = """
`sops` is an encryption manager and editor for files that contains secrets.

`sops` supports both AWS, KMS and PGP encryption:

    * To encrypt or decrypt a document with AWS KMS, specify the KMS ARN
      in the `-k` flag or in the ``SOPS_KMS_ARN`` environment variable.
      (you need valid credentials in ~/.aws/credentials)

    * To encrypt or decrypt using PGP, specify the PGP fingerprint in the
      `-g` flag or in the ``SOPS_PGP_FP`` environment variable.

Those flags are ignored if the document already stores encryption info.
Internally the KMS and PGP key IDs are stored in the document under
``sops.kms`` and ``sops.pgp``.

    YAML
        sops:
            kms:
            -   arn: "aws:kms:us-east-1:656532927350:key/305caadb"
            -   arn: "aws:kms:us-west-2:457153232612:key/f7da420e"
            pgp:
            -   fp: 85D77543B3D624B63CEA9E6DBC17301B491B3F21

    JSON
        {"sops": {
            "kms": [
                {"arn": "aws:kms:us-east-1:650:key/305caadb"},
                {"arn": "aws:kms:us-west-2:457153232612:key/f7da420e" }
            ],
            "pgp": [
                {"fp": 85D77543B3D624B63CEA9E6DBC17301B491B3F21}
            ]}
        }

    TEXT (JSON serialization of the `sops` object)
        SOPS={"sops":{"kms":[{"arn":"aws:kms:us-east-1:650:ke...}]}}

The ``SOPS_KMS_ARN`` and ``SOPS_PGP_FP`` environment variables can
take multiple keys separated by commas. All spaces are trimmed.

By default, editing is done in vim. Set the env variable ``$EDITOR``
to use a different editor.

Mozilla Services - ulfr, relud - 2015
"""

# A list of KMS ARNs either provided on the command line or retrieved
# from the user environment
SOPS_KMS_ARN = ""

# A list of PGP fingeprints either provided on the command line or
# retrieved from the user environment
SOPS_PGP_FP = ""

DEFAULT_YAML = """# Welcome to SOPS. This is the default template.
# Remove these lines and add your data.
# Don't modify the `sops` section, it contains key material.
example_key: example_value
example_array:
    - example_value1
    - example_value2
example_multiline: |
    this is a
    multiline
    entry
"""


def main():
    argparser = argparse.ArgumentParser(
        usage='sops <file>',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='Encrypted secrets editor',
        epilog=dedent(DESC))
    argparser.add_argument('file',
                           help="file to edit; create it if it doesn't exist")
    argparser.add_argument('-k', '--kms', dest='kmsarn',
                           help="ARN of KMS key used for encryption")
    argparser.add_argument('-g', '--pgp', dest='pgpfp',
                           help="fingerprint of PGP key for decryption")
    argparser.add_argument('-d', '--decrypt', action='store_true',
                           dest='decrypt',
                           help="decrypt <file> and print it to stdout")
    argparser.add_argument('-e', '--encrypt', action='store_true',
                           dest='encrypt',
                           help="encrypt <file> and print it to stdout")
    argparser.add_argument('-i', '--in-place', action='store_true',
                           dest='in_place',
                           help="write output back to <file> instead "
                                "of stdout for encrypt/decrypt")
    argparser.add_argument('-r', '--rotate', action='store_true',
                           dest='rotate',
                           help="generate a new data encryption key and "
                                "encrypt all values with the new key")
    argparser.add_argument('--input-type', dest='input_type',
                           help="input type (yaml, json, ...), "
                                "if undef, use file extension")
    argparser.add_argument('--output-type', dest='output_type',
                           help="output type (yaml, json, ...), "
                                "if undef, use input type")
    args = argparser.parse_args()

    global SOPS_KMS_ARN
    if args.kmsarn:
        SOPS_KMS_ARN = args.kmsarn
    elif 'SOPS_KMS_ARN' in os.environ:
        SOPS_KMS_ARN = os.environ['SOPS_KMS_ARN']

    global SOPS_PGP_FP
    if args.pgpfp:
        SOPS_PGP_FP = args.pgpfp
    elif 'SOPS_PGP_FP' in os.environ:
        SOPS_PGP_FP = os.environ['SOPS_PGP_FP']

    # use input type as output type if not specified
    if args.input_type:
        itype = args.input_type
    else:
        itype = detect_filetype(args.file)

    if args.output_type:
        otype = args.output_type
    else:
        otype = itype

    need_key = False
    is_new_file = False
    try:
        os.stat(args.file)
        # read the encrypted file from disk
        tree = load_tree(args.file, itype)
        tree, need_key = verify_or_create_sops_branch(tree)
    except:
        if args.encrypt or args.decrypt:
            panic("cannot operate on non-existent file", error_code=100)
        print("%s doesn't exist, creating it." % args.file)
        is_new_file = True
        if itype is "yaml":
            tree = ruamel.yaml.load(DEFAULT_YAML, ruamel.yaml.RoundTripLoader)
        else:
            tree = dict()
            tree['data'] = 'Welcome to SOPS. ' + \
                'Remove this line and add your data to the file.'
        tree, need_key = verify_or_create_sops_branch(tree)

    if args.rotate:
        need_key = True

    if args.encrypt:
        # Encrypt mode: encrypt, display and exit
        key, tree = get_key(tree, need_key)

        tree = walk_and_encrypt(tree, key)

    elif args.decrypt:
        # Decrypt mode: decrypt, display and exit
        key, tree = get_key(tree)
        tree = walk_and_decrypt(tree, key)

    else:
        # EDIT Mode: decrypt, edit, encrypt and save
        key, tree = get_key(tree, need_key)

        # we need a stash to save the IV and AAD and reuse them
        # if a given value has not changed during editing
        stash = {'sops': {'has_stash': True}}
        if not is_new_file:
            tree = walk_and_decrypt(tree, key, stash=stash)

        # the decrypted tree is written to a tempfile and an editor
        # is opened on the file
        tmppath = write_file(tree, filetype=otype)
        tmpstamp = os.stat(tmppath)
        run_editor(tmppath)

        # verify if file has been modified, and if not, just exit
        tmpstamp2 = os.stat(tmppath)
        if tmpstamp == tmpstamp2:
            os.remove(tmppath)
            panic("%s has not been modified, exit without writing" % args.file,
                  error_code=200)

        # encrypt the tree
        tree = load_tree(tmppath, otype)
        os.remove(tmppath)
        tree = walk_and_encrypt(tree, key, stash)

    # if we're in -e or -d mode, and not in -i mode, display to stdout
    if (args.encrypt or args.decrypt) and not args.in_place:
        write_file(tree, path='/dev/stdout', filetype=otype)

    # otherwise, write the tree to a file
    else:
        path = write_file(tree, path=args.file, filetype=otype)
        print("file written to %s" % (path), file=sys.stderr)


def detect_filetype(file):
    """Detect the type of file based on its extension.
    Return a string that describes the format: `text`, `yaml`, `json`
    """
    base, ext = os.path.splitext(file)
    if (ext == '.yaml') or (ext == '.yml'):
        return 'yaml'
    elif ext == '.json':
        return 'json'
    return 'text'


def load_tree(path, filetype):
    """Load the tree.

    Read data from `path` using format defined by `filetype`.
    Return a dictionary with the data.

    """
    tree = dict()
    with open(path, "rt") as fd:
        if filetype == 'yaml':
            tree = ruamel.yaml.load(fd, ruamel.yaml.RoundTripLoader)
        elif filetype == 'json':
            tree = json.load(fd)
        else:
            for line in fd:
                if line.startswith('SOPS='):
                    tree['sops'] = json.loads(
                        line.rstrip('\n').split('=', 1)[1])
                else:
                    if 'data' not in tree:
                        tree['data'] = str()
                    tree['data'] += line
    return tree


def verify_or_create_sops_branch(tree):
    """Verify or create the sops branch in the tree.

    If the current tree doesn't have a sops branch with either kms or pgp
    information, create it using the content of the global variables and
    indicate that an encryption is needed when returning.

    """
    if 'sops' not in tree:
        tree['sops'] = dict()
        tree['sops']['attention'] = 'This section contains key material' + \
            ' that should only be modified with extra care. See `sops -h`.'
    if 'kms' in tree['sops'] and isinstance(tree['sops']['kms'], list):
        # check that we have at least one ARN to work with
        for entry in tree['sops']['kms']:
            if 'arn' in entry and entry['arn'] != "":
                return tree, False
    # if we're here, no arn was found
    if 'pgp' in tree['sops'] and isinstance(tree['sops']['pgp'], list):
        # check that we have at least one fingerprint to work with
        for entry in tree['sops']['pgp']:
            if 'fp' in entry and entry['fp'] != "":
                return tree, False
    # if we're here, no fingerprint was found either
    has_at_least_one_method = False
    if SOPS_KMS_ARN != "":
        tree['sops']['kms'] = list()
        for arn in SOPS_KMS_ARN.split(','):
            entry = {"arn": arn.replace(" ", "")}
            tree['sops']['kms'].append(entry)
            has_at_least_one_method = True
    if SOPS_PGP_FP != "":
        tree['sops']['pgp'] = list()
        for fp in SOPS_PGP_FP.split(','):
            entry = {"fp": fp.replace(" ", "")}
            tree['sops']['pgp'].append(entry)
            has_at_least_one_method = True
    if not has_at_least_one_method:
        panic("Error: No KMS ARN or PGP Fingerprint found to encrypt the data "
              "key, read the help (-h) for more information.", 111)
    # return True to indicate an encryption key needs to be created
    return tree, True


def walk_and_decrypt(branch, key, stash=None):
    """Walk the branch recursively and decrypt leaves."""
    for k, v in branch.items():
        if k == 'sops':
            continue    # everything under the `sops` key stays in clear
        nstash = dict()
        if stash:
            stash[k] = {'has_stash': True}
            nstash = stash[k]
        if isinstance(v, dict):
            branch[k] = walk_and_decrypt(v, key, nstash)
        elif isinstance(v, list):
            branch[k] = walk_list_and_decrypt(v, key, nstash)
        elif isinstance(v, ruamel.yaml.scalarstring.PreservedScalarString):
            ev = decrypt(v, key, nstash)
            branch[k] = ruamel.yaml.scalarstring.PreservedScalarString(ev)
        else:
            branch[k] = decrypt(v, key, nstash)
    return branch


def walk_list_and_decrypt(branch, key, stash=None):
    """Walk a list contained in a branch and decrypts its values."""
    nstash = dict()
    kl = []
    for i, v in enumerate(list(branch)):
        if stash and i in stash:
            nstash = stash[i]
        if isinstance(v, dict):
            kl.append(walk_and_decrypt(v, key, nstash))
        elif isinstance(v, list):
            kl.append(walk_list_and_decrypt(v, key, nstash))
        else:
            kl.append(decrypt(v, key, nstash))
    return kl


def decrypt(value, key, stash=None):
    """Return a decrypted value."""
    # operate on bytes, but return a string
    value = value.encode('utf-8')
    # extract fields using a regex
    res = re.match(b'^ENC\[AES256_GCM,data:(.+),iv:(.+),aad:(.+),tag:(.+)\]$',
                   value)
    # if the value isn't in encrypted form, return it as is
    if res is None:
        return value
    enc_value = b64decode(res.group(1))
    iv = b64decode(res.group(2))
    aad = b64decode(res.group(3))
    tag = b64decode(res.group(4))
    decryptor = Cipher(algorithms.AES(key),
                       modes.GCM(iv, tag),
                       default_backend()
                       ).decryptor()
    decryptor.authenticate_additional_data(aad)
    cleartext = decryptor.update(enc_value) + decryptor.finalize()
    if stash:
        # save the values for later if we need to reencrypt
        stash['iv'] = iv
        stash['aad'] = aad
        stash['cleartext'] = cleartext
    return cleartext.decode('utf-8')


def walk_and_encrypt(branch, key, stash=None):
    """Walk the branch recursively and encrypts its leaves."""
    for k, v in branch.items():
        if k == 'sops':
            continue    # everything under the `sops` key stays in clear
        nstash = dict()
        if stash and k in stash:
            nstash = stash[k]
        if isinstance(v, dict):
            # recursively walk the tree
            branch[k] = walk_and_encrypt(v, key, nstash)
        elif isinstance(v, list):
            branch[k] = walk_list_and_encrypt(v, key, nstash)
        elif isinstance(v, ruamel.yaml.scalarstring.PreservedScalarString):
            ev = encrypt(v, key, nstash)
            branch[k] = ruamel.yaml.scalarstring.PreservedScalarString(ev)
        else:
            branch[k] = encrypt(v, key, nstash)
    return branch


def walk_list_and_encrypt(branch, key, stash=None):
    """Walk a list contained in a branch and encrypts its values."""
    nstash = dict()
    kl = []
    for i, v in enumerate(list(branch)):
        if stash and i in stash:
            nstash = stash[i]
        if isinstance(v, dict):
            kl.append(walk_and_encrypt(v, key, nstash))
        elif isinstance(v, list):
            kl.append(walk_list_and_encrypt(v, key, nstash))
        else:
            kl.append(encrypt(v, key, nstash))
    return kl


def encrypt(value, key, stash=None):
    """Return an encrypted string of the value provided."""
    value = value.encode('utf-8')
    # if we have a stash, and the value of cleartext has not changed,
    # attempt to take the IV and AAD value from the stash.
    # if the stash has no existing value, or the cleartext has changed,
    # generate new IV and AAD.
    if stash and stash['cleartext'] == value:
        iv = stash['iv']
        aad = stash['aad']
    else:
        iv = os.urandom(32)
        aad = os.urandom(32)
    encryptor = Cipher(algorithms.AES(key),
                       modes.GCM(iv),
                       default_backend()).encryptor()
    encryptor.authenticate_additional_data(aad)
    enc_value = encryptor.update(value) + encryptor.finalize()
    return "ENC[AES256_GCM,data:{value},iv:{iv},aad:{aad}," \
           "tag:{tag}]".format(value=b64encode(enc_value).decode('utf-8'),
                               iv=b64encode(iv).decode('utf-8'),
                               aad=b64encode(aad).decode('utf-8'),
                               tag=b64encode(encryptor.tag).decode('utf-8'))


def get_key(tree, need_key=False):
    """Obtain a 256 bits symetric key.

    If the document contain an encrypted key, try to decrypt it using
    KMS or PGP. Otherwise, generate a new random key.

    """
    if need_key:
        # if we're here, the tree doesn't have a key yet. generate
        # one and store it in the tree
        print("please wait while a data encryption key is being generated"
              " and stored securely", file=sys.stderr)
        key = os.urandom(32)
        tree = encrypt_key_with_kms(key, tree)
        tree = encrypt_key_with_pgp(key, tree)
        return key, tree
    key = get_key_from_kms(tree)
    if not (key is None):
        return key, tree
    key = get_key_from_pgp(tree)
    if not (key is None):
        return key, tree
    panic("[error] couldn't retrieve a key to encrypt/decrypt the tree",
          error_code=128)


def get_key_from_kms(tree):
    """Get the key form the KMS tree leave."""
    try:
        kms_tree = tree['sops']['kms']
    except KeyError:
        return None
    i = -1
    for entry in kms_tree:
        i += 1
        try:
            enc = entry['enc']
        except KeyError:
            continue
        if 'arn' not in entry or entry['arn'] == "":
            print("KMS ARN not found, skipping entry %s" % i, file=sys.stderr)
            continue
        # extract the region from the ARN
        # arn:aws:kms:{REGION}:...
        res = re.match(r'^arn:aws:kms:(.+):([0-9]+):key/(.+)$',
                       entry['arn'])
        if res is None:
            print("Invalid ARN '%s' in entry %s" % (entry['arn'], i),
                  file=sys.stderr)
            continue
        try:
            region = res.group(1)
        except:
            print("Unable to find region from ARN '%s' in entry %s" %
                  (entry['arn'], i), file=sys.stderr)
            continue
        kms = boto3.client('kms', region_name=region)
        # use existing data key, ask kms to decrypt it
        try:
            kms_response = kms.decrypt(CiphertextBlob=b64decode(enc))
        except Exception as e:
            print("failed to decrypt key using kms: %s, skipping it" % e,
                  file=sys.stderr)
            continue
        return kms_response['Plaintext']
    return None


def encrypt_key_with_kms(key, tree):
    """Encrypt the key using the KMS."""
    try:
        isinstance(tree['sops']['kms'], list)
    except KeyError:
        return tree
    i = -1
    for entry in tree['sops']['kms']:
        i += 1
        if 'arn' not in entry or entry['arn'] == "":
            print("KMS ARN not found, skipping entry %d" % i, file=sys.stderr)
            continue
        arn = entry['arn']
        # extract the region from the ARN
        # arn:aws:kms:{REGION}:...
        res = re.match(r'^arn:aws:kms:(.+):([0-9]+):key/(.+)$',
                       arn)
        if res is None:
            print("Invalid ARN '%s' in entry %s" % (entry['arn'], i),
                  file=sys.stderr)
            continue
        try:
            region = res.group(1)
        except:
            print("Unable to find region from ARN '%s' in entry %s" %
                  (entry['arn'], i), file=sys.stderr)
            continue
        kms = boto3.client('kms', region_name=region)
        try:
            kms_response = kms.encrypt(KeyId=arn, Plaintext=key)
        except Exception as e:
            print("failed to encrypt key using kms arn %s: %s, skipping it" %
                  (arn, e), file=sys.stderr)
            continue
        entry['enc'] = b64encode(
            kms_response['CiphertextBlob']).decode('utf-8')
        entry['created_at'] = time.time()
        tree['sops']['kms'][i] = entry
    return tree


def get_key_from_pgp(tree):
    """Retreive the key from the PGP tree leave."""
    try:
        pgp_tree = tree['sops']['pgp']
    except KeyError:
        return None
    i = -1
    for entry in pgp_tree:
        i += 1
        try:
            enc = entry['enc']
        except KeyError:
            continue
        try:
            p = subprocess.Popen(['gpg', '-d'], stdout=subprocess.PIPE,
                                 stdin=subprocess.PIPE)
            key = p.communicate(input=enc)[0]
        except Exception as e:
            print("PGP decryption failed in entry %s with error: %s" %
                  (i, e), file=sys.stderr)
            continue
        return key
    return None


def encrypt_key_with_pgp(key, tree):
    """Encrypt the key using the PGP key."""
    try:
        isinstance(tree['sops']['pgp'], list)
    except KeyError:
        return tree
    i = -1
    for entry in tree['sops']['pgp']:
        i += 1
        if 'fp' not in entry or entry['fp'] == "":
            print("PGP fingerprint not found, skipping entry %d" % i,
                  file=sys.stderr)
            continue
        fp = entry['fp']
        try:
            p = subprocess.Popen(['gpg', '--no-default-recipient', '--yes',
                                  '--encrypt', '-a', '-r', fp, '--trusted-key',
                                  fp[-16:], '--no-encrypt-to'],
                                 stdout=subprocess.PIPE,
                                 stdin=subprocess.PIPE)
            enc = p.communicate(input=key)[0]
        except Exception as e:
            print("failed to encrypt key using pgp fp %s: %s, skipping it" %
                  (fp, e), file=sys.stderr)
            continue
        enc = enc.decode('utf-8')
        entry['enc'] = ruamel.yaml.scalarstring.PreservedScalarString(enc)
        entry['created_at'] = time.time()
        tree['sops']['pgp'][i] = entry
    return tree


def write_file(tree, path=None, filetype=None):
    """Write the tree content in a file using filetype format.

    Write the content of `tree` encoded using the format defined by
    `filetype` at the location `path`.
    If `path` is not defined, a tempfile is created.
    if `filetype` is not defined, tree is treated as a blob of data.

    Return the path of the file written.

    """
    if path:
        fd = open(path, "wb")
    else:
        fd = tempfile.NamedTemporaryFile(suffix="."+filetype, delete=False)
        path = fd.name
    if filetype == "yaml":
        fd.write(ruamel.yaml.dump(tree, Dumper=ruamel.yaml.RoundTripDumper,
                                  indent=4).encode('utf-8'))
    elif filetype == "json":
        fd.write(json.dumps(tree, sort_keys=True, indent=4).encode('utf-8'))
    else:
        if 'data' in tree:
            # add a newline if there's none
            if tree['data'][-1:] != '\n':
                tree['data'] += '\n'
            fd.write(tree['data'].encode('utf-8'))
        if 'sops' in tree:
            jsonstr = json.dumps(tree['sops'], sort_keys=True)
            fd.write(("SOPS=%s" % jsonstr).encode('utf-8'))
    fd.close()
    return path


def run_editor(path):
    """Open the text editor on the given file path."""
    editor = None
    if 'EDITOR' in os.environ:
        editor = os.environ['EDITOR']
    else:
        process = subprocess.Popen(["which", "vim", "nano"],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        for line in process.stdout:
            editor = line.strip()
            break

    if editor:
        subprocess.call([editor, path])
    else:
        panic("Please define your EDITOR environment variable.", 201)
    return


def panic(msg, error_code=1):
    print(msg, file=sys.stderr)
    sys.exit(error_code)


if __name__ == '__main__':
    main()
