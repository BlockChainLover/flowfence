#!/usr/bin/env python3
"""Acquire the accepted public BIRD DB package and hash/extract its PostgreSQL source."""
import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import shutil
import urllib.parse
import urllib.request
import zipfile


def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
    return h.hexdigest()


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--private-root',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();a.private_root.mkdir(parents=True,exist_ok=True)
    url='https://drive.google.com/uc?export=download&id=13VLWIwpw5E3d5DUkMvzw7hvHE67a4XkG'
    archive=a.private_root/'minidev_current.zip'
    if not archive.exists():
        class Form(HTMLParser):
            def __init__(self):super().__init__();self.fields={};self.action=None
            def handle_starttag(self,t,attrs):
                d=dict(attrs)
                if t=='form':self.action=d['action']
                if t=='input' and d.get('type')=='hidden':self.fields[d['name']]=d['value']
        with urllib.request.urlopen(url,timeout=60) as r:body=r.read().decode()
        form=Form();form.feed(body)
        if form.action!='https://drive.usercontent.google.com/download':raise RuntimeError('Unexpected public download form')
        request=form.action+'?'+urllib.parse.urlencode(form.fields)
        tmp=archive.with_suffix('.partial');total=0
        with urllib.request.urlopen(request,timeout=90) as r,tmp.open('wb') as f:
            while True:
                b=r.read(4*1024*1024)
                if not b:break
                f.write(b);total+=len(b)
                if total%(64*1024*1024)==0:print('Downloaded MiB',total//(1024*1024),flush=True)
        if total!=799944582:raise RuntimeError('Archive size differs from accepted S0 source; retain partial and investigate provenance')
        tmp.rename(archive)
    if digest(archive) != "aeb211c0e39010bbdae3838bb5e8bd27dc446ed77495b1709f85ccc9bf67f2be":
        raise RuntimeError("Archive differs from S1 captured source; human provenance review required")
    previous = json.loads(a.output.read_text()) if a.output.exists() else None
    entries=[]
    with zipfile.ZipFile(archive) as z:
        for info in z.infolist():
            name=info.filename
            if name.startswith('__MACOSX/'):continue
            wanted=name=='minidev/MINIDEV_postgresql/BIRD_dev.sql' or '/database_description/' in name and name.endswith('.csv')
            if not wanted:continue
            relative=Path(name)
            if '..' in relative.parts or relative.is_absolute():raise RuntimeError('Unsafe archive member')
            dest=a.private_root/relative;dest.parent.mkdir(parents=True,exist_ok=True)
            if not dest.exists():
                with z.open(info) as src,dest.open('wb') as out:shutil.copyfileobj(src,out,8*1024*1024)
            entries.append({'member':name,'size':dest.stat().st_size,'sha256':digest(dest)})
    if previous and previous['extracted_files'] != entries:
        raise RuntimeError('Extracted files differ from recorded S1 source; refusing to overwrite provenance')
    result={'source_url':'https://drive.google.com/file/d/13VLWIwpw5E3d5DUkMvzw7hvHE67a4XkG/view','archive_size':archive.stat().st_size,'archive_sha256':digest(archive),'extracted_files':entries,'raw_files_location':str(a.private_root),'models_called':0}
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,indent=2)+'\n')
    print('Archive and PostgreSQL dump retained and hashed; extracted files',len(entries),flush=True)


if __name__=='__main__':main()
