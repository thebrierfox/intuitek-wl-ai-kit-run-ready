# Master Meta Directive for Runnable AI Upgrade Repositories

This directive codifies the structural patterns, file conventions, and instruction style that enabled the successful “live run” of the reference upgrade repository. By following these guidelines, future repositories will be both understandable to an orchestrator and executable within a Python environment.

## A. Execution‑Truth

* Never claim execution without artefacts from the session (files, logs, outputs).
* Timestamp actions; record raw commands and outputs in an `upgrade_log.md` or dedicated demo log.
* If a tool is missing or a step fails, log the block and continue with fallbacks.

## B. Environment

* Use Python 3.9+ with minimal dependencies. Specify dependencies in `requirements.txt` and `pyproject.toml`.
* Ensure the repository root is on `PYTHONPATH` when running the CLI or modules (for example: `PYTHONPATH=. python3 cli/aegis_cli.py plan --config config/defaults.yaml --profile chat_safe`).
* Every importable directory (`internal`, `internal/code`, `orchestrator`, `cli`) must contain an `__init__.py` to make it a package.

## C. Repository Structure

The following top‑level directories and files are required to make the repository runnable:

- **internal/** – prompt‑driven modules.
  - **internal/modules/** – markdown documentation for each module describing category, reason, theoretical basis, prompt trigger, expected behaviour and trace label.
  - **internal/code/** – Python implementations for internal modules.  Each file defines a `run_module(payload: dict) -> dict` function.  Include an `__init__.py`.
  - **internal/manifest.yaml** – manifest listing all internal modules with metadata and an `entry_point` pointing to the fully qualified module path (e.g., `internal.code.self_refine:run_module`).
- **external/** – subfolders for any external modules and a manifest.
- **orchestrator/** – orchestration engine.  Contains `engine.py` that loads manifests, conflict policies and configuration, resolves conflicts and produces a plan. Includes `__init__.py`.
- **cli/** – command‑line interface.  Contains `aegis_cli.py` implementing `plan` and `run` commands using `argparse` and the orchestrator; includes `__init__.py`.
- **config/** – YAML configuration files such as `defaults.yaml` (profiles listing which modules to enable) and `policies.yaml` (exclusive and soft conflict rules).
- **docs/** – human‑readable documentation.  Should include this master directive, module descriptions, conflict explanations and prompt templates.
- **templates/** – ready‑to‑use prompt templates for complex protocols such as P‑C‑A, self‑refine and chain‑of‑verification.
- **tests/** – a test suite (e.g., pytest) verifying that manifests are valid, conflicts resolve and module functions run without error.
- **requirements.txt** and **pyproject.toml** – dependency management and package metadata.
- **CHANGELOG.md**, **upgrade_log.md** – versioning and operational logs.

## D. Manifest and Module Contract

Each internal module must be registered in `internal/manifest.yaml` with fields:

```yaml
- id: self_refine
  category: reasoning
  reason: "Iteratively improve an answer by critiquing and refining"
  entry_point: internal.code.self_refine:run_module
  prompt_trigger: "SELF_REFINE"
  trace_label: "SelfRefine"
```

The `entry_point` must point to a callable that conforms to a uniform interface:

```python
def run_module(payload: dict) -> dict:
    """Execute the module logic and return a result.

    Args:
        payload: A dictionary containing at least a `prompt` or other module‑specific fields.
    Returns:
        A dictionary with keys:
        - ok (bool): whether the module succeeded.
        - result: the module's output.
        - trace (list of str): trace messages for logging.
        - meta (dict): any additional metadata.
    """
    # implementation here
```

Avoid external dependencies unless absolutely necessary; document installation steps in `docs/EXTERNAL.md`.

## E. Policies and Profiles

Conflict policies are defined in `config/policies.yaml` as exclusive groups and soft conflicts. Soft conflicts specify a set of modules and the resolution strategy, e.g., `refine_then_vote` when both `self_refine` and `majority_vote` are requested.

Default profiles live in `config/defaults.yaml`. A profile lists modules to enable for a given use case. Example:

```yaml
profiles:
  chat_safe:
    modules:
      - self_refine
      - chain_of_verification_micro
  chat_rigorous:
    modules:
      - self_refine
      - majority_vote
      - chain_of_verification_micro
      - resource_impact_estimator
```

## F. Orchestrator and CLI

The orchestrator loads manifests, policies and profiles, resolves conflicts and produces a plan. It should provide functions to:

1. **load_manifests** – read YAML manifests for internal and external modules.
2. **load_policies** – parse conflict rules.
3. **load_defaults** – read default profiles.
4. **resolve_plan(profile_name)** – given a profile, return a plan with enabled and disabled modules.
5. **run_entry_point(module_id, payload)** – import and run a module's entry point.

The CLI exposes `plan` and `run` commands. The `plan` command prints the resolved plan; the `run` command executes a given module id by delegating to the orchestrator's `run_entry_point`.

## G. Testing and Continuous Integration

A `tests/` directory should contain unit tests ensuring that manifests are valid YAML, that required fields exist, that the orchestrator resolves conflicts correctly and that each `run_module()` function executes without errors. Configure GitHub Actions (or another CI pipeline) to run tests on every push.

## H. Documentation and Templates

- **README.md** should include a quick‑start: how to install dependencies, run the CLI and activate modules. Provide example commands and mention environment variables.
- **docs/INTERNAL.md** summarises internal modules and their purposes.
- **docs/CONFLICTS.md** documents exclusive/soft conflicts and resolution strategies.
- **docs/TEMPLATES.md** lists prompt templates available in `templates/` and explains how to use them.
- **docs/MASTER_META_DIRECTIVE.md** (this file) records the high‑level design and procedural guidance.

## I. Demo Runbook

To verify that the repository is runnable, perform a demonstration and log it:

1. Generate a plan: `PYTHONPATH=. python3 cli/aegis_cli.py plan --config config/defaults.yaml --profile chat_safe` and save the output to `demo_orchestrator_demo_log.md`.
2. Exercise core modules: import and run `self_refine`, `majority_vote`, `chain_of_verification_micro`, and `resource_impact_estimator` using the orchestrator's `run_entry_point()` and record their outputs in the demo log.
3. Append a timestamped summary of the demo to `upgrade_log.md`.
4. If using a remote repository, commit the updated logs to version control.

## J. Instruction Style for Future Prompts

When instructing an AI agent to build or extend a repository:

1. **Be explicit about structure** – specify folder names and file locations (e.g., `Create internal/code/self_refine.py with a run_module() function`).
2. **Mention manifests and entry points** – instruct the agent to add modules to `internal/manifest.yaml` with the correct `entry_point` field.
3. **Call out `__init__.py`** – remind the agent to add `__init__.py` files in any package directories so imports work.
4. **Define policies and profiles** – instruct to provide or update YAML files that govern conflicts and module selection.
5. **Include execution commands** – show how to run the CLI with `PYTHONPATH=.` and suggest running individual modules for testing.
6. **Emphasise logs** – direct the agent to log each significant action or demonstration in `upgrade_log.md` or a dedicated demo log.

By adhering to this directive, you capture both the architecture and procedural know‑how required to make the repository runnable. This ensures repeatable success when designing and deploying future upgrade menus or orchestrator repositories.
