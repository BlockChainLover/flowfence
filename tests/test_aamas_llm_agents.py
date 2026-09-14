"""No API tests for real intermediate decisions and mediator context delivery."""
import copy
import json
from pathlib import Path
from unittest.mock import patch

import pytest

from src.defenses.mas_flowfence import inspect_mas_event
from src.experiments.aamas_llm_agents import (
    DEFENSES, SYSTEM_PROMPT, DeterministicDryRunClient, LLMAgentEpisode,
    MiniMaxAgentClient, ProviderFailure, expected_decision, load_config,
    parse_action, run_matrix, summarize_episodes, validate_config,
)
from src.runtime.policy import default_secret_policies


@pytest.fixture
def inputs():
    config, tasks, hashes = load_config(Path("configs/experiment/aamas2027/e1_pilot.json"))
    return config, tasks, hashes


def episode(inputs, client=None, defense="ifc_safeview", topology="blackboard_4", condition="attack"):
    config, tasks, _ = inputs
    return LLMAgentEpisode(tasks[0], topology, condition, defense, 1, config, client or DeterministicDryRunClient())


def test_config_matrix_and_gold(inputs):
    config, tasks, _ = inputs
    validate_config(config, tasks)
    formal, _, _ = load_config(Path("configs/experiment/aamas2027/e1_formal.json"))
    assert len(tasks) == len(formal["task_ids"]) == 12
    assert len(formal["task_ids"]) * len(formal["topologies"]) * len(formal["conditions"]) * len(formal["defenses"]) * len(formal["seeds"]) == 144
    assert len({t["scenario_id"] for t in tasks}) == 1
    assert len({expected_decision(t)["vendor_id"][-1] for t in tasks}) >= 2


@pytest.mark.parametrize("edit", [
    {"provider": "other"}, {"attack": "summary_poisoning_indirect"},
    {"defenses": ["static_acl"]}, {"api_attempts_per_call": 2}, {"seeds": [1, 1]},
])
def test_config_validation_rejects_drift(inputs, edit):
    config, tasks, _ = inputs
    with pytest.raises(ValueError):
        validate_config({**config, **edit}, tasks)


@pytest.mark.parametrize("defense", DEFENSES)
@pytest.mark.parametrize("topology", ["chain_4", "blackboard_4"])
def test_three_agents_execute_and_gold_is_checked(inputs, defense, topology):
    run = episode(inputs, defense=defense, topology=topology)
    result = run.run()
    assert result["status"] == "completed"
    assert result["success"]
    assert result["agent_generation_count"] == 3
    assert result["llm_calls"] == 0  # fixture is not counted as paid/model evidence
    assert [c["role"] for c in run.calls] == ["planner_agent", "finance_agent", "doc_writer_agent"]
    assert result["raw_exposure"] > 0 if defense == "none" else result["raw_exposure"] == 0
    assert result["privacy_safe_success"] == (defense != "none")


def test_defense_fairness_and_actual_downstream_context(inputs):
    runs = [episode(inputs, defense=d) for d in DEFENSES]
    for run in runs:
        run.run()
    assert all(c["system"] == SYSTEM_PROMPT for r in runs for c in r.context_history)
    raw_token = default_secret_policies()[-1].raw_value
    assert raw_token in runs[0].context_history[0]["prompt"]
    assert all(raw_token not in c["prompt"] for r in runs[1:] for c in r.context_history)
    assert runs[0]._public_task() == runs[1]._public_task() == runs[2]._public_task()
    assert runs[0].config["generation"] == runs[1].config["generation"] == runs[2].config["generation"]


def test_generated_message_is_mediated_before_next_llm_call(inputs):
    secret = default_secret_policies()[-1].raw_value
    class MessageClient(DeterministicDryRunClient):
        def complete_messages(self, system, prompt):
            response = super().complete_messages(system, prompt)
            if "ROLE: planner_agent" in prompt:
                obj = json.loads(response["text"])
                obj["message"] += " intermediate-marker " + secret
                response["text"] = json.dumps(obj)
            return response
    run = episode(inputs, client=MessageClient())
    assert run.run()["success"]
    finance_prompt = run.context_history[1]["prompt"]
    assert "intermediate-marker" in finance_prompt
    assert secret not in finance_prompt
    assert "internal credential withheld" in finance_prompt


def test_wrong_generated_tool_action_is_not_repaired_from_gold(inputs):
    class WrongQuote(DeterministicDryRunClient):
        def complete_messages(self, system, prompt):
            result = super().complete_messages(system, prompt)
            if "ROLE: finance_agent" in prompt:
                obj = json.loads(result["text"])
                obj["vendor_id"] = "UNLISTED_VENDOR"
                result["text"] = json.dumps(obj)
            return result
    run = episode(inputs, client=WrongQuote())
    result = run.run()
    assert result["status"] == "completed" and not result["success"]
    assert not result["structured_correctness"]["approved_state_correct"]
    assert '"approved_state": null' in run.context_history[2]["prompt"]


def test_planner_hold_changes_deterministic_workflow(inputs):
    class HoldPlanner(DeterministicDryRunClient):
        def complete_messages(self, system, prompt):
            if "ROLE: planner_agent" in prompt:
                return {"text": json.dumps({"action": "hold", "message": "Please hold"}), "usage": {}}
            return super().complete_messages(system, prompt)
    run = episode(inputs, client=HoldPlanner())
    result = run.run()
    assert not result["success"]
    assert "Planner request delivered: False" in run.context_history[1]["prompt"]
    assert run.approved is None


def test_same_interception_coverage(inputs):
    sequences = []
    for defense in DEFENSES:
        run = episode(inputs, defense=defense)
        with patch("src.experiments.aamas_llm_agents.inspect_mas_event", wraps=inspect_mas_event) as guard:
            run.run()
            sequences.append([(c.kwargs["event_type"], c.kwargs["actor_id"], c.kwargs["recipient_id"], c.kwargs["channel"]) for c in guard.call_args_list])
            assert all(c.kwargs["attack_annotation"] is None for c in guard.call_args_list)
    assert sequences[0] == sequences[1] == sequences[2]


def test_model_parser_failures_are_saved_without_payload(inputs):
    class Broken(DeterministicDryRunClient):
        def complete_messages(self, system, prompt):
            return {"text": default_secret_policies()[-1].raw_value, "model_version": "test-version", "usage": {"prompt_tokens": 12, "completion_tokens": 4}}
    records = []
    run = episode(inputs, client=Broken())
    run.sink = lambda kind, row: records.append((kind, copy.deepcopy(row)))
    result = run.run()
    assert result["status"] == "failed" and result["error_type"] == "AGENT_JSON_PARSE_ERROR"
    assert result["input_tokens"] == 12 and result["output_tokens"] == 4
    assert result["model_version"] == "test-version"
    assert [r["status"] for k, r in records if k == "call_attempts"] == ["started", "failed"]
    assert default_secret_policies()[-1].raw_value not in json.dumps(records)


def test_transport_failure_attempt_is_preserved(inputs):
    class Failed(DeterministicDryRunClient):
        def complete_messages(self, system, prompt):
            raise ProviderFailure("HTTP_429")
    run = episode(inputs, client=Failed())
    result = run.run()
    assert result["status"] == "failed" and result["error_type"] == "HTTP_429"
    assert len(run.calls) == 1 and run.calls[0]["status"] == "failed"
    assert result["retries"] == 0


def test_missing_credentials_produce_blocked_episode(inputs):
    class Unavailable(DeterministicDryRunClient):
        def available(self):
            return False
    result = episode(inputs, client=Unavailable()).run()
    assert result["status"] == "blocked" and result["error_type"] == "BLOCKED_BY_API"
    assert result["llm_calls"] == 0


def test_safe_outputs_and_summary_rebuild(inputs, tmp_path):
    config, tasks, hashes = inputs
    first = run_matrix(config, tasks, tmp_path, dry_run=True, config_hashes=hashes)
    assert first["episodes"] == 8 and first["llm_calls"] == 0
    rows = [json.loads(s) for s in (tmp_path / "episodes.jsonl").read_text().splitlines()]
    rebuilt = summarize_episodes(rows)
    assert rebuilt["paired_papc_vs_ifc"] == first["paired_papc_vs_ifc"]
    second = run_matrix(config, tasks, tmp_path, dry_run=True, config_hashes=hashes)
    assert second == first
    for path in tmp_path.glob("*.json*"):
        assert all(s.raw_value not in path.read_text() for s in default_secret_policies())


def test_interrupted_call_is_not_silently_retried(inputs, tmp_path):
    config, tasks, hashes = inputs
    config = {**config, "task_ids": [tasks[0]["task_id"]], "defenses": ["ifc_safeview"]}
    run = episode((config, tasks, hashes))
    row = {"run_id": run.run_id, "call_id": run.run_id + "__call1", "status": "started", "role": "planner_agent", "model_version": None, "input_tokens": 0, "output_tokens": 0, "provider_request": True}
    (tmp_path / "call_attempts.jsonl").write_text(json.dumps(row) + "\n")
    summary = run_matrix(config, tasks, tmp_path, dry_run=True, config_hashes=hashes)
    result = json.loads((tmp_path / "episodes.jsonl").read_text())
    assert summary["failed_episodes"] == 1
    assert result["error_type"] == "SESSION_INTERRUPTED"
    assert len((tmp_path / "call_attempts.jsonl").read_text().splitlines()) == 1


def test_api_response_reports_actual_model_version(monkeypatch):
    monkeypatch.setenv("MINIMAX_API_KEY", "test-only-not-a-real-key")
    class Response:
        def __enter__(self): return self
        def __exit__(self, *args): return False
        def read(self): return json.dumps({"model": "provider-returned-version", "choices": [{"message": {"content": "{}"}, "finish_reason": "stop"}], "usage": {"prompt_tokens": 3}}).encode()
    with patch("urllib.request.urlopen", return_value=Response()) as request:
        result = MiniMaxAgentClient(model="MiniMax-M2.7").complete_messages("common-system", "common-task")
        sent = json.loads(request.call_args.args[0].data)
    assert result["model_version"] == "provider-returned-version"
    assert sent["messages"][0] == {"role": "system", "content": "common-system"}


def test_schema_rejects_wrong_action():
    with pytest.raises(ProviderFailure):
        parse_action('{"action":"send_vendor_update","message":"x"}', "planner_agent")


def test_real_client_matrix_constructor_and_unavailable_records(inputs, tmp_path, monkeypatch):
    config, tasks, hashes = inputs
    monkeypatch.delenv("MINIMAX_API_KEY", raising=False)
    result = run_matrix(config, tasks, tmp_path, config_hashes=hashes)
    assert result["blocked_episodes"] == 8
    assert result["llm_calls"] == 0
    overall = result["paired_papc_vs_ifc"][-1]
    assert overall["raw_exposure"]["unavailable"] == 4
    assert overall["raw_exposure"]["tie"] == 0


def test_existing_provider_settings_constructor():
    client = MiniMaxAgentClient(model="kimi-k2.6", provider_settings={"openai_api_key": "fixture-key", "openai_base_url": "https://example.invalid/v1"})
    assert client.available()
    assert client.model == "kimi-k2.6"
    assert client.settings.base_url == "https://example.invalid/v1"


def test_private_full_traces_separate_from_safe_output(inputs, tmp_path):
    config, tasks, hashes = inputs
    safe, private = tmp_path / "safe", tmp_path / "private"
    run_matrix(config, tasks, safe, dry_run=True, config_hashes=hashes, private_output=private)
    files = list(private.glob("*.jsonl"))
    assert len(files) == 8
    assert all((p.stat().st_mode & 0o777) == 0o600 for p in files)
    stages = [json.loads(line)["stage"] for line in files[0].read_text().splitlines()]
    assert "request" in stages and "response" in stages and "mediated_event" in stages
    assert any(p.raw_value in files[0].read_text() for p in default_secret_policies())
    assert all(p.raw_value not in (safe / "events.jsonl").read_text() for p in default_secret_policies())


def test_blocked_message_not_restored_to_downstream_context(inputs):
    from src.defenses.mas_flowfence import DefenseResult
    def guard(**kwargs):
        result = inspect_mas_event(**kwargs)
        if kwargs["event_type"] == "SEND_MESSAGE" and kwargs["actor_id"] == "planner_agent":
            return DefenseResult("[blocked-test-marker]", {**result.decision, "decision": "block", "defense_fired": True}, result.policy_decision)
        return result
    run = episode(inputs, topology="chain_4")
    with patch("src.experiments.aamas_llm_agents.inspect_mas_event", side_effect=guard):
        result = run.run()
    assert not result["success"]
    assert "Planner request delivered: False" in run.context_history[1]["prompt"]
    assert "[content blocked by runtime]" in run.context_history[1]["prompt"]


def test_source_exposure_not_misattributed_to_llm(inputs):
    row = episode(inputs, defense="none").run()
    assert row["source_raw_exposure"] > 0
    assert row["generated_raw_exposure"] == 0
    assert row["generated_external_exposure"] == 0


def test_private_output_cannot_be_nested_in_safe_bundle(inputs, tmp_path):
    config, tasks, hashes = inputs
    with pytest.raises(ValueError):
        run_matrix(config, tasks, tmp_path, dry_run=True, config_hashes=hashes, private_output=tmp_path / "full")


def test_non_dry_matrix_through_http_adapter(inputs, tmp_path):
    config, tasks, hashes = inputs
    fixture = DeterministicDryRunClient()
    class Response:
        def __init__(self, result): self.result = result
        def __enter__(self): return self
        def __exit__(self, *args): return False
        def read(self): return json.dumps({"model": "provider-returned-MiniMax-version", "choices": [{"message": {"content": self.result["text"]}, "finish_reason": "stop"}], "usage": {"prompt_tokens": 7, "completion_tokens": 11}}).encode()
    def request(req, timeout):
        body = json.loads(req.data)
        result = fixture.complete_messages(body["messages"][0]["content"], body["messages"][1]["content"])
        return Response(result)
    with patch("urllib.request.urlopen", side_effect=request) as http:
        result = run_matrix(config, tasks, tmp_path, config_hashes=hashes,
                            provider_settings={"openai_api_key": "test-only-fixture", "openai_base_url": "https://example.invalid/v1"})
    assert result["episodes"] == 8 and result["llm_calls"] == http.call_count == 24
    assert result["failed_episodes"] == result["blocked_episodes"] == 0
    rows = [json.loads(line) for line in (tmp_path / "episodes.jsonl").read_text().splitlines()]
    assert all(row["success"] and row["input_tokens"] == 21 and row["output_tokens"] == 33 for row in rows)
    assert all(row["model_version"] == "provider-returned-MiniMax-version" for row in rows)


def test_actual_exfiltration_tool_privilege_counted(inputs):
    run = episode(inputs, defense="none")
    run._mediate(default_secret_policies()[-1].raw_value, "TOOL_CALL", "doc_writer_agent", "external_vendor_agent", "vendor_send_tool", origin="agent_generated")
    assert run.audit[-1]["privilege_reach"] == 5
    assert run.audit[-1]["raw_exposure"] == run.audit[-1]["external_exposure"] == 1


def test_parameter_bootstrap_clusters_seeds_without_inflating_tasks(inputs):
    from src.experiments.aamas_paired import paired_parameter_inference
    a = episode(inputs, defense="ifc_safeview").run()
    b = episode(inputs, defense="flowfence_lite_nonoracle").run()
    rows = [a, b, {**a, "seed": 2}, {**b, "seed": 2}]
    result = paired_parameter_inference(rows, draws=100)
    metric = result["comparisons"][-1]["metrics"]["success"]
    assert metric["parameter_instance_clusters"] == 1
    assert metric["cluster_bootstrap_95_ci"] == [0, 0]
    assert result["independent_historical_scenarios"] == 1
    assert metric["exact_two_sided_sign_p"] is None
