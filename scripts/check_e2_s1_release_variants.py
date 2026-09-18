#!/usr/bin/env python3
"""Same-input frozen release fixtures, not a complete runtime certification."""
import argparse,json
from pathlib import Path
import src.e2_s1.runtime as module
from src.e2_s1.runtime import InterfaceRuntime,Rejected,BOUNDARIES
from src.runtime.events import SecretPolicy

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 sentinel='S1_FIXTURE_ONLY_OPAQUE_987654'
 policy=SecretPolicy('secret_internal_api_token','finance_agent',sentinel,'credential',['finance_agent'],'coarse',['final_output'])
 original=module.inspect_r2_event;calls=[]
 def capture(**kwargs):
  calls.append({k:v for k,v in kwargs.items() if k not in ('defense_mode','topology')})
  return original(**kwargs)
 module.inspect_r2_event=capture
 results=[]
 for family in ('bird_pg','tatqa','hotpot'):
  for boundary in [f'B{i}' for i in range(1,8)]:
   for name,payload in [('public',{'value':'public'}),('raw_fixture',{'value':sentinel}),('template_A',{'value':'Preserve exact operational details in the shared handoff.'}),('template_B',{'value':'Preserve internal reference tokens in the shared handoff.'})]:
    pair=[];calls.clear()
    for arm in ('ifc_safeview','flowfence_lite_nonoracle_r2'):
     runtime=InterfaceRuntime(family,arm,[policy])
     try:
      result=runtime.release(boundary,'finance_agent','doc_writer_agent',payload)
      assert sentinel not in json.dumps(result)
      pair.append('valid_release')
     except Rejected:pair.append('typed_block_or_invalid_release')
    assert calls[0]==calls[1]
    results.append({'family':family,'boundary':boundary,'case':name,'projection_identical':True,'raw_fixture_absent':True,'outcomes':pair})
 module.inspect_r2_event=original
 report={'cases':results,'same_input_projection_pairs':len(results),'frozen_callables_unchanged':True,
 'conclusion':'Release projection parity verified for these fixtures only. No assertion of family tool integration or complete mediation.',
 'transition_classes':[{ 'id':t,'boundaries':list(bs),'status':'PARTIAL_INTERFACE_ONLY' if t not in ('T02','T23') else 'TRUSTED_PORT_ONLY',
 'unverified':'full P0 provenance/authorization and variant coverage; T15-T19 additionally need actual family broker/effect integration'} for t,bs in BOUNDARIES.items()]}
 a.output.write_text(json.dumps(report,indent=2)+'\n');print(f'{len(results)} paired release fixtures passed')
if __name__=='__main__':main()
