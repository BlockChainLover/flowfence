"""Trusted PostgreSQL source capability: SELECT/WITH over source-public tables.

SQL AST authorization complements server SELECT-only grants and read-only transactions.
No model text supplies connection parameters, roles, schemas, or publication callbacks.
"""
import json
import math
from decimal import Decimal
from datetime import date, datetime, time
from copy import deepcopy

# Data-computation functions, not arbitrary PostgreSQL administration/IO functions.
# SQL syntax constructs (CASE, COALESCE, casts, arithmetic) are parsed separately.
DATA_FUNCTIONS=frozenset('age date now abs acos asin atan atan2 avg bit_and bit_or bool_and bool_or btrim ceil ceiling char_length character_length concat concat_ws count date_part date_trunc degrees exp extract floor greatest initcap least left length ln log lower lpad ltrim max md5 min mod nullif octet_length overlay position power radians regexp_match regexp_matches regexp_replace repeat replace reverse right round rpad rtrim sign split_part sqrt stddev stddev_pop stddev_samp string_agg strpos substr substring sum to_char to_date to_number to_timestamp translate trim trunc upper variance var_pop var_samp array_agg array_length array_lower array_upper cardinality unnest generate_series row_number rank dense_rank percent_rank cume_dist ntile lag lead first_value last_value nth_value json_agg jsonb_agg json_build_object jsonb_build_object'.split())

class CapabilityError(Exception):
    def __init__(self, code):self.code=code;super().__init__(code)


def encode(value):
    if isinstance(value,float) and not math.isfinite(value):return {'postgres_type':'float','text':str(value)}
    if isinstance(value,(Decimal,date,datetime,time,bytes,memoryview)):
        return {'postgres_type':type(value).__name__,'text':bytes(value).hex() if isinstance(value,(bytes,memoryview)) else str(value)}
    if isinstance(value,tuple):return [encode(x) for x in value]
    if isinstance(value,list):return [encode(x) for x in value]
    if isinstance(value,dict):return {k:encode(v) for k,v in value.items()}
    return value


def authorize_sql(sql,tables):
    from pglast import parser
    if not isinstance(sql,str):raise CapabilityError('SQL_TYPE')
    try:tree=json.loads(parser.parse_sql_json(sql))
    except Exception:raise CapabilityError('SQL_SYNTAX') from None
    if len(tree['stmts'])!=1 or 'SelectStmt' not in tree['stmts'][0]['stmt']:raise CapabilityError('READ_ONLY_REQUIRED')
    nodes=[]
    def visit(v):
        if isinstance(v,dict):
            nodes.append(v)
            for x in v.values():visit(x)
        elif isinstance(v,list):
            for x in v:visit(x)
    visit(tree)
    ctes={v['CommonTableExpr']['ctename'] for v in nodes if 'CommonTableExpr' in v}
    for v in nodes:
        for k in v:
            if k.endswith('Stmt') and k!='SelectStmt':raise CapabilityError('READ_ONLY_REQUIRED')
        if v.get('intoClause') or v.get('lockingClause'):raise CapabilityError('READ_ONLY_REQUIRED')
        if 'RangeVar' in v:
            rv=v['RangeVar'];name=rv['relname'];schema=rv.get('schemaname')
            if schema not in (None,'public') or (name not in tables and not(schema is None and name in ctes)):
                raise CapabilityError('SOURCE_TABLE_DENIED')
        if 'FuncCall' in v:
            names=[x['String']['sval'] for x in v['FuncCall']['funcname']]
            if len(names)>2 or (len(names)==2 and names[0]!='pg_catalog') or names[-1].lower() not in DATA_FUNCTIONS:
                raise CapabilityError('FUNCTION_CAPABILITY_DENIED')
    return sql


class ReadonlyBroker:
    """Owned by trusted runtime. Return is a private draft until runtime B5 publication."""
    def __init__(self,metadata,*,timeout_ms=30000):
        self.__metadata=deepcopy(metadata);self.__timeout_ms=timeout_ms
    def metadata(self,db_id):return deepcopy(self.__metadata[db_id])
    def execute(self,db_id,arguments):
        import psycopg2
        try:
            if set(arguments)!={'sql'}:raise CapabilityError('ARGUMENT_SCHEMA')
            sql=authorize_sql(arguments['sql'],set(self.__metadata[db_id]['tables']))
            # Fixed trusted DB name/role, never values supplied by an actor.
            role=self.__metadata[db_id]['role']
            with psycopg2.connect(dbname='bird',user=role,host='127.0.0.1',
                    options=f'-c default_transaction_read_only=on -c max_parallel_workers_per_gather=0 -c statement_timeout={self.__timeout_ms}') as conn:
                with conn.cursor() as cur:
                    cur.execute(sql);rows=cur.fetchall();columns=[c.name for c in cur.description]
            return {'ok':True,'columns':columns,'rows':encode(rows),'error':None}
        except CapabilityError as e:return {'ok':False,'columns':[],'rows':[],'error':{'code':e.code,'retry_class':'NEVER'}}
        except psycopg2.Error as e:
            return {'ok':False,'columns':[],'rows':[],'error':{'code':'TIMEOUT' if e.pgcode=='57014' else 'SQL_ERROR','sqlstate':e.pgcode,'retry_class':'SAFE_RETRY'}}
