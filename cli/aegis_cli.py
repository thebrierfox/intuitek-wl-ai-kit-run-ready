#!/usr/bin/env python3
"""
Command-line interface for the IntuiTek WL AI Kit.

This CLI provides two commands:
  - plan: generates a plan for a given profile by loading the manifest,
    defaults and policies and resolving conflicts.
  - run: runs an individual module by id by dynamically importing its entry point.
"""
import argparse
from orchestrator import engine


def main() -> None:
    parser = argparse.ArgumentParser(description="IntuiTek WL AI Kit CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Plan command
    plan_parser = subparsers.add_parser("plan", help="Generate a plan for a profile")
    plan_parser.add_argument("--config", default="config/defaults.yaml", help="Path to defaults config YAML")
    plan_parser.add_argument("--profile", default="chat_safe", help="Profile name to use from defaults config")

    # Run command
    run_parser = subparsers.add_parser("run", help="Run a module by id")
    run_parser.add_argument("--module", required=True, help="Module ID to run from manifest")

    args = parser.parse_args()

    if args.command == "plan":
        # Load data
        manifest = engine.load_manifest("internal/manifest.yaml")
        defaults = engine.load_defaults(args.config)
        policies = engine.load_policies("config/policies.yaml")
        requested = defaults.get(args.profile, [])
        # Generate plan
        plan = engine.generate_plan(requested, manifest, policies)
        print("Plan modules (enabled):")
        for mod_id in plan.get("enabled", []):
            print(f"- {mod_id}")
        if plan.get("disabled"):
            print("Disabled modules due to conflicts:")
            for mod_id in plan["disabled"]:
                print(f"- {mod_id}")
    elif args.command == "run":
        manifest = engine.load_manifest("internal/manifest.yaml")
        entry_point = None
        for mod in manifest:
            if mod.get("id") == args.module:
                entry_point = mod.get("entry_point")
                break
        if not entry_point:
            print(f"Module '{args.module}' not found in manifest")
            return
        result = engine.run_entry_point(entry_point, {})
        print(result)


if __name__ == "__main__":
    main()
