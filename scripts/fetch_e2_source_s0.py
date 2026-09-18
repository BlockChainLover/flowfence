#!/usr/bin/env python3
"""Fetch public pinned S0 inputs only; never decrypt BrowseComp or execute source code."""
import argparse
import io
import json
from pathlib import Path
import subprocess
import urllib.request
import zipfile


def download(url, target, etag=None):
    request = urllib.request.Request(url, headers={'If-Match': etag} if etag else {})
    with urllib.request.urlopen(request, timeout=90) as response:
        target.write_bytes(response.read())


class RangeArchive(io.RawIOBase):
    """Read an existing public ZIP with ordinary HTTP ranges, without a full download."""
    def __init__(self, url):
        self.url, self.position = url, 0
        with urllib.request.urlopen(urllib.request.Request(url, method='HEAD'), timeout=45) as response:
            self.size = int(response.headers['Content-Length'])
            self.etag = response.headers.get('ETag')
        self.cache = {}

    def seekable(self):
        return True

    def seek(self, offset, whence=0):
        self.position = offset if whence == 0 else self.position + offset if whence == 1 else self.size + offset
        return self.position

    def tell(self):
        return self.position

    def read(self, size=-1):
        if size < 0:
            size = self.size - self.position
        if size == 0:
            return b''
        key = self.position, size
        if key not in self.cache:
            headers = {'Range': f'bytes={self.position}-{self.position + size - 1}'}
            if self.etag:
                headers['If-Match'] = self.etag
            with urllib.request.urlopen(urllib.request.Request(self.url, headers=headers), timeout=90) as response:
                if response.status != 206:
                    raise RuntimeError('Server did not honor bounded ZIP range request')
                self.cache[key] = response.read()
        value = self.cache[key]
        self.position += len(value)
        return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', type=Path, required=True)
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[1]
    provenance = json.loads((repo/'artifacts/aamas2027_e2_source_s0/source_provenance.json').read_text())
    root = args.source_root
    root.mkdir(parents=True, exist_ok=True)
    data = root/'data'
    data.mkdir(exist_ok=True)
    for name, source in provenance['repositories'].items():
        dest = root/name
        if not dest.exists():
            subprocess.run(['git', 'init', str(dest)], check=True, capture_output=True)
            subprocess.run(['git', '-C', str(dest), 'remote', 'add', 'origin', source['url']], check=True)
            subprocess.run(['git', '-C', str(dest), 'fetch', '--depth', '1', 'origin', source['commit']], check=True)
            subprocess.run(['git', '-C', str(dest), 'checkout', '--detach', 'FETCH_HEAD'], check=True)
        actual = subprocess.check_output(['git', '-C', str(dest), 'rev-parse', 'HEAD'], text=True).strip()
        if actual != source['commit']:
            raise RuntimeError(f'{name}: existing checkout differs; use a fresh source directory')
    for name, source in provenance['datasets'].items():
        for filename in source['files']:
            wanted = filename.startswith(('livesqlbench', 'bird_interact_data')) or filename in {
                'data/mini_dev_pg-00000-of-00001.json',
                'data/mini_dev_sqlite-00000-of-00001.json',
                'data/test-00000-of-00001.parquet',
                'distractor/validation-00000-of-00001.parquet'}
            if not wanted or not filename.endswith(('.json', '.jsonl', '.parquet')):
                continue
            local = 'hotpot_distractor_validation.parquet' if name == 'hotpotqa/hotpot_qa' else name.replace('/', '__')+'__'+filename.replace('/', '__')
            url = f'https://huggingface.co/datasets/{name}/resolve/{source["revision"]}/{filename}'
            download(url, data/local)
    download(provenance['browsecomp_blob']['url'], data/'browsecomp_encrypted.csv', provenance['browsecomp_blob']['ETag'])
    archive = RangeArchive(provenance['legacy_sqlite_fixture_package']['url'])
    with zipfile.ZipFile(archive) as z:
        members = [x for x in z.infolist() if x.filename.endswith('/superhero.sqlite')]
        if len(members) != 1:
            raise RuntimeError('Expected one official superhero DB archive member')
        (data/'superhero.sqlite').write_bytes(z.read(members[0]))
    print('Fetched public S0 inputs. No decryption, solver, evaluator, or model executed.')


if __name__ == '__main__':
    main()
