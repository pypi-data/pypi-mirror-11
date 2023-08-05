#  _________________________________________________________________________
#
#  Pyomo: Python Optimization Modeling Objects
#  Copyright (c) 2015 Sandia Corporation.
#  Under the terms of Contract DE-AC04-94AL85000 with Sandia Corporation,
#  the U.S. Government retains certain rights in this software.
#  This software is distributed under the BSD License.
#  _________________________________________________________________________

import pyomo.util.plugin

from six import iteritems

import random

from pyomo.pysp import phextension

from pyomo.core.base import minimize, maximize

import math

class EcksteinCombettesExtension(pyomo.util.plugin.SingletonPlugin):

    pyomo.util.plugin.implements(phextension.IPHExtension)

    pyomo.util.plugin.alias("ecksteincombettesextension")

    def __init__(self):

        self._check_output = False
        self._JName = "PhiSummary.csv"
        self._subproblems_to_queue = []

    def compute_updates(self, ph, subproblems):

        print("Computing updates given solutions to subproblems=",subproblems)

        ########################################
        ##### compute y values and u values ####
        ##### these are scenario-based        ##
        ########################################

        # NOTE: z is initiaized to be xbar in the code above, but it is *not* xbar. 
        # NOTE: v is essentailly y bar
        # NOTE: lambda is 1/rho xxxxxxxxxxxxx so if you see 1/lamba in a latex file, use rho in the py file
        # ASSUME W is the Eckstein W, not the PH W

        for stage in ph._scenario_tree._stages[:-1]:

            for tree_node in stage._tree_nodes:

                if ph._dual_mode is True:
                    raise RuntimeError("***dual_mode not supported by compute_y in plugin ")
                tree_node_averages = tree_node._averages
                tree_node_zs = tree_node._z

                for scenario in tree_node._scenarios:

                    weight_values = scenario._w[tree_node._name]
                    rho_values = scenario._rho[tree_node._name]
                    var_values = scenario._x[tree_node._name]

                    for variable_id in tree_node._standard_variable_ids:
                        varval = var_values[variable_id]
                        if varval is not None:
                            if scenario._objective_sense == minimize:

                               if scenario._name in subproblems:
                                   # CRITICAL: Y depends on the z and weight values that were used when solving the scenario!
                                   z_for_solve = scenario._xbars_for_solve[tree_node._name][variable_id]
                                   w_for_solve = scenario._ws_for_solve[tree_node._name][variable_id]
                                   scenario._y[variable_id] = rho_values[variable_id] * (z_for_solve - varval) - w_for_solve

                               # check it!
                               #print("THIS %s SHOULD EQUAL THIS %s" % (varval + (1.0/rho_values[variable_id])*scenario._y[variable_id],z_for_solve-(1.0/rho_values[variable_id])*w_for_solve))
                               scenario._u[variable_id] = varval - tree_node_averages[variable_id]
                            else:
                                raise RuntimeError("***maximize not supported by compute_y in plugin ")

        ###########################################
        # compute v values - these are node-based #
        ###########################################

        if self._check_output:

            print("Y VALUES:")
            for scenario in ph._scenario_tree._scenarios:
                print(scenario._y)

            print("U VALUES:")
            for scenario in ph._scenario_tree._scenarios:
                print(scenario._u)

        for stage in ph._scenario_tree._stages[:-1]:
            for tree_node in stage._tree_nodes:
                for variable_id in tree_node._standard_variable_ids:
                    expected_y = 0.0
                    for scenario in tree_node._scenarios:
                        expected_y += ((scenario._y[variable_id] * scenario._probability) / tree_node._probability)
                    tree_node._v[variable_id] = expected_y

        if self._check_output:

            print("V VALUES:")
            for stage in ph._scenario_tree._stages[:-1]:
                for tree_node in stage._tree_nodes:
                    print(tree_node._v)

        ###########################################
        # compute norms and test for convergence  #
        ###########################################

        p_unorm = 0.0
        p_vnorm = 0.0

        for stage in ph._scenario_tree._stages[:-1]:
            for tree_node in stage._tree_nodes:
                for variable_id in tree_node._standard_variable_ids:
                    for scenario in tree_node._scenarios:
                        this_v_val = tree_node._v[variable_id]
                        p_vnorm += tree_node._probability * this_v_val * this_v_val
                        this_u_val = scenario._u[variable_id]
                        p_unorm += scenario._probability * this_u_val * this_u_val
                    
        p_unorm = math.sqrt(p_unorm)
        p_vnorm = math.sqrt(p_vnorm)

        print("U NORM=%s" % p_unorm)
        print("V NORM=%s" % p_vnorm)

        # TODO: make these real and configurable!
        delta = 1e-1
        epsilon = 1e-1

        if p_unorm < delta and p_vnorm < epsilon:
            print("***HEY -WE'RE DONE!!!***")
            foobar

        #####################################################
        # compute phi; if greater than zero, update z and w #
        #####################################################
        with open(self._JName,"a") as f:
             f.write("%10d" % (ph._current_iteration))

        phi = 0.0
        for scenario in tree_node._scenarios:
            for tree_node in scenario._node_list[:-1]:
                tree_node_zs = tree_node._z
                cumulative_sub_phi = 0.0
                for variable_id in tree_node._standard_variable_ids:
                        var_values = scenario._x[tree_node._name]
                        varval = var_values[variable_id]
                        weight_values = scenario._w[tree_node._name]
#                        print "WEIGHT VALUES=",weight_values[variable_id]
#                        print "TREE NODE ZS=",tree_node_zs[variable_id]
#                        print "YS=",scenario._y[variable_id]
#                        print "VAR VALUE=",varval
                        if varval is not None:
#                            print "COMPUTING SUB PHI", "Y=",scenario._y[variable_id],"W=",weight_values[variable_id]
                            sub_phi = scenario._probability * ((tree_node_zs[variable_id] - varval) * (scenario._y[variable_id] + weight_values[variable_id]))
                            cumulative_sub_phi += sub_phi
                            phi += sub_phi
                        else:
                            foobar
                with open(self._JName,"a") as f:
                    f.write(", %10f" % (cumulative_sub_phi))
                print(">>SUB-PHI FOR SCENARIO=%s EQUALS %s" % (scenario._name,cumulative_sub_phi))

        with open(self._JName,"a") as f:
            for subproblem in subproblems:
                f.write(", %s" % subproblem)
            f.write("\n")

        print("PHI=%s" % phi)
        if phi > 0:
            tau = 1.0 # this is the over-relaxation parameter - we need to do something more useful
            # probability weighted norms are used below - this doesn't match the paper.
            theta = phi/(p_unorm*p_unorm + p_vnorm*p_vnorm) 
            print("THETA=%s" % theta)
            for stage in ph._scenario_tree._stages[:-1]:
                for tree_node in stage._tree_nodes:
                    if self._check_output:
                        print("TREE NODE ZS BEFORE: %s" % tree_node._z)
                        print("TREE NODE VS BEFORE: %s" % tree_node._v)
                    tree_node_zs = tree_node._z
                    for variable_id in tree_node._standard_variable_ids:
                        for scenario in tree_node._scenarios:
                            rho_values = scenario._rho[tree_node._name]
                            weight_values = scenario._w[tree_node._name]
                            if self._check_output:
                                print("WEIGHT VALUE PRIOR TO MODIFICATION=",weight_values[variable_id])
                                print("U VALUE PRIOR TO MODIFICATION=",scenario._u[variable_id])
#                            print("SUBTRACTING TERM TO Z=%s" % (tau * theta * tree_node._v[variable_id]))
                            tree_node._z[variable_id] -= (tau * theta * tree_node._v[variable_id])
                            weight_values[variable_id] += (tau * theta * scenario._u[variable_id])
                            if self._check_output:
                                print("NEW WEIGHT FOR VARIABLE=",variable_id,"FOR SCENARIO=",scenario._name,"EQUALS",weight_values[variable_id])
#                    print("TREE NODE ZS AFTER: %s" % tree_node._z)
        elif phi == 0.0:
            print("***PHI WAS ZERO - NOT DOING ANYTHING - NO MOVES - DOING CHECK BELOW!")
            pass
        else:
            # WE MAY NOT BE SCREWED, BUT WE'LL ASSUME SO FOR NOW.
            print("***PHI IS NEGATIVE - NOT DOING ANYTHING")

        # CHECK HERE - PHI SHOULD BE 0 AT THIS POINT - THIS IS JUST A CHECK
        with open(self._JName,"a") as f:
             f.write("%10d" % (ph._current_iteration))
#        print("COMPUTING NEW PHI***")
        phi = 0.0

        sub_phi_to_scenario_map = {}

        for scenario in tree_node._scenarios:
            for tree_node in scenario._node_list[:-1]:
                tree_node_zs = tree_node._z
                cumulative_sub_phi = 0.0
                for variable_id in tree_node._standard_variable_ids:
                    var_values = scenario._x[tree_node._name]
                    varval = var_values[variable_id]
                    weight_values = scenario._w[tree_node._name]
                    if varval is not None:
                        sub_phi = scenario._probability * ((tree_node_zs[variable_id] - varval) * (scenario._y[variable_id] + weight_values[variable_id]))
                        cumulative_sub_phi += sub_phi
                        phi += sub_phi
                    else:
                        foobar

                # HEY - shouldn't the following be moved out one level of indentation, to map to the scenario? it of course works for two-stage.
                    
                if not cumulative_sub_phi in sub_phi_to_scenario_map:
                    sub_phi_to_scenario_map[cumulative_sub_phi] = []
                sub_phi_to_scenario_map[cumulative_sub_phi].append(scenario._name)

                with open(self._JName,"a") as f:
                    f.write(", %10f" % (cumulative_sub_phi))
                print("**SUB-PHI FOR SCENARIO=%s EQUALS %s" % (scenario._name,cumulative_sub_phi))

        print("NEW PHI=%s" % phi)
        with open(self._JName,"a") as f:
            f.write("\n")

        print("SUB PHI MAP=",sub_phi_to_scenario_map)

        negative_sub_phis = [sub_phi for sub_phi in sub_phi_to_scenario_map if sub_phi < 0.0]

        if len(negative_sub_phis) == 0:
            print("**** YIKES! QUEUING SUBPROBLEMS AT RANDOM****")
            # TBD - THIS ASSUMES UNIQUE PHIS, WHICH IS NOT ALWAYS THE CASE.
            all_phis = sub_phi_to_scenario_map.keys()
            random.shuffle(all_phis)
            for phi in all_phis[0:ph._async_buffer_length]:
                scenario_name = sub_phi_to_scenario_map[phi][0]
                print("QUEUEING SUBPROBLEM=",scenario_name)
                self._subproblems_to_queue.append(scenario_name)

        else:
            print("Selecting most negative phi scenarios to queue")
            sorted_phis = sorted(sub_phi_to_scenario_map.keys())
            for phi in sorted_phis[0:ph._async_buffer_length]:
                scenario_name = sub_phi_to_scenario_map[phi][0]
                print("QUEUEING SUBPROBLEM=",scenario_name)
                self._subproblems_to_queue.append(scenario_name)

    def reset(self, ph):
        self.__init__()

    def pre_ph_initialization(self,ph):
        """Called before PH initialization"""
        pass

    def post_instance_creation(self,ph):
        """Called after the instances have been created"""
        with open(self._JName,"w") as f:
            f.write("Phi Summary; generally two lines per iteration\n")
            f.write("Iteration ")
            for scenario in ph._scenario_tree._scenarios:
                f.write(", %10s" % (scenario._name))
            f.write(", Subproblems Returned")
            f.write("\n")

    def post_ph_initialization(self, ph):
        """Called after PH initialization"""
        pass

    ##########################################################
    # the following callbacks are specific to synchronous PH #
    ##########################################################

    def post_iteration_0_solves(self, ph):
        """Called after the iteration 0 solves"""

        # we want the PH estimates of the weights initially, but we'll compute them afterwards.
        ph._ph_weight_updates_enabled = False

        # we will also handle xbar updates (z).
        ph._ph_xbar_updates_enabled = False

    def post_iteration_0(self, ph):
        """Called after the iteration 0 solves, averages computation, and weight computation"""
        print("POST ITERATION 0 CALLBACK")

        # define y and u parameters for each non-leaf variable in each scenario.
        print("****ADDING Y, U, V, and Z PARAMETERS")

        for scenario in ph._scenario_tree._scenarios:

            scenario._y = {}
            scenario._u = {}

            # instance = scenario._instance

            for tree_node in scenario._node_list[:-1]:

                nodal_index_set = tree_node._standard_variable_ids
                assert nodal_index_set is not None

                scenario._y.update((variable_id, 0.0) for variable_id in nodal_index_set)
                scenario._u.update((variable_id, 0.0) for variable_id in nodal_index_set)
#                print "YS AFTER UPDATE:",scenario._y

        # define v and z parameters for each non-leaf variable in the tree.
        for stage in ph._scenario_tree._stages[:-1]:
            for tree_node in stage._tree_nodes:

                nodal_index_set = tree_node._standard_variable_ids
                assert nodal_index_set is not None

                tree_node._v = dict((i,0) for i in nodal_index_set)
                tree_node._z = dict((i,tree_node._averages[i]) for i in nodal_index_set)

        # copy z to xbar in the scenario tree, as we've told PH we will be taking care of it.
        for stage in ph._scenario_tree._stages[:-1]:
            for tree_node in stage._tree_nodes:

                nodal_index_set = tree_node._standard_variable_ids
                assert nodal_index_set is not None

                tree_node._xbars = dict((i,tree_node._z[i]) for i in nodal_index_set)

        # mainly to set up data structures.
        for scenario in ph._scenario_tree._scenarios:
            self.asynchronous_pre_scenario_queue(ph, scenario._name)

        # pick subproblems at random - we need a number equal to the async buffer length.
        async_buffer_length = ph._async_buffer_length
        all_subproblems = [scenario._name for scenario in ph._scenario_tree._scenarios]
        random.shuffle(all_subproblems)
        self._subproblems_to_queue = all_subproblems[0:ph._async_buffer_length]

    def pre_iteration_k_solves(self, ph):
        """Called before each iteration k solve"""
        pass

    def post_iteration_k_solves(self, ph):
        """Called after the iteration k solves"""
        pass

    def post_iteration_k(self, ph):
        """Called after the iteration k is finished"""
        pass

    ##########################################################

    ###########################################################
    # the following callbacks are specific to asynchronous PH #
    ###########################################################

    def pre_asynchronous_solves(self, ph):
        """Called before the asynchronous solve loop is executed"""
        pass

    def asynchronous_pre_scenario_queue(self, ph, scenario_name):
        """Called right before each scenario solve is been queued"""

        # we need to cache the z and w that were used when solving the input scenario.
        scenario = ph._scenario_tree.get_scenario(scenario_name)

        scenario._xbars_for_solve = {}
        for tree_node in scenario._node_list[:-1]:
            scenario._xbars_for_solve[tree_node._name] = dict((k,v) for k,v in iteritems(tree_node._z))

        scenario._ws_for_solve = {}
        for tree_node in scenario._node_list[:-1]:
            scenario._ws_for_solve[tree_node._name] = dict((k,v) for k,v in iteritems(scenario._w[tree_node._name]))

    def post_asynchronous_var_w_update(self, ph, subproblems):
        """Called after a batch of asynchronous sub-problems are solved and corresponding statistics are updated"""
        print("POST ASYNCH VAR W CALLBACK")
        self.compute_updates(ph, subproblems)

    def post_asynchronous_solves(self, ph):
        """Called after the asynchronous solve loop is executed"""
        pass

    def asynchronous_subproblems_to_queue(self, ph):
        """Called after subproblems within buffer length window have been processed"""
        result = self._subproblems_to_queue
        self._subproblems_to_queue = []
        return result

    ###########################################################

    def post_ph_execution(self, ph):
        """Called after PH has terminated"""
        pass
