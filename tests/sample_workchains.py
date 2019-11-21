# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Defines simple workchains which are used in the tests.
"""

import numpy as np
import scipy.linalg as la
from aiida.engine import WorkChain, workfunction
from aiida.orm import Float, List
from aiida_tools import check_workchain_step


class Echo(WorkChain):
    """
    WorkChain which returns the input.
    """
    @classmethod
    def define(cls, spec):
        super(Echo, cls).define(spec)

        spec.input('x', valid_type=Float)
        spec.output('result', valid_type=Float)
        spec.outline(cls.echo)

    @check_workchain_step
    def echo(self):
        self.report('Starting echo')
        self.out('result', self.inputs.x)


class EchoDifferentNames(WorkChain):
    """
    WorkChain which returns the input, with "non-standard" input / output names.
    """
    @classmethod
    def define(cls, spec):
        super(EchoDifferentNames, cls).define(spec)

        spec.input('y', valid_type=Float)
        spec.output('the_result', valid_type=Float)
        spec.outline(cls.echo)

    @check_workchain_step
    def echo(self):
        self.report('Starting echo')
        self.out('the_result', self.inputs.y)


class Negative(WorkChain):
    """
    WorkChain which returns the negative of the input.
    """
    @classmethod
    def define(cls, spec):
        super(Negative, cls).define(spec)

        spec.input('x', valid_type=Float)
        spec.output('result', valid_type=Float)
        spec.outline(cls.run_negative)

    @check_workchain_step
    def run_negative(self):
        self.report('Starting negative, input {}'.format(self.inputs.x.value))
        self.out('result', Float(-self.inputs.x.value).store())


class Norm(WorkChain):
    """
    WorkChain which returns the norm of the input list.
    """
    @classmethod
    def define(cls, spec):
        super(Norm, cls).define(spec)

        spec.input('x', valid_type=List)
        spec.output('result', valid_type=Float)
        spec.outline(cls.evaluate)

    @check_workchain_step
    def evaluate(self):  # pylint: disable=missing-docstring
        self.report('Starting evaluate')
        res = Float(la.norm(self.inputs.x.get_attribute('list')))
        res.store()
        self.out('result', res)


@workfunction
def sin_list(x):
    return Float(np.sin(list(x)[0])).store()


@workfunction
def rosenbrock(x):
    x, y = x
    return Float((1 - x)**2 + 100 * (y - x**2)**2).store()


@workfunction
def add(x, y):
    return Float(x + y).store()
