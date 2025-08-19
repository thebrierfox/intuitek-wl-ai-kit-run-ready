# Majority Vote Module

**Category:** Verification

**Reason for use:** Combines multiple independently generated answers and selects the answer that appears most frequently, improving reliability.

**Theoretical basis:** Ensemble methods and majority voting reduce error by aggregating independent judgments.

**Prompt trigger:** Include “majority vote” in the instructions or plan to activate this module.

**Expected behaviour:** Accepts a list of answers and returns the choice with the highest vote count; falls back to the first answer if tied.

**Trace label:** majority_vote
