import pytest
from .utils import *
from shared.openreac_output_comparison import *

INF_AMPL = 8.98845e+307

@pytest.mark.acopf_preprocessing_output_test
def test_default_Q_bounds():
    """
    Test the default behavior of ACOPF preprocessing when Q bounds are incoherent.
    """
    network = network_2_buses_connected_by_1_line()
    run_acopf_preprocessing(network, AMPL_DIR, OUTPUT_DIR, RESOURCES_PATH)
    generators_bounds = load_acopf_preprocessing_output(OUTPUT_DIR)
    
    assert compare_p(0, generators_bounds.loc[generators_bounds["num"] == 1, "Pmin"].iloc[0])
    assert compare_p(200, generators_bounds.loc[generators_bounds["num"] == 1, "Pmax"].iloc[0])
    assert compare_q(-60, generators_bounds.loc[generators_bounds["num"] == 1, "Qmin"].iloc[0])
    assert compare_q(60, generators_bounds.loc[generators_bounds["num"] == 1, "Qmax"].iloc[0])

@pytest.mark.acopf_preprocessing_output_test
def test_correct_bounds():
    """
    Test the behavior of ACOPF preprocessing block when Q bounds are coherent.
    """
    network = network_2_buses_connected_by_1_line()
    network.create_curve_reactive_limits(pd.DataFrame.from_records(index='id', 
                                               data=[{'id': 'GEN', 'p': -200, 'min_q': -5, 'max_q': 21.21},
                                                    {'id': 'GEN', 'p': 0, 'min_q': -17, 'max_q': 19},]))
    run_acopf_preprocessing(network, AMPL_DIR, OUTPUT_DIR, RESOURCES_PATH)
    generators_bounds = load_acopf_preprocessing_output(OUTPUT_DIR)

    assert compare_p(0, generators_bounds.loc[generators_bounds["num"] == 1, "Pmin"].iloc[0])
    assert compare_p(200, generators_bounds.loc[generators_bounds["num"] == 1, "Pmax"].iloc[0])
    assert compare_q(-17, generators_bounds.loc[generators_bounds["num"] == 1, "Qmin"].iloc[0])
    assert compare_q(19, generators_bounds.loc[generators_bounds["num"] == 1, "Qmax"].iloc[0])
