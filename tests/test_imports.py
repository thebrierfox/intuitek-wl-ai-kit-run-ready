import pytest


def test_import_modules():
    from internal.code import self_refine, majority_vote, chain_of_verification_micro, resource_impact_estimator
    # Ensure that run_module functions exist and are callable
    assert callable(self_refine.run_module)
    assert callable(majority_vote.run_module)
    assert callable(chain_of_verification_micro.run_module)
    assert callable(resource_impact_estimator.run_module)
