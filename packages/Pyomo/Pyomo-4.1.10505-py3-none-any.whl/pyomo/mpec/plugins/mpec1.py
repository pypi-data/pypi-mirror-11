#  _________________________________________________________________________
#
#  Pyomo: Python Optimization Modeling Objects
#  Copyright (c) 2014 Sandia Corporation.
#  Under the terms of Contract DE-AC04-94AL85000 with Sandia Corporation,
#  the U.S. Government retains certain rights in this software.
#  This software is distributed under the BSD License.
#  _________________________________________________________________________

import logging

from pyomo.util.plugin import alias
from pyomo.core.base import (Transformation,
                             Constraint,
                             Block,
                             Param,
                             SortComponents,
                             ComponentUID)
from pyomo.mpec.complementarity import Complementarity

from six import iterkeys

logger = logging.getLogger('pyomo.core')


#
# This transformation reworks each Complementarity block to 
# add a constraint that ensures the complementarity condition.
# Specifically, 
#
#   x1 >= 0  OR  x2 >= 0
#
# becomes
#
#   x1 >= 0
#   x2 >= 0
#   x1*x2 <= 0
#
class MPEC1_Transformation(Transformation):

    alias('mpec.simple_nonlinear', doc="Nonlinear transformations of complementarity conditions when all variables are non-negative")

    def __init__(self):
        super(MPEC1_Transformation, self).__init__()

    def _apply_to(self, instance, **kwds):
        options = kwds.pop('options', {})
        bound = kwds.pop('mpec_bound', 0.0)
        #
        # Create a mutable parameter that defines the value of the upper bound
        # on the constraints
        #
        bound = options.get('mpec_bound', bound)
        instance.mpec_bound = Param(mutable=True, initialize=bound)
        #
        # Setup transformation data
        #
        tdata = instance._transformation_data['mpec.simple_nonlinear']
        tdata.compl_cuids = []
        #
        # Iterate over the model finding Complementarity components
        #
        for block in instance.block_data_objects(active=True, sort=SortComponents.deterministic):
            for complementarity in block.component_objects(Complementarity, active=True, descend_into=False):
                for index in sorted(iterkeys(complementarity)):
                    _data = complementarity[index]
                    if not _data.active:
                        continue
                    _data.to_standard_form()
                    #
                    _type = getattr(_data.c, "_type", 0)
                    if _type == 1:
                        #
                        # Constraint expression is bounded below, so we can replace 
                        # constraint c with a constraint that ensures that either
                        # constraint c is active or variable v is at its lower bound.
                        #
                        _data.ccon = Constraint(expr=(_data.c.body - _data.c.lower)*_data.v <= instance.mpec_bound)
                        del _data.c._type
                    elif _type == 3:
                        #
                        # Variable v is bounded above and below.  We can define
                        #
                        _data.ccon_l = Constraint(expr=(_data.v - _data.v.bounds[0])*_data.c.body <= instance.mpec_bound)
                        _data.ccon_u = Constraint(expr=(_data.v - _data.v.bounds[1])*_data.c.body <= instance.mpec_bound)
                        del _data.c._type
                    elif _type == 2:        #pragma:nocover
                        raise ValueError("to_standard_form does not generate _type 2 expressions")
                tdata.compl_cuids.append( ComponentUID(complementarity) )
                block.reclassify_component_type(complementarity, Block)
