import pytest
from commons import *

@pytest.mark.dcopf_output_test
def test_dcopf_on_network_of_2_nodes_connected_by_1_line():
    """
    Very simple test of DCOPF modelisation on network with 2 nodes.
    """
    network = network_2_buses_connected_by_1_line()
    run_dcopf(network, AMPL_CODE_PATH, OUTPUT_PATH, RESOURCES_PATH)
    results = import_dcopf_results(output_path=OUTPUT_PATH)
    assert is_diff_less_than_threshold(0.00625, results.loc[results["bus_cc"] == 1, "teta_dc"].iloc[0], DELTA_ANGLE)
    assert is_diff_less_than_threshold(0, results.loc[results["bus_cc"] == 2, "teta_dc"].iloc[0], DELTA_ANGLE)


