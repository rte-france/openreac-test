import pytest
from commons import *

@pytest.mark.connnected_component_test
def test_connected_component_on_network_of_2_nodes_connected_by_1_line():
    """
    Very simple test of calculation of the connected component on network with 2 nodes.
    """
    network = network_2_buses_connected_by_1_line()
    run_connected_component(network, AMPL_CODE_PATH, OUTPUT_PATH, RESOURCES_PATH)
    bus_cc, null_phase_bus = import_connected_component_results(output_path=OUTPUT_PATH)
    # verify buses in the main synchronous component
    assert bus_cc.at[0, "bus_cc"] == 1
    assert bus_cc.at[1, "bus_cc"] == 2 
    # verify value of reference bus
    assert null_phase_bus == 2


