"""Orchestrator engine for runnable AI kit.
Loads module manifests, resolves policies, and produces execution plans.
"""

import yaml
import importlib
from pathlib import Path
from typing import Dict, Any, List


MANIFEST_PATH = Path("internal/manifest.yaml")
POLICIES_PATH = Path("config/policies.yaml")
DEFAULTS_PATH = Path("config/defaults.yaml")


def load_yaml(path: Path) -> Any:
    """Load a YAML file and return the parsed data."""
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_manifest() -> Dict[str, Any]:
    """Load the internal module manifest."""
    return load_yaml(MANIFEST_PATH)


def plan(profile: str = "chat_safe") -> Dict[str, Any]:
    """Construct a simple plan based on the requested profile.

    This stub ignores policies and returns all modules listed in the manifest
    or those specified in config/defaults.yaml for the given profile.
    """
    manifest = load_manifest()
    defaults = load_yaml(DEFAULTS_PATH)
    enabled_modules = defaults.get(profile, manifest.get("modules", []))
    # If modules are dict entries, extract ids
    module_ids: List[str] = []
    for m in enabled_modules:
        if isinstance(m, dict):
            module_ids.append(m.get("id"))
        else:
            module_ids.append(m)
    return {
        "profile": profile,
        "modules": module_ids,
    }


def run_entry_point(entry_point: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """Dynamically import and run a module's entry point."""
    module_path, func_name = entry_point.split(":")
    module = importlib.import_module(module_path)
    func = getattr(module, func_name)
    return func(payload)


if __name__ == "__main__":
    # Example usage: print a plan
    import sys
    profile = sys.argv[1] if len(sys.argv) > 1 else "chat_safe"
    plan_dict = plan(profile)
    print(plan_dict)
