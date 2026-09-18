"""Architecture tests only: no provider import or generated study outcome."""
import unittest
from src.experiments.aamas_gate_ac import DynamicWorkflow, ReleaseAdapter
from src.runtime.events import SecretPolicy
from src.defenses.mas_flowfence_r2 import R2_MODE


TRAJECTORIES=[
    [dict(op='delegate',next_actor='specialist_a',message='public task'),
     dict(op='tool',tool='lookup',arguments='public query'),
     dict(op='finish',value='fixture complete')],
    [dict(op='delegate',next_actor='specialist_b',message='public task'),
     dict(op='write',key='note',value='public result',next_actor='tool_executor'),
     dict(op='tool',tool='verify',arguments='public item',next_actor='synthesizer'),
     dict(op='finish')],
    [dict(op='delegate',next_actor='specialist_a',message='public task'),
     dict(op='delegate',next_actor='manager',message='clarify'),
     dict(op='delegate',next_actor='specialist_b',message='revised request'),
     dict(op='tool',tool='lookup',arguments='public query',next_actor='specialist_a'),
     dict(op='delegate',next_actor='synthesizer',message='public summary'),
     dict(op='finish')],
]


def exercise_trajectories():
    results=[]
    for family in ('procurement_travel','research_document','it_incident'):
        for index,actions in enumerate(TRAJECTORIES):
            def planner(state, actions=actions):return actions[state['step']]
            flow=DynamicWorkflow(planner,dict(lookup=lambda _: 'lookup fixture',verify=lambda _: 'verified fixture'))
            result=flow.run(family)
            assert result['status']=='completed'
            results.append(dict(family=family,variant=index,**result))
    return results


class ArchitectureTests(unittest.TestCase):
    def test_nine_dynamic_paths(self):
        results=exercise_trajectories()
        self.assertEqual(len(results),9)
        for family in {r['family'] for r in results}:
            traces=[r['trace'] for r in results if r['family']==family]
            self.assertEqual({len(t) for t in traces},{3,4,6})
            self.assertEqual(len({tuple((e['actor'],e['next_actor']) for e in t) for t in traces}),3)
            self.assertEqual({e['tool'] for t in traces for e in t if e['tool']},{'lookup','verify'})
    def test_invalid_choice_not_silently_rerouted(self):
        flow=DynamicWorkflow(lambda _:dict(op='delegate',next_actor='nonexistent',message='x'),{})
        with self.assertRaises(ValueError):flow.run('fixture')
    def test_cycle_terminates_by_budget(self):
        flow=DynamicWorkflow(lambda _:dict(op='delegate',next_actor='manager',message='x'),{},max_steps=3)
        self.assertEqual(flow.run('fixture')['status'],'budget_exhausted')
    def test_safe_view_keeps_tool_argument_shape(self):
        p=SecretPolicy('fixture','owner','SYNTH-ONLY','P4',['owner'],'none',['external_message'])
        a=ReleaseAdapter('ifc_safeview',[p],['owner','reader'])
        value=a.value({'query':'SYNTH-ONLY'},'owner','tool:lookup','external_message','TOOL_CALL')
        self.assertEqual(set(value),{'query'})
        self.assertNotIn(p.raw_value,value['query'])

    def test_delivered_raw_evaluation(self):
        p=SecretPolicy('fixture','owner','SYNTH-ONLY','P4',['owner'],'none',['shared_doc'])
        for defense in ('ifc_safeview',R2_MODE):
            a=ReleaseAdapter(defense,[p],['owner','reader'])
            self.assertNotIn(p.raw_value,a.release(p.raw_value,'owner','reader','shared_doc'))
            self.assertFalse(a.events[-1]['unauthorized_raw'])
            self.assertEqual(a.release('public','owner','reader','shared_doc'),'public')


if __name__=='__main__':unittest.main()
