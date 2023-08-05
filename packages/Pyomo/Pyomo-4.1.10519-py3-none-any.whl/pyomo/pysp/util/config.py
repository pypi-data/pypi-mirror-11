import sys
import copy
import logging

import pyutilib.misc.config
from pyutilib.misc.config import (ConfigValue,
                                  ConfigBlock)
from pyomo.core.base import maximize, minimize

import six

logger = logging.getLogger('pyomo.pysp')

# TODO:
# - add and implement option to disable PH advanced preprocessing
# - anything phpyro named to sppyro named
# - from model_name to model_location
# - objective_sense to objective_sense_stage_based
# - from bound_cfgfile to boundsetter_callback
# - from aggregate_cfgfile to aggregategetter_callback
# - from "--scenario-tree-seed"
# - from solver_manager scenario_tree_manager, and add pyro solver manager support with sppyro
# - from pyro_manager_hostname to pyro_hostname
# - from rho_cfgfile to phrhosetter_callback
# - implement ph_timelimit
# - Default True? for enable_normalized_termdiff_convergence
# - integer variables? with implementation and command-line option name of retain_quadratic_binary_terms
# - implementation of drop_proximal_terms
# - generalize for options configurations with enable_ww_extensions, ww_extension_cfgfile, ww_extension_annotationfile, user_defined_extension,
# - generalize options collection for ph convergers
# - profile_memory implemented?

def _domain_must_be_str(val):
    if not isinstance(val, six.string_types):
        raise TypeError(
            "Option value must be a built-in "
            "string type, not '%s'" % (type(val)))
    return val

def _domain_tuple_of_str(val):
    if isinstance(val, six.string_types):
        return (val,)
    elif not isinstance(val, (list, tuple)):
        raise TypeError(
            "Option value must be a built-in list or "
            "tuple of string type, not '%s'" % (type(val)))
    else:
        for _v in val:
            if not isinstance(_v, six.string_types):
                raise TypeError(
                    "Option value must be a built-in "
                    "string type, not '%s'" % (type(_v)))
        return tuple(_v for _v in val)

#
# register an option to a ConfigBlock,
# making sure nothing is overwritten
#
def safe_register_option(configblock,
                         name,
                         configvalue,
                         *args,
                         **kwds):
    assert isinstance(configblock, ConfigBlock)
    assert configvalue._parent == None
    assert configvalue._userSet == False
    assert configvalue._userAccessed == False
    if name not in configblock:
        configblock.declare(
            name,
            copy.deepcopy(configvalue)).\
            declare_as_argument(*args, **kwds)
    else:
        current = configblock.get(name)
        assert current._userSet == configvalue._userSet
        assert current._userAccessed == configvalue._userAccessed
        assert current._data == configvalue._data
        assert current._default == configvalue._default
        assert current._domain == configvalue._domain
        assert current._description == configvalue._description
        assert current._doc == configvalue._doc
        assert current._visibility == configvalue._visibility
        assert current._argparse == configvalue._argparse

#
# register an option to a ConfigBlock,
# throwing an error if the name is not new
#
def safe_register_unique_option(configblock,
                                name,
                                configvalue,
                                *args,
                                **kwds):

    assert isinstance(configblock, ConfigBlock)
    assert configvalue._parent == None
    assert configvalue._userSet == False
    assert configvalue._userAccessed == False
    if name in configblock:
        raise RuntimeError(
            "Option registration failed. An option "
            "with name '%s' already exists on the ConfigBlock."
            % (name))
    configblock.declare(
        name,
        copy.deepcopy(configvalue)).\
        declare_as_argument(*args, **kwds)

common_block = ConfigBlock("A collection of common PySP options")

safe_register_unique_option(
    common_block,
    "model_location",
    ConfigValue(
        ".",
        domain=_domain_must_be_str,
        description=(
            "The directory or filename where the reference model is "
            "found. If a directory is given, the reference model is "
            "assumed to reside in a file named 'ReferenceModel.py' in "
            "that directory.  Default is '.'. "
        ),
        doc=None,
        visibility=0),
    "-m",
    "--model-location")

safe_register_unique_option(
    common_block,
    "scenario_tree_location",
    ConfigValue(
        None,
        domain=_domain_must_be_str,
        description=(
            "The directory or filename where the scenario tree "
            "structure is defined. If a directory is given, the "
            "scenario tree structure is assumed to reside in a file "
            "named 'ScenarioStructure.dat' in that directory. All "
            "scenario data files are assumed to reside in the same "
            "directory. If unspecified, it is assumed that reference "
            "model is of type ConcreteModel and the reference model "
            "file contains a callback named "
            "'pysp_instance_creation_callback'."
        ),
        doc=None,
        visibility=0),
    "-s",
    "--scenario-tree-location")

_objective_sense_choices = \
    [maximize, 'max', 'maximize',
     minimize, 'min', 'minimize', None]
def _objective_sense_domain(val):
    if val in ('min', 'minimize', minimize):
        return minimize
    elif val in ('max', 'maximize', maximize):
        return maximize
    elif val is None:
        return None
    else:
        raise ValueError(
            "Invalid choice: %s. (choose from one of %s"
            % (val, _objective_sense_choices))
safe_register_unique_option(
    common_block,
    "objective_sense_stage_based",
    ConfigValue(
        None,
        domain=_objective_sense_domain,
        description=(
            "The objective sense to use when auto-generating the "
            "scenario instance objective function, which is equal to "
            "the sum of the scenario-tree stage costs declared on the "
            "reference model.  If unspecified, it is assumed a "
            "stage-cost based objective function has been declared on "
            "the reference model."
        ),
        doc=None,
        visibility=0),
    "-o",
    "--objective-sense-stage-based",
    choices=_objective_sense_choices)

safe_register_unique_option(
    common_block,
    "boundsetter_callback",
    ConfigValue(
        None,
        domain=_domain_must_be_str,
        description=(
            "File containing containing a 'pysp_boundsetter_callback' "
            "function, used to update per-scenario variable bounds. "
            "This callback will be executed immediately after the "
            "'pysp_aggregategetter_callback' function during the "
            "instance construction phase of scenario tree setup."
        ),
        doc=None,
        visibility=0))

safe_register_unique_option(
    common_block,
    "aggregategetter_callback",
    ConfigValue(
        None,
        domain=_domain_must_be_str,
        description=(
            "File containing containing a "
            "'pysp_aggregategetter_callback' function, used to collect "
            "and store aggregate scenario information on the main "
            "scenario tree manager during the instance construction "
            "phase of scenario tree setup. If the scenario tree is "
            "distributed across multiple processes, this information "
            "will be broadcast at the end of collection."
        ),
        doc=None,
        visibility=0))

safe_register_unique_option(
    common_block,
    "scenario_tree_random_seed",
    ConfigValue(
        None,
        domain=int,
        description=(
            "The random seed associated with manipulation operations "
            "on the scenario tree (e.g., down-sampling or bundle "
            "creation). Default is None, indicating unassigned."
        ),
        doc=None,
        visibility=0))

safe_register_unique_option(
    common_block,
    "scenario_tree_downsample_fraction",
    ConfigValue(
        None,
        domain=int,
        description=(
            "The proportion of the scenarios in the scenario tree that "
            "are actually used.  Specific scenarios are selected at "
            "random.  Default is 1.0, indicating no down-sampling."
        ),
        doc=None,
        visibility=0))

safe_register_unique_option(
    common_block,
    "scenario_bundle_specification",
    ConfigValue(
        None,
        domain=_domain_must_be_str,
        description=(
            "The name of the scenario bundling specification to be "
            "used when generating the scenario tree.  Default is "
            "None, indicating no bundling is employed. If the "
            "specified name ends with a .dat suffix, the argument is "
            "interpreted as the path to a file. Otherwise, the name "
            "is interpreted as a file in the instance directory, "
            "constructed by adding the .dat suffix automatically."
        ),
        doc=None,
        visibility=0))

safe_register_unique_option(
    common_block,
    "create_random_bundles",
    ConfigValue(
        0,
        domain=int,
        description=(
            "Specification to create the indicated number of random, "
            "equally-sized (to the degree possible) scenario "
            "bundles. Default is 0, indicating no scenario bundles "
            "will be created."
        ),
        doc=None,
        visibility=0))

safe_register_unique_option(
    common_block,
    "scenario_tree_manager",
    ConfigValue(
        "serial",
        domain=_domain_must_be_str,
        description=(
            "The type of scenario tree manager to use. The default, "
            "'serial', builds all scenario instances on the parent "
            "process and performs all scenario tree operations "
            "sequentially. If 'sppyro' is specified, the scenario tree "
            "is fully distributed and scenario tree operations are "
            "performed asynchronously."
        ),
        doc=None,
        visibility=0))

safe_register_unique_option(
    common_block,
    "pyro_hostname",
    ConfigValue(
        None,
        domain=_domain_must_be_str,
        description=(
            "The hostname to bind on when searching for a Pyro "
            "nameserver. By default, the first nameserver found will be "
            "used. This option can also help speed up initialization "
            "time if the hostname is known (e.g., localhost)."
        ),
        doc=None,
        visibility=0))

safe_register_unique_option(
    common_block,
    "handshake_with_sppyro",
    ConfigValue(
        False,
        domain=bool,
        description=(
            "Take extra steps to acknowledge Pyro based requests are "
            "received by workers. It is often expedient to ignore the "
            "simple acknowledegment results returned."
        ),
        doc=None,
        visibility=0))

safe_register_unique_option(
    common_block,
    "sppyro_required_workers",
    ConfigValue(
        None,
        domain=int,
        description=(
            "Set the number of idle PySP-Pyro worker processes "
            "expected to be available when the 'sppyro' scenario tree "
            "manager is selected. This option should be used when the "
            "number of workers is less than the total number of "
            "scenarios (or bundles). When this option is not used, "
            "the manager will attempt to assign each scenario (or "
            "bundle) to a single worker process until the timeout "
            "indicated by the --sppyro-find-workers-timeout option occurs."
        ),
        doc=None,
        visibility=0))

safe_register_unique_option(
    common_block,
    "sppyro_find_workers_timeout",
    ConfigValue(
        30,
        domain=float,
        description=(
            "Set the time limit (seconds) for finding idle worker "
            "processes when the 'sppyro' scenario tree manager is "
            "selected. This option is ignored when "
            "--sppyro-required-workers is used.  Default is 30 "
            "seconds."
        ),
        doc=None,
        visibility=0))

safe_register_unique_option(
    common_block,
    "shutdown_pyro",
    ConfigValue(
        False,
        domain=bool,
        description=(
            "Attempt to shut down all Pyro-related (including sppyro) components "
            "associated with the Pyro name server used by any scenario "
            "tree manager or solver manager. Components to shutdown "
            "include the name server, dispatch server, and any worker "
            "processes. Note that in Pyro4, the nameserver will always "
            "ignore this request."
        ),
        doc=None,
        visibility=0))

safe_register_unique_option(
    common_block,
    "symbolic_solver_labels",
    ConfigValue(
        False,
        domain=bool,
        description=(
            "When interfacing with the solver, use symbol names "
            "derived from the model. For example, "
            "'my_special_variable[1_2_3]' instead of 'x552'.  Useful "
            "for debugging. When using NL file based solvers, this "
            "option results in corresponding .row (constraints) and "
            ".col (variables) file being created. The ordering in these "
            "files provides a mapping from NL file index to symbolic "
            "model names."
        ),
        doc=None,
        visibility=0))

safe_register_unique_option(
    common_block,
    "file_determinism",
    ConfigValue(
        1,
        domain=int,
        description=(
            "When interfacing with a solver using file based I/O, set "
            "the effort level for ensuring the file creation process is "
            "determistic. The default (1) sorts the index of components "
            "when transforming the model.  Anything less than 1 "
            "disables index sorting and can speed up model I/O. "
            "Anything greater than 1 additionaly sorts by component "
            "name to override declartion order."
        ),
        doc=None,
        visibility=0))

safe_register_unique_option(
    common_block,
    "output_solver_logs",
    ConfigValue(
        False,
        domain=bool,
        description=(
            "Output solver logs during scenario sub-problem solves."
        ),
        doc=None,
        visibility=0))

safe_register_unique_option(
    common_block,
    "output_times",
    ConfigValue(
        False,
        domain=bool,
        description=(
            "Output timing statistics during various runtime stages."
        ),
        doc=None,
        visibility=0))

safe_register_unique_option(
    common_block,
    "output_instance_construction_times",
    ConfigValue(
        False,
        domain=bool,
        description=(
            "Output timing statistics for instance construction. This "
            "option will be ignored when the scenario tree is "
            "distributed over multiple processes using sppyro."
        ),
        doc=None,
        visibility=0))

safe_register_unique_option(
    common_block,
    "verbose",
    ConfigValue(
        False,
        domain=bool,
        description=(
            "Generate verbose output for both initialization and "
            "execution."
        ),
        doc=None,
        visibility=0))

#
# PH Options
#

safe_register_unique_option(
    common_block,
    "ph_warmstart_file",
    ConfigValue(
        "",
        domain=_domain_must_be_str,
        description=(
            "Disable iteration 0 solves and warmstart rho, weight, "
            "and xbar parameters from solution or history file."
        ),
        doc=None,
        visibility=0))

safe_register_unique_option(
    common_block,
    "ph_warmstart_index",
    ConfigValue(
        "",
        domain=_domain_must_be_str,
        description=(
            "Indicates the iteration inside a history file from which "
            "to load a warmstart."
        ),
        doc=None,
        visibility=0))

def _rho_domain(val):
    val = float(val)
    if val < 0:
        raise ValueError(
            "Invalid value for default rho: %s. "
            "Value must be non-negative or None."
            % (val))
    return val

safe_register_unique_option(
    common_block,
    "default_rho",
    ConfigValue(
        None,
        domain=_rho_domain,
        description=(
            "The default PH rho value for all non-anticipative "
            "variables. *** Required ***"
        ),
        doc=None,
        visibility=0),
    "-r",
    "--default-rho")

_xhat_method_choices = \
    ['closest-scenario','voting','rounding']
def _xhat_method_domain(val):
    if val in _xhat_method_choices:
        return val
    else:
        raise ValueError(
            "Invalid choice: %s. (choose from one of %s"
            % (val, _xhat_method_choices))

safe_register_unique_option(
    common_block,
    "xhat_method",
    ConfigValue(
        "closest-scenario",
        domain=_xhat_method_domain,
        description=(
            "Specify the method used to compute a bounding solution at "
            "PH termination. Defaults to 'closest-scenario'. Other "
            "variants are: 'voting' and 'rounding'."
        ),
        doc=None,
        visibility=0),
    choices=_xhat_method_choices)

safe_register_unique_option(
    common_block,
    "overrelax",
    ConfigValue(
        False,
        domain=bool,
        description=(
            "Compute weight updates using combination of previous and "
            "current variable averages."
        ),
        doc=None,
        visibility=0))

safe_register_unique_option(
    common_block,
    "nu",
    ConfigValue(
        1.5,
        domain=float,
        description=(
            "Parameter used to update weights when using the overrelax "
            "option."
        ),
        doc=None,
        visibility=0))

safe_register_unique_option(
    common_block,
    "async",
    ConfigValue(
        False,
        domain=bool,
        description=(
            "Run PH in asychronous mode after iteration 0."
        ),
        doc=None,
        visibility=0))

safe_register_unique_option(
    common_block,
    "async_buffer_length",
    ConfigValue(
        1,
        domain=int,
        description=(
            "Number of scenarios to collect, if in async mode, before "
            "doing statistics and weight updates. Default is 1."
        ),
        doc=None,
        visibility=0))

safe_register_unique_option(
    common_block,
    "phrhosetter_callback",
    ConfigValue(
        None,
        domain=_domain_must_be_str,
        description=(
            "File containing a 'pysp_phrhosetter_callback' function, "
            "used to update per-variable rho parameters. This callback "
            "will be executed during PH initialization."
        ),
        doc=None,
        visibility=0))

safe_register_unique_option(
    common_block,
    "max_iterations",
    ConfigValue(
        100,
        domain=int,
        description=(
            "The maximal number of PH iterations. Default is 100."
        ),
        doc=None,
        visibility=0))

safe_register_unique_option(
    common_block,
    "ph_timelimit",
    ConfigValue(
        None,
        domain=float,
        description=(
            "Limits the number of seconds spent inside the solve "
            "method of PH."
        ),
        doc=None,
        visibility=0))

safe_register_unique_option(
    common_block,
    "termdiff_threshold",
    ConfigValue(
        0.0001,
        domain=float,
        description=(
            "The convergence threshold used in the term-diff and "
            "normalized term-diff convergence criteria. Default is "
            "0.0001."
        ),
        doc=None,
        visibility=0))

safe_register_unique_option(
    common_block,
    "enable_free_discrete_count_convergence",
    ConfigValue(
        False,
        domain=bool,
        description=(
            "Terminate PH based on the free discrete variable count "
            "convergence metric."
        ),
        doc=None,
        visibility=0))

safe_register_unique_option(
    common_block,
    "free_discrete_count_threshold",
    ConfigValue(
        20,
        domain=int,
        description=(
            "The convergence threshold used in the criterion based on "
            "when the free discrete variable count convergence "
            "criterion. Default is 20."
        ),
        doc=None,
        visibility=0))

safe_register_unique_option(
    common_block,
    "enable_normalized_termdiff_convergence",
    ConfigValue(
        True,
        domain=bool,
        description=(
            "Terminate PH based on the normalized termdiff convergence "
            "metric. Default is True. "
        ),
        doc=None,
        visibility=0))

safe_register_unique_option(
    common_block,
    "enable_termdiff_convergence",
    ConfigValue(
        False,
        domain=bool,
        description=(
            "Terminate PH based on the termdiff convergence metric."
        ),
        doc=None,
        visibility=0))

safe_register_unique_option(
    common_block,
    "enable_outer_bound_convergence",
    ConfigValue(
        False,
        domain=bool,
        description=(
            "Terminate PH based on the outer bound convergence "
            "metric."
        ),
        doc=None,
        visibility=0))

safe_register_unique_option(
    common_block,
    "outer_bound_convergence_threshold",
    ConfigValue(
        None,
        domain=float,
        description=(
            "The convergence threshold used in the outer bound "
            "convergence criterion. Default is None, indicating "
            "unassigned."
        ),
        doc=None,
        visibility=0))

safe_register_unique_option(
    common_block,
    "linearize_nonbinary_penalty_terms",
    ConfigValue(
        0,
        domain=int,
        description=(
            "Approximate the PH quadratic term for non-binary "
            "variables with a piece-wise linear function, using the "
            "supplied number of equal-length pieces from each bound to "
            "the average."
        ),
        doc=None,
        visibility=0))

safe_register_unique_option(
    common_block,
    "breakpoint_strategy",
    ConfigValue(
        0,
        domain=int,
        description=(
            "Specify the strategy to distribute breakpoints on the "
            "[lb, ub] interval of each variable when linearizing. 0 "
            "indicates uniform distribution. 1 indicates breakpoints at "
            "the node min and max, uniformly in-between. 2 indicates "
            "more aggressive concentration of breakpoints near the "
            "observed node min/max."
        ),
        doc=None,
        visibility=0))

safe_register_unique_option(
    common_block,
    "retain_quadratic_binary_terms",
    ConfigValue(
        False,
        domain=bool,
        description=(
            "Do not linearize PH objective terms involving binary "
            "decision variables."
        ),
        doc=None,
        visibility=0))

safe_register_unique_option(
    common_block,
    "drop_proximal_terms",
    ConfigValue(
        False,
        domain=bool,
        description=(
            "Eliminate proximal terms (i.e., the quadratic penalty "
            "terms) from the weighted PH objective."
        ),
        doc=None,
        visibility=0))

safe_register_unique_option(
    common_block,
    "enable_ww_extensions",
    ConfigValue(
        False,
        domain=bool,
        description=(
            "Enable the Watson-Woodruff PH extensions plugin."
        ),
        doc=None,
        visibility=0))

safe_register_unique_option(
    common_block,
    "ww_extension_cfgfile",
    ConfigValue(
        "",
        domain=_domain_must_be_str,
        description=(
            "The name of a configuration file for the Watson-Woodruff "
            "PH extensions plugin."
        ),
        doc=None,
        visibility=0))

safe_register_unique_option(
    common_block,
    "ww_extension_annotationfile",
    ConfigValue(
        "",
        domain=_domain_must_be_str,
        description=(
            "The name of a variable annotation file for the "
            "Watson-Woodruff PH extensions plugin."
        ),
        doc=None,
        visibility=0))

safe_register_unique_option(
    common_block,
    "user_defined_extension",
    ConfigValue(
        (),
        domain=_domain_tuple_of_str,
        description=(
            "The name of a python module specifying a user-defined PH "
            "extension plugin. Use this option when generating a template "
            "configuration file in order to include a plugin-specific "
            "options section. This option can be used multiple times."
        ),
        doc=None,
        visibility=0),
    action='append')

safe_register_unique_option(
    common_block,
    "solution_writer",
    ConfigValue(
        (),
        domain=_domain_tuple_of_str,
        description=(
            "The name of a python module specifying a user-defined "
            "plugin invoked to write the scenario tree solution. Use "
            "this option when generating a template configuration file "
            "in order to include a plugin-specific options "
            "section. This option can be used multiple times."
        ),
        doc=None,
        visibility=0),
    action='append')

safe_register_unique_option(
    common_block,
    "preprocess_fixed_variables",
    ConfigValue(
        False,
        domain=bool,
        description=(
            "Perform full preprocessing of instances after fixing or "
            "freeing variables in scenarios. By default, fixed "
            "variables will be included in the problem but 'fixed' by "
            "overriding their bounds.  This increases the speed of "
            "Pyomo model I/O, but may be useful to disable in "
            "debugging situations or if numerical issues are "
            "encountered with certain solvers."
        ),
        doc=None,
        visibility=0))

def _scenario_mipgap_domain(val):
    val = float(val)
    if not (0 <= val <= 1):
        raise ValueError(
            "Invalid value for scenario mipgap: %s. "
            "A value in the interval [0,1] is required."
            % (val))

safe_register_unique_option(
    common_block,
    "scenario_mipgap",
    ConfigValue(
        None,
        domain=_scenario_mipgap_domain,
        description=(
            "Specifies the mipgap for all PH scenario sub-problems."
        ),
        doc=None,
        visibility=0))

safe_register_unique_option(
    common_block,
    "scenario_solver_options",
    ConfigValue(
        (),
        domain=_domain_tuple_of_str,
        description=(
            "Solver options for all PH scenario sub-problems. This "
            "option can be used multiple times."
        ),
        doc=None,
        visibility=0),
    action='append')

safe_register_unique_option(
    common_block,
    "solver",
    ConfigValue(
        "cplex",
        domain=_domain_must_be_str,
        description=(
            "Optimization solver for all PH sub-problems."
        ),
        doc=None,
        visibility=0))

safe_register_unique_option(
    common_block,
    "solver_io",
    ConfigValue(
        None,
        domain=_domain_must_be_str,
        description=(
            "The type of IO used to execute the solver. Different "
            "solvers support different types of IO, but the following "
            "are common options: lp - generate LP files, nl - generate "
            "NL files, python - direct Python interface, os - generate "
            "OSiL XML files."
        ),
        doc=None,
        visibility=0))

safe_register_unique_option(
    common_block,
    "solver_manager",
    ConfigValue(
        "serial",
        domain=_domain_must_be_str,
        description=(
            "The type of solver manager used to coordinate scenario "
            "sub-problem solves. Default is serial."
        ),
        doc=None,
        visibility=0))

safe_register_unique_option(
    common_block,
    "sppyro_transmit_leaf_stage_variable_solutions",
    ConfigValue(
        False,
        domain=bool,
        description=(
            "By default, when running PH using the sppyro scenario "
            "tree manager, leaf-stage variable solutions are not "
            "transmitted back to the master scenario tree during "
            "intermediate iterations. This flag will override that "
            "behavior for cases where leaf-stage variable solutions are "
            "required on the master scenario tree. Using this option "
            "can degrade runtime performance. When PH exits, variable "
            "values are collected from all stages whether or not this "
            "option was used. Also, note that PH extensions have the "
            "ability to override this flag at runtime."
        ),
        doc=None,
        visibility=0))

safe_register_unique_option(
    common_block,
    "disable_warmstarts",
    ConfigValue(
        False,
        domain=bool,
        description=(
            "Disable warm-start of scenario sub-problem solves in PH "
            "iterations >= 1."
        ),
        doc=None,
        visibility=0))

safe_register_unique_option(
    common_block,
    "output_scenario_tree_solution",
    ConfigValue(
        False,
        domain=bool,
        description=(
            "If a feasible solution is found, report it (even leaves) "
            "in scenario tree format upon termination."
        ),
        doc=None,
        visibility=0))

safe_register_unique_option(
    common_block,
    "output_solver_results",
    ConfigValue(
        False,
        domain=bool,
        description=(
            "Output solutions obtained after each scenario sub-problem "
            "solve."
        ),
        doc=None,
        visibility=0))

safe_register_unique_option(
    common_block,
    "report_only_statistics",
    ConfigValue(
        False,
        domain=bool,
        description=(
            "When reporting solutions, only output per-variable "
            "statistics - not the individual scenario values."
        ),
        doc=None,
        visibility=0))

safe_register_unique_option(
    common_block,
    "report_solutions",
    ConfigValue(
        False,
        domain=bool,
        description=(
            "Always report PH solutions after each iteration. Enabled "
            "if --verbose is enabled."
        ),
        doc=None,
        visibility=0))

safe_register_unique_option(
    common_block,
    "report_weights",
    ConfigValue(
        False,
        domain=bool,
        description=(
            "Always report PH weights prior to each iteration. Enabled "
            "if --verbose is enabled."
        ),
        doc=None,
        visibility=0))

safe_register_unique_option(
    common_block,
    "report_rhos_each_iteration",
    ConfigValue(
        False,
        domain=bool,
        description=(
            "Always report PH rhos prior to each iteration."
        ),
        doc=None,
        visibility=0))

safe_register_unique_option(
    common_block,
    "report_rhos_first_iteration",
    ConfigValue(
        False,
        domain=bool,
        description=(
            "Report rhos prior to PH iteration 1. Enabled if --verbose "
            "is enabled."
        ),
        doc=None,
        visibility=0))

safe_register_unique_option(
    common_block,
    "report_for_zero_variable_values",
    ConfigValue(
        False,
        domain=bool,
        description=(
            "Report statistics (variables and weights) for all "
            "variables, not just those with values differing from 0."
        ),
        doc=None,
        visibility=0))

safe_register_unique_option(
    common_block,
    "report_only_nonconverged_variables",
    ConfigValue(
        False,
        domain=bool,
        description=(
            "Report statistics (variables and weights) only for "
            "non-converged variables."
        ),
        doc=None,
        visibility=0))

safe_register_unique_option(
    common_block,
    "suppress_continuous_variable_output",
    ConfigValue(
        False,
        domain=bool,
        description=(
            "Eliminate PH-related output involving continuous "
            "variables."
        ),
        doc=None,
        visibility=0))

safe_register_unique_option(
    common_block,
    "disable_gc",
    ConfigValue(
        False,
        domain=bool,
        description=(
            "Disable the python garbage collecter."
        ),
        doc=None,
        visibility=0))

safe_register_unique_option(
    common_block,
    "profile_memory",
    ConfigValue(
        False,
        domain=bool,
        description=(
            "If Guppy is available, report memory usage statistics "
            "for objects created by various PySP constructs."
        ),
        doc=None,
        visibility=0))

safe_register_unique_option(
    common_block,
    "keep_solver_files",
    ConfigValue(
        False,
        domain=bool,
        description=(
            "Retain temporary input and output files for scenario "
            "sub-problem solves."
        ),
        doc=None,
        visibility=0))

safe_register_unique_option(
    common_block,
    "profile",
    ConfigValue(
        0,
        domain=int,
        description=(
            "Enable profiling of Python code. The value of this "
            "option is the number of functions that are summarized."
        ),
        doc=None,
        visibility=0))

safe_register_unique_option(
    common_block,
    "traceback",
    ConfigValue(
        False,
        domain=bool,
        description=(
            "When an exception is thrown, show the entire call "
            "stack. Ignored if profiling is enabled."
        ),
        doc=None,
        visibility=0))

#
# Deprecated command-line option names
# (DO NOT REGISTER THEM OUTSIDE OF THIS FILE)
#
_map_to_deprecated = {}
_deprecated_block = ConfigBlock("A collection of common deprecated PySP command-line options")
if pyutilib.misc.config.argparse_is_available:

    #
    # --model-directory
    #
    class _DeprecatedModelDirectory(pyutilib.misc.config.argparse.Action):
        def __init__(self, option_strings, dest, nargs=None, **kwargs):
            if nargs is not None:
                raise ValueError("nargs not allowed")
            super(_DeprecatedModelDirectory, self).\
                __init__(option_strings, dest, **kwargs)
        def __call__(self, parser, namespace, values, option_string=None):
            logger.warning(
                "DEPRECATED: The '--model-directory' command-line "
                "option has been deprecated and will be removed "
                "in the future. Please use --model-location instead.")
            setattr(namespace, 'CONFIGBLOCK.model_location', values)

    def _warn_model_directory(val):
        # don't use logger here since users might not import
        # the pyomo logger in a scripting interface
        sys.stderr.write(
            "\tWARNING: The 'model_directory' config item will be ignored "
            "unless it is being used as a command-line option "
            "where it can be redirected to 'model_location'. "
            "Please use 'model_location' instead.\n")
        return _domain_must_be_str(val)

    safe_register_unique_option(
        _deprecated_block,
        "model_directory",
        ConfigValue(
            None,
            domain=_warn_model_directory,
            description=(
                "Deprecated alias for --model-location"
            ),
            doc=None,
            visibility=-1),
        "--model-directory",
        action=_DeprecatedModelDirectory)
    _map_to_deprecated['model_location'] = \
        _deprecated_block.get('model_directory')

    #
    # -i, --instance-directory
    #
    class _DeprecatedInstanceDirectory(pyutilib.misc.config.argparse.Action):
        def __init__(self, option_strings, dest, nargs=None, **kwargs):
            if nargs is not None:
                raise ValueError("nargs not allowed")
            super(_DeprecatedInstanceDirectory, self).\
                __init__(option_strings, dest, **kwargs)
        def __call__(self, parser, namespace, values, option_string=None):
            logger.warning(
                "DEPRECATED: The '--instance-directory' ('-i') command-line "
                "option has been deprecated and will be removed "
                "in the future. Please use '--scenario-tree-location' ('-s') instead.")
            setattr(namespace, 'CONFIGBLOCK.scenario_tree_location', values)

    def _warn_instance_directory(val):
        # don't use logger here since users might not import
        # the pyomo logger in a scripting interface
        sys.stderr.write(
            "\tWARNING: The 'instance_directory' config item will be ignored "
            "unless it is being used as a command-line option "
            "where it can be redirected to 'scenario_tree_location'. "
            "Please use 'scenario_tree_location' instead.\n")
        return _domain_must_be_str(val)

    safe_register_unique_option(
        _deprecated_block,
        "instance_directory",
        ConfigValue(
            None,
            domain=_warn_instance_directory,
            description=(
                "Deprecated alias for --scenario-tree-location, -s"
            ),
            doc=None,
            visibility=-1),
        "-i",
        "--instance-directory",
        action=_DeprecatedInstanceDirectory)
    _map_to_deprecated['scenario_tree_location'] = \
        _deprecated_block.get('instance_directory')

    #
    # --handshake-with-phpyro
    #

    class _DeprecatedHandshakeWithPHPyro(pyutilib.misc.config.argparse.Action):
        def __init__(self, option_strings, dest, nargs=None, **kwargs):
            if nargs is not None:
                raise ValueError("nargs not allowed")
            super(_DeprecatedHandshakeWithPHPyro, self).\
                __init__(option_strings, dest, nargs=0, **kwargs)
        def __call__(self, parser, namespace, values, option_string=None):
            logger.warning(
                "DEPRECATED: The '--handshake-with-phpyro command-line "
                "option has been deprecated and will be removed "
                "in the future. Please use '--handshake-with-sppyro instead.")
            setattr(namespace, 'CONFIGBLOCK.handshake_with_sppyro', True)

    def _warn_handshake_with_phpyro(val):
        # don't use logger here since users might not import
        # the pyomo logger in a scripting interface
        sys.stderr.write(
            "\tWARNING: The 'handshake_with_phpyro' config item will be ignored "
            "unless it is being used as a command-line option "
            "where it can be redirected to 'handshake_with_sppyro'. "
            "Please use 'handshake_with_sppyro' instead.\n")
        return bool(val)

    safe_register_unique_option(
        _deprecated_block,
        "handshake_with_phpyro",
        ConfigValue(
            None,
            domain=_warn_handshake_with_phpyro,
            description=(
                "Deprecated alias for --handshake-with-sppyro"
            ),
            doc=None,
            visibility=-1),
        action=_DeprecatedHandshakeWithPHPyro)
    _map_to_deprecated['handshake_with_sppyro'] = \
        _deprecated_block.get('handshake_with_phpyro')

    #
    # --phpyro-required-workers
    #

    class _DeprecatedPHPyroRequiredWorkers(pyutilib.misc.config.argparse.Action):
        def __init__(self, option_strings, dest, nargs=None, **kwargs):
            if nargs is not None:
                raise ValueError("nargs not allowed")
            super(_DeprecatedPHPyroRequiredWorkers, self).\
                __init__(option_strings, dest, **kwargs)
        def __call__(self, parser, namespace, values, option_string=None):
            logger.warning(
                "DEPRECATED: The '--phpyro-required-workers command-line "
                "option has been deprecated and will be removed "
                "in the future. Please use '--sppyro-required-workers instead.")
            setattr(namespace, 'CONFIGBLOCK.sppyro_required_workers', values)

    def _warn_phpyro_required_workers(val):
        # don't use logger here since users might not import
        # the pyomo logger in a scripting interface
        sys.stderr.write(
            "\tWARNING: The 'phpyro_required_workers' config item will be ignored "
            "unless it is being used as a command-line option "
            "where it can be redirected to 'sppyro_required_workers'. "
            "Please use 'sppyro_required_workers' instead.\n")
        return int(val)

    safe_register_unique_option(
        _deprecated_block,
        "phpyro_required_workers",
        ConfigValue(
            None,
            domain=_warn_phpyro_required_workers,
            description=(
                "Deprecated alias for --sppyro-required-workers"
            ),
            doc=None,
            visibility=-1),
        action=_DeprecatedPHPyroRequiredWorkers)
    _map_to_deprecated['sppyro_required_workers'] = \
        _deprecated_block.get('phpyro_required_workers')

    #
    # --phpyro-workers-timeout
    #

    class _DeprecatedPHPyroWorkersTimeout(pyutilib.misc.config.argparse.Action):
        def __init__(self, option_strings, dest, nargs=None, **kwargs):
            if nargs is not None:
                raise ValueError("nargs not allowed")
            super(_DeprecatedPHPyroWorkersTimeout, self).\
                __init__(option_strings, dest, **kwargs)
        def __call__(self, parser, namespace, values, option_string=None):
            logger.warning(
                "DEPRECATED: The '--phpyro-workers-timeout command-line "
                "option has been deprecated and will be removed "
                "in the future. Please use '--sppyro-find-workers-timeout instead.")
            setattr(namespace, 'CONFIGBLOCK.sppyro_find_workers_timeout', values)

    def _warn_phpyro_workers_timeout(val):
        # don't use logger here since users might not import
        # the pyomo logger in a scripting interface
        sys.stderr.write(
            "\tWARNING: The 'phpyro_workers_timeout' config item will be ignored "
            "unless it is being used as a command-line option "
            "where it can be redirected to 'sppyro_find_workers_timeout'. "
            "Please use 'sppyro_find_workers_timeout' instead.\n")
        return float(val)

    safe_register_unique_option(
        _deprecated_block,
        "phpyro_workers_timeout",
        ConfigValue(
            None,
            domain=_warn_phpyro_workers_timeout,
            description=(
                "Deprecated alias for --sppyro-find-workers-timeout"
            ),
            doc=None,
            visibility=-1),
        action=_DeprecatedPHPyroWorkersTimeout)
    _map_to_deprecated['sppyro_find_workers_timeout'] = \
        _deprecated_block.get('phpyro_workers_timeout')

    #
    # --phpyro-transmit-leaf-stage-variable-solutions
    #

    class _DeprecatedPHPyroTransmitLeafStageVariableSolutions(
            pyutilib.misc.config.argparse.Action):
        def __init__(self, option_strings, dest, nargs=None, **kwargs):
            if nargs is not None:
                raise ValueError("nargs not allowed")
            super(_DeprecatedPHPyroTransmitLeafStageVariableSolutions, self).\
                __init__(option_strings, dest, nargs=0, **kwargs)
        def __call__(self, parser, namespace, values, option_string=None):
            logger.warning(
                "DEPRECATED: The '--phpyro-transmit-leaf-stage-variable-solutions command-line "
                "option has been deprecated and will be removed "
                "in the future. Please use '--sppyro-transmit-leaf-stage-variable-solutions instead.")
            setattr(namespace, 'CONFIGBLOCK.sppyro_transmit_leaf_stage_variable_solutions', True)

    def _warn_phpyro_transmit_leaf_stage_variable_solutions(val):
        # don't use logger here since users might not import
        # the pyomo logger in a scripting interface
        sys.stderr.write(
            "\tWARNING: The 'phpyro_transmit_leaf_stage_variable_solutions' config item will be ignored "
            "unless it is being used as a command-line option "
            "where it can be redirected to 'sppyro_transmit_leaf_stage_variable_solutions'. "
            "Please use 'sppyro_transmit_leaf_stage_variable_solutions' instead.\n")
        return bool(val)

    safe_register_unique_option(
        _deprecated_block,
        "phpyro_transmit_leaf_stage_variable_solutions",
        ConfigValue(
            None,
            domain=_warn_phpyro_transmit_leaf_stage_variable_solutions,
            description=(
                "Deprecated alias for --sppyro-transmit-leaf-stage-variable-solutions"
            ),
            doc=None,
            visibility=-1),
        action=_DeprecatedPHPyroTransmitLeafStageVariableSolutions)
    _map_to_deprecated['sppyro_transmit_leaf_stage_variable_solutions'] = \
        _deprecated_block.get('phpyro_transmit_leaf_stage_variable_solutions')

    #
    # --scenario-tree-seed
    #

    class _DeprecatedScenarioTreeSeed(pyutilib.misc.config.argparse.Action):
        def __init__(self, option_strings, dest, nargs=None, **kwargs):
            if nargs is not None:
                raise ValueError("nargs not allowed")
            super(_DeprecatedScenarioTreeSeed, self).\
                __init__(option_strings, dest, **kwargs)
        def __call__(self, parser, namespace, values, option_string=None):
            logger.warning(
                "DEPRECATED: The '--scenario-tree-seed command-line "
                "option has been deprecated and will be removed "
                "in the future. Please use '--scenario-tree-random-seed instead.")
            setattr(namespace, 'CONFIGBLOCK.scenario_tree_random_seed', values)

    def _warn_scenario_tree_seed(val):
        # don't use logger here since users might not import
        # the pyomo logger in a scripting interface
        sys.stderr.write(
            "\tWARNING: The 'scenario_tree_seed' config item will be ignored "
            "unless it is being used as a command-line option "
            "where it can be redirected to 'scenario_tree_random_seed'. "
            "Please use 'scenario_tree_random_seed' instead.\n")
        return int(val)

    safe_register_unique_option(
        _deprecated_block,
        "scenario_tree_seed",
        ConfigValue(
            None,
            domain=_warn_scenario_tree_seed,
            description=(
                "Deprecated alias for --scenario-tree-random-seed"
            ),
            doc=None,
            visibility=-1),
        action=_DeprecatedScenarioTreeSeed)
    _map_to_deprecated['scenario_tree_random_seed'] = \
        _deprecated_block.get('scenario_tree_seed')


#
# Register a common option
#
def safe_register_common_option(configblock, name):
    assert isinstance(configblock, ConfigBlock)
    assert name not in _deprecated_block
    assert name in common_block
    common_value = common_block.get(name)
    assert common_value._parent == common_block
    assert common_value._userSet == False
    assert common_value._userAccessed == False
    if name not in configblock:
        common_value._parent = None
        common_value_copy = copy.deepcopy(common_value)
        common_value._parent = common_block
        configblock.declare(name, common_value_copy)
        #
        # handle deprecated command-line option names
        #
        if name in _map_to_deprecated:
            deprecated_value = _map_to_deprecated[name]
            assert deprecated_value._parent == _deprecated_block
            assert deprecated_value._userSet == False
            assert deprecated_value._userAccessed == False
            deprecated_value._parent = None
            deprecated_value_copy = copy.deepcopy(deprecated_value)
            deprecated_value._parent = _deprecated_block
            configblock.declare(deprecated_value_copy._name, deprecated_value_copy)
    else:
        current = configblock.get(name)
        assert current._userSet == common_value._userSet
        assert current._userAccessed == common_value._userAccessed
        assert current._data == common_value._data
        assert current._default == common_value._default
        assert current._domain == common_value._domain
        assert current._description == common_value._description
        assert current._doc == common_value._doc
        assert current._visibility == common_value._visibility
        assert current._argparse == common_value._argparse
        if name in _map_to_deprecated:
            deprecated_value = _map_to_deprecated[name]
            assert deprecated_value._name in configblock
            current = configblock.get(deprecated_value._name)
            assert current._userSet == deprecated_value._userSet
            assert current._userAccessed == deprecated_value._userAccessed
            assert current._data == deprecated_value._data
            assert current._default == deprecated_value._default
            assert current._domain == deprecated_value._domain
            assert current._description == deprecated_value._description
            assert current._doc == deprecated_value._doc
            assert current._visibility == deprecated_value._visibility
            assert current._argparse == deprecated_value._argparse

class Junk1(object):

    @staticmethod
    def register_options(config_block):
        common_option_names = [
            'model_location',
            'scenario_tree_location',
            'objective_sense_stage_based']
        for name in common_option_names:
            safe_register_common_option(config_block, name)

class Junk2(object):
    @staticmethod
    def register_options(config_block):
        for name in common_block:
            safe_register_common_option(config_block, name)

if __name__ == "__main__":
    import pyomo.environ
    import argparse

    block = ConfigBlock()
    Junk1.register_options(block)
    Junk2.register_options(block)

    ap = argparse.ArgumentParser()
    block.initialize_argparse(ap)
    block.import_argparse(ap.parse_args())

    #print block.generate_yaml_template()
    #print block.model_location
    #block.model_location = 'gabe'
    #print block.model_location
    #print block['model_location']
    #print block.get('model_location')
    #print list(block.user_values())
    #print list(block.unused_user_values())
    #block.model_location = '2'
    #block.phpyro_transmit_leaf_stage_variable_solutions = 1
    #print 'model_location' in block
    #print 'model location' in block
#    block.solution_writer
    #print type(block.model_location)
    print(list((_c._name, _c.value(False)) for _c in block.user_values()))
    print(list(_c._name for _c in block.unused_user_values()))

    #options = ConfigBlock()
    #options.model_location = common.get('model_location')

