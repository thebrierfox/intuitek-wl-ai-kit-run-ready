# Chain of Verification Micro Module

**Category:** Verification

**Reason for use:** Applies a lightweight chain-of-verification technique to catch simple logical or factual errors in generated responses.

**Theoretical basis:** Micro chain-of-verification uses a brief series of follow-up questions to check the consistency of an answer, increasing reliability without significant overhead.

**Prompt trigger:** Include “chain of verification micro” in the plan or request to enable this module.

**Expected behaviour:** Generates a few verifying questions about the original response, uses the answers to assess accuracy, and updates the confidence score or flags issues.

**Trace label:** chain_of_verification_micro
