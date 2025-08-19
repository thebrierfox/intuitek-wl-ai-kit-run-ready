# Conflict Policies Overview

This document describes the conflict policies used in the IntuiTek WL AI Kit.

## Exclusive Groups

No modules are currently mutually exclusive. Exclusive groups would list module IDs that cannot be enabled together.

## Soft Conflicts

Some modules may interact in a defined order rather than being disabled. The following soft conflict is configured:

- **self_refine** and **majority_vote**: When both are requested, the orchestrator applies the `refine_then_vote` resolution strategy. The output is first refined and then a majority vote is taken if multiple candidates are present.
