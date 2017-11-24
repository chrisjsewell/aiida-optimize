"""
Tests for the OptimizationWorkChain.
"""

import numpy as np


def test_parameter_sweep(configure, submit_as_async):  # pylint: disable=unused-argument
    """
    Simple test of the OptimizationWorkChain with the ParameterSweep engine.
    """

    from echo_workchain import Echo
    from aiida_optimize.engines import ParameterSweep
    from aiida.orm import WorkflowFactory
    from aiida.orm.data.parameter import ParameterData
    tolerance = 0.
    result = WorkflowFactory('optimize.optimize').run(
        engine=ParameterSweep,
        engine_kwargs=ParameterData(
            dict=dict(
                result_key='result',
                parameters=[{
                    'x': x
                } for x in np.linspace(-2, 2, 10)]
            )
        ),
        calculation_workchain=Echo
    )
    assert np.isclose(result['calculation_result'].value, -2, atol=tolerance)
    assert np.isclose(result['optimizer_result'].value, -2, atol=tolerance)
