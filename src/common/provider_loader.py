import os
from pathlib import Path


PROFILE_MAP = {
    "qwen36": {
        "api_key": "DASHSCOPE_API_KEY",
        "base_url": "DASHSCOPE_BASE_URL",
        "model_keys": ("MODEL_QWEN36",),
    },
    "qwen35": {
        "api_key": "DASHSCOPE_API_KEY",
        "base_url": "DASHSCOPE_BASE_URL",
        "model_keys": ("MODEL_QWEN35",),
    },
    "glm5": {
        "api_key": "DASHSCOPE_API_KEY",
        "base_url": "DASHSCOPE_BASE_URL",
        "model_keys": ("MODEL_GLM5.1", "MODEL_GLM5"),
    },
    "kimi25": {
        "api_key": "DASHSCOPE_API_KEY",
        "base_url": "DASHSCOPE_BASE_URL",
        "model_keys": ("MODEL_KIMI2.6", "MODEL_KIMI25"),
    },
    "minimax25": {
        "api_key": "MINIMAX_API_KEY",
        "base_url": "MINIMAX_BASE_URL",
        "model_keys": ("MODEL_MINIMAX25",),
    },
    "minimax27": {
        "api_key": "MINIMAX_API_KEY",
        "base_url": "MINIMAX_BASE_URL",
        "model_keys": ("MODEL_MINIMAX27",),
    },
}


def _parse_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip("'").strip('"')
    return values


def _resolve_model_name(values: dict[str, str], model_keys: tuple[str, ...]) -> tuple[str, str | None]:
    for key in model_keys:
        if values.get(key):
            return values[key], key
    return "", None


def load_provider_profile(env_path: str, profile: str) -> dict[str, str]:
    path = Path(env_path)
    if not path.exists():
        raise FileNotFoundError(f"Provider env file not found: {env_path}")
    if profile not in PROFILE_MAP:
        raise ValueError(f"Unknown provider profile: {profile}")

    values = _parse_env_file(path)
    mapping = PROFILE_MAP[profile]
    model_name, resolved_model_key = _resolve_model_name(values, mapping["model_keys"])

    missing = [
        key
        for key in (mapping["api_key"], mapping["base_url"])
        if not values.get(key)
    ]
    if not model_name:
        missing.append("/".join(mapping["model_keys"]))
    if missing:
        raise ValueError(f"Missing provider settings in {env_path}: {', '.join(missing)}")

    return {
        "profile": profile,
        "openai_api_key": values[mapping["api_key"]],
        "openai_base_url": values[mapping["base_url"]],
        "model_name": model_name,
        "resolved_model_key": resolved_model_key,
    }


def apply_openai_compatible_env(env: dict[str, str], env_path: str, profile: str, judge_profile: str | None = None) -> dict[str, str]:
    model_profile = load_provider_profile(env_path, profile)
    judge = load_provider_profile(env_path, judge_profile or profile)

    updated = dict(env)
    updated["OPENAI_API_KEY"] = model_profile["openai_api_key"]
    updated["OPENAI_BASE_URL"] = model_profile["openai_base_url"]
    updated["OPENAI_MODEL"] = model_profile["model_name"]
    updated["JUDGE_MODEL"] = judge["model_name"]
    updated["FLOWFENCE_PROVIDER_PROFILE"] = model_profile["profile"]
    return updated
