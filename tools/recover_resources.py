#!/usr/bin/env python3
"""Recover only hash-verified resources from a user's local GRF or uncompressed TAR.

No download, executable, encryption bypass, or game assets are included.
"""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import json
import struct
import tarfile
import zlib

class Grf:
    def __init__(self, path):
        self.path = Path(path)
        self.base = 0
        if self.path.suffix.lower() == '.tar':
            with tarfile.open(self.path, 'r:') as archive:
                entries = [entry for entry in archive if entry.isfile() and entry.name.lower().endswith('data.grf')]
                if not entries:
                    raise ValueError('No data.grf member found in the uncompressed TAR')
                self.base = entries[0].offset_data
        with self.path.open('rb') as stream:
            stream.seek(self.base)
            header = stream.read(46)
            if len(header) != 46 or not header.startswith((b'Master of Magic', b'Event Horizon')):
                raise ValueError('Unsupported GRF header')
            self.version = struct.unpack_from('<I', header, 42)[0]
            if self.version not in (0x200, 0x300):
                raise ValueError('Only GRF 2.0 and 3.0 are supported')
            offset = struct.unpack_from('<Q' if self.version >= 0x300 else '<I', header, 30)[0]
            stream.seek(self.base + 46 + offset)
            if self.version >= 0x300:
                marker, packed, size = struct.unpack('<III', stream.read(12))
                if marker != 148:
                    raise ValueError('Unsupported GRF 3.0 index')
            else:
                packed, size = struct.unpack('<II', stream.read(8))
            raw = zlib.decompress(stream.read(packed))
            if len(raw) != size:
                raise ValueError('Invalid GRF index length')
        self.entries = {}
        cursor = 0
        fmt = '<IIIBQ' if self.version >= 0x300 else '<IIIBI'
        width = struct.calcsize(fmt)
        while cursor < len(raw):
            end = raw.index(b'\0', cursor)
            name = raw[cursor:end].decode('latin1').replace('\\', '/')
            values = struct.unpack_from(fmt, raw, end + 1)
            cursor = end + 1 + width
            self.entries[name.lower()] = values

    def read(self, name):
        values = self.entries.get(name.replace('\\', '/').lower())
        if values is None:
            return None
        packed, aligned, size, flags, offset = values
        if flags & (6 | 128):
            raise ValueError('Encrypted resources are not supported by this extraction tool')
        with self.path.open('rb') as stream:
            stream.seek(self.base + 46 + offset)
            data = zlib.decompress(stream.read(packed))
        if len(data) != size:
            raise ValueError('Invalid resource length')
        return data

def recover(grf, recipe, destination, verify_only=False):
    destination = Path(destination).resolve()
    recovered, unresolved = [], []
    for row in recipe['files']:
        relative = PurePosixPath(row['path'].replace('\\', '/'))
        if relative.is_absolute() or '..' in relative.parts:
            raise ValueError('Unsafe output path in manifest')
        source = row.get('source')
        if not source:
            unresolved.append({'path': row['path'], 'reason': row['status']})
            continue
        try:
            data = grf.read(source)
            if data is None or hashlib.sha256(data).hexdigest() != row['sha256']:
                unresolved.append({'path': row['path'], 'reason': 'Missing resource or reference hash mismatch'})
                continue
        except ValueError as error:
            unresolved.append({'path': row['path'], 'reason': str(error)})
            continue
        if not verify_only:
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            temporary = target.with_name(target.name + '.recovery.tmp')
            temporary.write_bytes(data)
            temporary.replace(target)
        recovered.append(row['path'])
    return {'name': recipe['name'], 'verified': len(recovered), 'unresolved': unresolved, 'written': not verify_only}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True, help='Your local GRF or uncompressed installer TAR')
    parser.add_argument('--output', type=Path, required=True, help='New local output directory for recovery mods')
    parser.add_argument('--manifest', type=Path, required=True, help='One English recovery recipe from manifests/')
    parser.add_argument('--verify-only', action='store_true')
    args = parser.parse_args()
    recipe = json.loads(args.manifest.read_text())
    result = recover(Grf(args.source), recipe, args.output / recipe['name'], args.verify_only)
    if not args.verify_only:
        target = args.output / recipe['name']
        target.mkdir(parents=True, exist_ok=True)
        (target / 'mod.json').write_text(json.dumps({'name': recipe['name'], 'version': '1.0.0', 'author': 'Local resource recovery', 'description': recipe['description'], 'default': 'off', 'requires': recipe.get('requires', {})}, indent=2) + '\n')
        (target / 'RECOVERY.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
    return 2 if result['unresolved'] else 0

if __name__ == '__main__':
    raise SystemExit(main())
