# input files 
INPUT_NETWORK_FILES = {"ampl_network_batteries.txt", 
                       "ampl_network_branches.txt", 
                       "ampl_network_buses.txt", 
                       "ampl_network_generators.txt", 
                       "ampl_network_hvdc.txt", 
                       "ampl_network_lcc_converter_stations.txt",
                       "ampl_network_limits.txt", 
                       "ampl_network_loads.txt", 
                       "ampl_network_ptc.txt", 
                       "ampl_network_rtc.txt",
                       "ampl_network_shunts.txt", 
                       "ampl_network_static_var_compensators.txt", 
                       "ampl_network_substations.txt", 
                       "ampl_network_tct.txt", 
                       "ampl_network_vsc_converter_stations.txt"}

OR_INPUT_CONFIG_FILES = {"param_algo.txt", 
                      "param_generators_reactive.txt", 
                      "param_shunts.txt", 
                      "param_transformers.txt", 
                      "ampl_network_substations_override.txt"}

# output files 
OR_CSV_RESULTS_FILES = {"reactiveopf_results_generators.csv", 
                 "reactiveopf_results_rtc.csv", 
                 "reactiveopf_results_shunts.csv", 
                 "reactiveopf_results_static_var_compensators.csv", 
                 "reactiveopf_results_vsc_converter_stations.csv",
                 "reactiveopf_results_voltages.csv"}

INDICATORS_FILE = "reactiveopf_results_indic.txt"
AMPL_PRINTING_FILE = "AMPL_runner_0.out"