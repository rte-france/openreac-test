import pytest
from .utils import *
from shared.openreac_output_comparison import *

INF_AMPL = 8.98845e+307

@pytest.mark.acopf_preprocessing_output_test
def test_acopf_on_network_of_2_nodes_connected_by_1_line():
    """
    Very simple test of ACOPF modelisation on network with 2 nodes.
    """
    network = network_2_buses_connected_by_1_line()
    run_acopf_preprocessing(network, AMPL_DIR, OUTPUT_DIR, RESOURCES_PATH)
    generators_bounds = load_acopf_preprocessing_output(OUTPUT_DIR)
    
    assert compare_p(0, generators_bounds.loc[generators_bounds["num"] == 1, "Pmin"].iloc[0])
    assert compare_p(200, generators_bounds.loc[generators_bounds["num"] == 1, "Pmax"].iloc[0])
    assert compare_q(-60, generators_bounds.loc[generators_bounds["num"] == 1, "Qmin"].iloc[0])
    assert compare_q(60, generators_bounds.loc[generators_bounds["num"] == 1, "Qmax"].iloc[0])
    
if __name__ == "__main__":
    test_acopf_on_network_of_2_nodes_connected_by_1_line()

