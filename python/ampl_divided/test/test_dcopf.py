import pytest
from .utils import *
from shared.openreac_output_comparison import *

@pytest.mark.dcopf_output_test
def test_dcopf_on_network_of_2_nodes_connected_by_1_line():
    """
    Very simple test of DCOPF modelisation on network with 2 nodes.
    """
    network = network_2_buses_connected_by_1_line()
    run_dcopf_only(network, AMPL_DIR, OUTPUT_DIR, RESOURCES_PATH)
    results = load_dcopf_output(path=OUTPUT_DIR)
    assert compare_phi(0.00625, results.loc[results["bus_cc"] == 1, "teta_dc"].iloc[0])
    assert compare_phi(0, results.loc[results["bus_cc"] == 2, "teta_dc"].iloc[0])


