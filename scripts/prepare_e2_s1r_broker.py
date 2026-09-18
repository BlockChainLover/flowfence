#!/usr/bin/env python3
"""Inspect original source schema and provision narrowly granted temporary query roles."""
import argparse,csv,json,sys
from pathlib import Path

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--dependency-path',type=Path,required=True);p.add_argument('--private-root',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();sys.path.insert(0,str(a.dependency_path))
 import psycopg2
 from psycopg2 import sql
 metadata={}
 with psycopg2.connect(dbname='bird',user='postgres',host='127.0.0.1') as conn:
  with conn.cursor() as cur:
   # No table/data mutation. Original evaluator still connects as its source superuser.
   cur.execute('REVOKE CREATE ON SCHEMA public FROM PUBLIC')
   cur.execute('REVOKE TEMPORARY ON DATABASE bird FROM PUBLIC')
   cur.execute("SELECT table_name,column_name,data_type,udt_name,is_nullable,column_default,ordinal_position FROM information_schema.columns WHERE table_schema='public' ORDER BY table_name,ordinal_position")
   cols={}
   for t,*values in cur.fetchall():cols.setdefault(t,[]).append(dict(zip(['name','data_type','udt_name','nullable','default','ordinal'],values)))
   cur.execute("SELECT c.relname,k.conname,k.contype,pg_get_constraintdef(k.oid) FROM pg_constraint k JOIN pg_class c ON c.oid=k.conrelid JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='public' ORDER BY c.relname,k.conname")
   constraints={}
   for t,name,kind,definition in cur.fetchall():constraints.setdefault(t,[]).append({'name':name,'type':kind,'definition':definition})
   for db in sorted((a.private_root/'minidev/MINIDEV/dev_databases').iterdir()):
    files=sorted((db/'database_description').glob('*.csv'))
    if not files:continue
    role='e2_read_'+db.name
    cur.execute('SELECT 1 FROM pg_roles WHERE rolname=%s',(role,))
    if not cur.fetchone():cur.execute(sql.SQL('CREATE ROLE {} LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT').format(sql.Identifier(role)))
    cur.execute(sql.SQL('GRANT CONNECT ON DATABASE bird TO {}').format(sql.Identifier(role)))
    cur.execute(sql.SQL('GRANT USAGE ON SCHEMA public TO {}').format(sql.Identifier(role)))
    tables={}
    for path in files:
     name=path.stem.lower();assert name in cols,name
     raw=path.read_bytes();codec='utf-8-sig' if raw.startswith(b'\xef\xbb\xbf') else 'utf-8'
     try:text=raw.decode(codec)
     except UnicodeDecodeError:codec='cp1252';text=raw.decode(codec)
     assert text.encode(codec)==raw
     tables[name]={'columns':cols[name],'constraints':constraints.get(name,[]),'description_csv':text,'description_encoding':codec}
     cur.execute(sql.SQL('GRANT SELECT ON TABLE public.{} TO {}').format(sql.Identifier(name),sql.Identifier(role)))
    metadata[db.name]={'db_id':db.name,'role':role,'tables':tables}
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(metadata,indent=2)+'\n');print(json.dumps({'db_profiles':len(metadata),'tables':sum(len(x['tables']) for x in metadata.values())}))
if __name__=='__main__':main()
