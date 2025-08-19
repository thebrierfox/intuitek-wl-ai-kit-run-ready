# Internal Modules Overview

This document describes each internal module in the IntuiTek WL AI Kit.

## self_refine

- **Category:** reasoning  
- **Description:** Iteratively improves an answer by critiquing and refining the previous response. Useful for enhancing content quality.

## majority_vote

- **Category:** verification  
- **Description:** Given multiple candidate answers, selects the one supported by the majority. Inspired by ensemble methods to improve reliability.

## chain_of_verification_micro

- **Category:** verification  
- **Description:** Performs a quick chain‑of‑verification to identify obvious errors or inconsistencies. Designed for fast checks with minimal overhead.

## resource_impact_estimator

- **Category:** estimation  
- **Description:** Estimates computational and environmental impact of running modules (runtime, memory usage, approximate CO₂ equivalent). Provides transparency about resource usage.
