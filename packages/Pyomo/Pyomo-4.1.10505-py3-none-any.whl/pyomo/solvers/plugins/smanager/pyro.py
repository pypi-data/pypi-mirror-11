#  _________________________________________________________________________
#
#  Pyomo: Python Optimization Modeling Objects
#  Copyright (c) 2014 Sandia Corporation.
#  Under the terms of Contract DE-AC04-94AL85000 with Sandia Corporation,
#  the U.S. Government retains certain rights in this software.
#  This software is distributed under the BSD License.
#  _________________________________________________________________________


__all__ = []

import base64
import ast
try:
    import cPickle as pickle
except:
    import pickle
import six

import pyutilib.pyro
import pyutilib.misc

import pyomo.util.plugin
from pyomo.opt.parallel.manager import *
from pyomo.opt.parallel.async_solver import *
from pyomo.core.base import Block
from pyomo.core.base.suffix import active_import_suffix_generator

class SolverManager_Pyro(AsynchronousSolverManager):

    pyomo.util.plugin.alias('pyro', doc="Execute solvers remotely using pyro")

    def __init__(self, host=None):

        self.host = host
        AsynchronousActionManager.__init__(self)

    def clear(self):
        """
        Clear manager state
        """
        AsynchronousSolverManager.clear(self)
        self.client = pyutilib.pyro.Client(host=self.host)
        self._ah = {}       # maps task ids to their corresponding action handle.
        self._opt_data = {}  # maps task ids to the corresponding import opt solver flags.
        self._args = {}     # maps task ids to the corresponding queued arguments

    def _perform_queue(self, ah, *args, **kwds):
        """
        Perform the queue operation.  This method returns the ActionHandle,
        and the ActionHandle status indicates whether the queue was successful.
        """

        opt = kwds.pop('opt', None)
        if opt is None:
            raise ActionManagerError("No solver passed to SolverManager_Pyro, "
                                     "method=_perform_queue; use keyword option 'opt'")


        self._verbose = kwds.pop('verbose', False)


        #
        # The following block of code is taken from the OptSolver.solve()
        # method, which we do not directly invoke with this interface
        #

        #
        # If the inputs are models, then validate that they have been
        # constructed! Collect suffix names to try and import from solution.
        #
        for arg in args:
            if isinstance(arg, Block):
                if not arg.is_constructed():
                    raise RuntimeError(
                        "Attempting to solve model=%s with unconstructed "
                        "component(s)" % (arg.name,) )

                model_suffixes = list(name for (name,comp) \
                                      in active_import_suffix_generator(arg))
                if len(model_suffixes) > 0:
                    kwds_suffixes = kwds.setdefault('suffixes',[])
                    for name in model_suffixes:
                        if name not in kwds_suffixes:
                            kwds_suffixes.append(name)

        #
        # Force pyomo.opt to ignore tests for availability, at least locally.
        #
        del_available = bool('available' not in kwds)
        kwds['available'] = True
        opt._presolve(*args, **kwds)
        problem_file_string = None
        with open(opt._problem_files[0], 'r') as f:
            problem_file_string = f.read()

        #
        # Delete this option, to ensure that the remote worker does the check for
        # availability.
        #
        if del_available:
            del kwds['available']

        #
        # We can't pickle the options object itself - so extract a simple
        # dictionary of solver options and re-construct it on the other end.
        #
        solver_options = {}
        for key in opt.options:
            solver_options[key]=opt.options[key]

        #
        # NOTE: let the distributed node deal with the warm-start
        # pick up the warm-start file, if available.
        #
        warm_start_file_string = None
        warm_start_file_name = None
        if hasattr(opt,  "_warm_start_solve"):
            if opt._warm_start_solve  and \
               (opt._warm_start_file_name is not None):
                warm_start_file_name = opt._warm_start_file_name
                with open(warm_start_file_name, 'r') as f:
                    warm_start_file_string = f.read()

        data = pyutilib.misc.Bunch(opt=opt.type, \
                                   file=problem_file_string, \
                                   filename=opt._problem_files[0], \
                                   warmstart_file=warm_start_file_string, \
                                   warmstart_filename=warm_start_file_name, \
                                   kwds=kwds, \
                                   solver_options=solver_options, \
                                   suffixes=opt._suffixes)

        task = pyutilib.pyro.Task(data=data.copy(), id=ah.id)
        self.client.add_task(task, verbose=self._verbose)
        self._ah[task['id']] = ah
        self._opt_data[task['id']] = (opt._smap_id,
                                      opt._load_solutions,
                                      opt._select_index,
                                      opt._default_variable_value)
        self._args[task['id']] = args

        return ah

    def _perform_wait_any(self):
        """
        Perform the wait_any operation.  This method returns an
        ActionHandle with the results of waiting.  If None is returned
        then the ActionManager assumes that it can call this method again.
        Note that an ActionHandle can be returned with a dummy value,
        to indicate an error.
        """

        if self.client.num_results() > 0:
            # this protects us against the case where we get an action
            # handle that we didn't know about or expect.
            while(True):
                task = self.client.get_result()
                if task['id'] in self._ah:

                    ah = self._ah[task['id']]
                    del self._ah[task['id']]

                    (smap_id,
                     load_solutions,
                     select_index,
                     default_variable_value) = self._opt_data[task['id']]
                    del self._opt_data[task['id']]

                    args = self._args[task['id']]
                    del self._args[task['id']]

                    ah.status = ActionStatus.done

                    pickled_results = task['result']
                    if six.PY3:
                        # These two conversions are in place to unwrap
                        # the hacks placed in the pyro_mip_server
                        # before transmitting the results
                        # object. These hacks are put in place to
                        # avoid errors when transmitting the pickled
                        # form of the results object with Pyro4.
                        pickled_results = \
                            base64.decodebytes(
                                ast.literal_eval(pickled_results))
                    results = self.results[ah.id] = pickle.loads(pickled_results)

                    # Tag the results object with the symbol map id.
                    results._smap_id = smap_id

                    if isinstance(args[0], Block):
                        _model = args[0]
                        if load_solutions:
                            _model.solutions.load_from(results[ah.id],
                                                       select=select_index,
                                                       default_variable_value=default_variable_value)
                            results._smap_id = None
                            result.solution.clear()
                        else:
                            results._smap = _model.solutions.symbol_map[smap_id]
                            _model.solutions.delete_symbol_map(smap_id)

                    return ah

if pyutilib.pyro.Pyro is None:
    SolverManagerFactory.deactivate('pyro')
