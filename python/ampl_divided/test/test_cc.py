import pytest
from .utils import *

@pytest.mark.connnected_component_test
def test_connected_component_on_network_of_2_nodes_connected_by_1_line():
    """
    Very simple test of calculation of the connected component on network with 2 nodes.
    """
    network = network_2_buses_connected_by_1_line()
    run_cc_only(network, AMPL_DIR, OUTPUT_DIR, RESOURCES_PATH)
    bus_cc, null_phase_bus = load_cc_output(output_path=OUTPUT_DIR)
    # verify buses in the main synchronous component
    assert bus_cc.at[0, "bus_cc"] == 1
    assert bus_cc.at[1, "bus_cc"] == 2 
    # verify value of reference bus
    assert null_phase_bus == 2


