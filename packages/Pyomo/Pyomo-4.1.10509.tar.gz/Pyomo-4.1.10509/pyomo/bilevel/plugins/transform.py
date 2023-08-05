#  _________________________________________________________________________
#
#  Pyomo: Python Optimization Modeling Objects
#  Copyright (c) 2014 Sandia Corporation.
#  Under the terms of Contract DE-AC04-94AL85000 with Sandia Corporation,
#  the U.S. Government retains certain rights in this software.
#  This software is distributed under the BSD License.
#  _________________________________________________________________________

from pyomo.core.base import Transformation, Var, ComponentUID
from pyomo.bilevel import SubModel
import logging
logger = logging.getLogger('pyomo.core')


class Base_BilevelTransformation(Transformation):

    def __init__(self):
        super(Base_BilevelTransformation, self).__init__()

    def _preprocess(self, tname, instance, **kwds):
        options = kwds.pop('options', {})
        sub = options.get('submodel',None)
        #
        # Iterate over the model collecting variable data,
        # until the submodel is found.
        #
        var = {}
        submodel = None
        for (name, data) in instance.component_map(active=True).items():
            if isinstance(data,Var):
                var[name] = data
            elif isinstance(data,SubModel):
                if sub is None or sub == name:
                    sub = name
                    submodel = data
                    break
        if submodel is None:
            raise RuntimeError("Missing submodel: "+str(sub))
        #
        instance._transformation_data[tname].submodel = [name]
        #
        # Fix variables
        #
        if submodel._fixed:
            fixed = [i.name for i in submodel._fixed]
            unfixed = []
            for v in var:
                if not v in fixed:
                    unfixed.append((v,getattr(submodel._parent(),v).is_indexed()))
        elif submodel._var:
            _var = set(submodel._var)
            unfixed = [(v,getattr(submodel._parent(),v).is_indexed()) for v in _var]
            fixed = []
            for v in var:
                if not v in _var:
                    fixed.append(v)
        else:
            raise RuntimeError("Must specify either 'fixed' or 'var' option for SubModel")
        #
        self._submodel           = sub
        self._upper_vars         = var
        self._fixed_upper_vars   = fixed
        self._unfixed_upper_vars = unfixed
        instance._transformation_data[tname].fixed = [ComponentUID(var[v]) for v in fixed]
        return submodel

    def _fix_all(self):
        """
        Fix the upper variables
        """
        self._fixed_cache = {}
        for v in self._fixed_upper_vars:
            self._fixed_cache[v] = self._fix(self._upper_vars[v])

    def _unfix_all(self):
        """
        Unfix the upper variables
        """
        for v in self._fixed_upper_vars:
            self._unfix(self._upper_vars[v], self._fixed_cache[v])

    def _fix(self, var):
        """
        Fix the upper level variables, tracking the variables that were
        modified.
        """
        cache = []
        for i,vardata in var.items():
            if not vardata.fixed:
                vardata.fix()
                cache.append(i)
        return cache

    def _unfix(self, var, cache):
        """
        Unfix the upper level variables.
        """
        for i in cache:
            var[i].unfix()

