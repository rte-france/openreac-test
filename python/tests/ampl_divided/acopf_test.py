import pytest
from commons import *

@pytest.mark.acopf_output_test
def test_acopf_on_network_of_2_nodes_connected_by_1_line():
    """
    Very simple test of ACOPF modelisation on network with 2 nodes.
    """
    network = network_2_buses_connected_by_1_line()
    run_acopf(network, AMPL_CODE_PATH, OUTPUT_PATH, RESOURCES_PATH)
    voltage_results, flows_results = import_acopf_results(output_path=OUTPUT_PATH)
    
    # verify voltage values
    assert is_diff_less_than_threshold(1.01817, voltage_results.loc[voltage_results["bus_cc"] == 1, "v"].iloc[0], DELTA_V)
    assert is_diff_less_than_threshold(0.00600, voltage_results.loc[voltage_results["bus_cc"] == 1, "teta"].iloc[0], DELTA_ANGLE)
    assert is_diff_less_than_threshold(1.01723, voltage_results.loc[voltage_results["bus_cc"] == 2, "v"].iloc[0], DELTA_V)
    assert is_diff_less_than_threshold(0.00000, voltage_results.loc[voltage_results["bus_cc"] == 2, "teta"].iloc[0], DELTA_ANGLE)

    # verify flows results
    assert is_diff_less_than_threshold(0.98245, flows_results.loc[(flows_results["num"] == 1) & (flows_results["bus1"] == 1) & (flows_results["bus2"] == 2), "P1"].iloc[0], DELTA_P)
    assert is_diff_less_than_threshold(0.10421, flows_results.loc[(flows_results["num"] == 1) & (flows_results["bus1"] == 1) & (flows_results["bus2"] == 2), "Q1"].iloc[0], DELTA_Q)
    assert is_diff_less_than_threshold(-0.98306, flows_results.loc[(flows_results["num"] == 1) & (flows_results["bus1"] == 1) & (flows_results["bus2"] == 2), "P2"].iloc[0], DELTA_P)
    assert is_diff_less_than_threshold(-0.09831, flows_results.loc[(flows_results["num"] == 1) & (flows_results["bus1"] == 1) & (flows_results["bus2"] == 2), "Q2"].iloc[0], DELTA_Q)


