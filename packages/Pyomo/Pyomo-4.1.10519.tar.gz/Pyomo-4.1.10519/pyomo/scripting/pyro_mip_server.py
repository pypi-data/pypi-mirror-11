#! /usr/bin/env python
#
# pyro_mip_server: A script that sets up a Pyro server for solving MIPs in
#           a distributed manner.
#
#  _________________________________________________________________________
#
#  Pyomo: Python Optimization Modeling Objects
#  Copyright (c) 2014 Sandia Corporation.
#  Under the terms of Contract DE-AC04-94AL85000 with Sandia Corporation,
#  the U.S. Government retains certain rights in this software.
#  This software is distributed under the BSD License.
#  _________________________________________________________________________

import os
import os.path
import sys
import traceback
import datetime
import base64
try:
    import cPickle as pickle
except:
    import pickle
import six
import pyutilib.services
import pyutilib.pyro
from pyomo.util import pyomo_command


class PyomoMIPWorker(pyutilib.pyro.TaskWorker):

    def process(self, data):
        import pyomo.opt

        data = pyutilib.misc.Bunch(**data)

        with pyutilib.services.TempfileManager.push():
            #
            # Construct the solver on this end, based on the input type stored in "data.opt".
            # This is slightly more complicated for asl-based solvers, whose real executable
            # name is stored in data.solver_options["solver"].
            #
            with pyomo.opt.SolverFactory(data.opt) as opt:

                if opt is None:
                    raise ValueError("Problem constructing solver `"+data.opt+"'")

                # here is where we should set any options required by the solver, available
                # as specific attributes of the input data object.
                solver_options = data.solver_options
                del data.solver_options
                for key,value in solver_options.items():
                    setattr(opt.options,key,value)

                problem_filename_suffix = os.path.split(data.filename)[1]
                temp_problem_filename = \
                    pyutilib.services.TempfileManager.create_tempfile(suffix="."+problem_filename_suffix)
                with open(temp_problem_filename, 'w') as f:
                    f.write(data.file)

                if data.warmstart_filename is not None:
                    warmstart_filename_suffix = os.path.split(data.warmstart_filename)[1]
                    temp_warmstart_filename = \
                        pyutilib.services.TempfileManager.create_tempfile(suffix="."+warmstart_filename_suffix)
                    with open(temp_warmstart_filename, 'w') as f:
                        f.write(data.warmstart_file)
                    assert opt.warm_start_capable()
                    assert (('warmstart' in data.kwds) and \
                            data.kwds['warmstart'])
                    data.kwds['warmstart_file'] = temp_warmstart_filename

                now = datetime.datetime.now()
                print(str(now) + ": Applying solver="+data.opt+" to solve problem="+temp_problem_filename)
                sys.stdout.flush()
                results = opt.solve(temp_problem_filename,
                                    suffixes=data.suffixes,
                                    **data.kwds)
                assert results._smap_id is None
                # NOTE: This results object contains solutions, because no model is provided
                # (just a model file).  Also, the results._smap_id value is None.

        now = datetime.datetime.now()
        print(str(now) + ": Solve completed - number of solutions="+str(len(results.solution)))
        sys.stdout.flush()
        # PYTHON3 / PYRO4 Fix
        # The default serializer in Pyro4 is not pickle and does not
        # support user defined types (e.g., the results object).
        # Therefore, we pickle the results object before sending it
        # over the wire so the user does not need to change the Pyro
        # serializer.  Protocal MUST be set to 1 to avoid errors
        # unpickling (I don't know why)
        pickled_results = pickle.dumps(results, protocol=1)

        if six.PY3:
            #
            # The standard bytes object returned by pickle.dumps must be
            # converted to base64 to avoid errors sending over the
            # wire with Pyro4. Also, the base64 bytes must be wrapped
            # in a str object to avoid a different set of Pyro4 errors.
            #
            return str(
                base64.encodebytes(
                    pickled_results))
        else:
            return pickled_results

@pyomo_command('pyro_mip_server', "Launch a Pyro server for Pyomo MIP solvers")
def main():
    #
    # Handle error when pyro is not installed
    #
    if pyutilib.pyro.Pyro is None:
        raise ImportError("Pyro or Pyro4 is not available")

    #
    # Import plugins
    #
    import pyomo.environ
    #
    exception_trapped = False
    try:
        pyutilib.pyro.TaskWorkerServer(PyomoMIPWorker, argv=sys.argv)
    except IOError:
        msg = sys.exc_info()[1]
        print("IO ERROR:")
        print(msg)
        exception_trapped = True
    except pyutilib.common.ApplicationError:
        msg = sys.exc_info()[1]
        print("APPLICATION ERROR:")
        print(str(msg))
        exception_trapped = True
    except RuntimeError:
        msg = sys.exc_info()[1]
        print("RUN-TIME ERROR:")
        print(str(msg))
        exception_trapped = True
    #
    # pyutilib.pyro tends to throw SystemExit exceptions if things
    # cannot be found or hooked up in the appropriate fashion. The
    # name is a bit odd, but we have other issues to worry about. we
    # are dumping the trace in case this does happen, so we can figure
    # out precisely who is at fault.
    #
    except SystemExit:
        msg = sys.exc_info()[1]
        print("Solver server encountered system error")
        print("Error: "+str(msg))
        print("Stack trace:")
        traceback.print_exc()
        exception_trapped = True
    except:
        print("Encountered unhandled exception")
        traceback.print_exc()
        exception_trapped = True
    #
    # If an exception occurred, then we probably want to shut down all
    # Pyro components.  Otherwise, the client may have forever while
    # waiting for results that will never arrive. There are better
    # ways to handle this at the client level, but until those are
    # implemented, this will suffice for cleanup.  NOTE: this should
    # perhaps be command-line driven, so it can be disabled if
    # desired.
    #
    if exception_trapped == True:
        print("Pyro solver server aborted")
