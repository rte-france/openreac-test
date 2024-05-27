import pytest
from .utils import *
from shared.openreac_output_comparison import *

@pytest.mark.acopf_output_test
def test_acopf_on_network_of_2_nodes_connected_by_1_line():
    """
    Very simple test of ACOPF modelisation on network with 2 nodes.
    """
    network = network_2_buses_connected_by_1_line()
    run_acopf(network, AMPL_DIR, OUTPUT_DIR, RESOURCES_PATH)
    voltage_results, flows_results = load_acopf_output(OUTPUT_DIR)
    
    # verify voltage values
    assert compare_v(0.701, voltage_results.loc[voltage_results["bus_cc"] == 1, "v"].iloc[0])
    assert compare_phi(0.013, voltage_results.loc[voltage_results["bus_cc"] == 1, "teta"].iloc[0])
    assert compare_v(.700, voltage_results.loc[voltage_results["bus_cc"] == 2, "v"].iloc[0])
    assert compare_phi(0.000, voltage_results.loc[voltage_results["bus_cc"] == 2, "teta"].iloc[0])

    # verify flows results
    assert compare_p(1.42665, flows_results.loc[(flows_results["num"] == 1) & (flows_results["bus1"] == 1) & (flows_results["bus2"] == 2), "P1"].iloc[0])
    assert compare_q(0.16094, flows_results.loc[(flows_results["num"] == 1) & (flows_results["bus1"] == 1) & (flows_results["bus2"] == 2), "Q1"].iloc[0])
    assert compare_p(-1.42857, flows_results.loc[(flows_results["num"] == 1) & (flows_results["bus1"] == 1) & (flows_results["bus2"] == 2), "P2"].iloc[0])
    assert compare_q(-0.14286, flows_results.loc[(flows_results["num"] == 1) & (flows_results["bus1"] == 1) & (flows_results["bus2"] == 2), "Q2"].iloc[0])


