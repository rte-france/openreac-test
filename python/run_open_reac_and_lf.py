import math
import pypowsybl as pp
import pypowsybl.loadflow as lf
import pypowsybl.voltage_initializer as v_init

def add_voltage_limit_overrides(network, params):
    """
    Add voltage limit overrides to open reac parameters, for all undefined voltage level limits of the network. 
    """
    low_voltage_overrides, high_voltage_overrides = [], []
    for id, row in network.get_voltage_levels().iterrows():
        if math.isnan(row['low_voltage_limit']):
            low_voltage_overrides.append((id, False, row['nominal_v'] * 0.7))
        if math.isnan(row['high_voltage_limit']):
            high_voltage_overrides.append((id, False, row['nominal_v'] * 1.3))
    params.add_specific_low_voltage_limits(low_voltage_overrides)
    params.add_specific_high_voltage_limits(high_voltage_overrides)

def test():
    network = pp.network.create_eurostag_tutorial_example1_network()

    # open reac parameters
    params = v_init.VoltageInitializerParameters()
    add_voltage_limit_overrides(network, params)
    
    # run open reac and apply results
    or_results = v_init.run(network, params, True)
    if (or_results.status == v_init.VoltageInitializerStatus.OK):
        or_results.apply_all_modifications(network)

    # load flow
    lf_parameters=lf.Parameters(voltage_init_mode=lf.VoltageInitMode.PREVIOUS_VALUES)
    lf_results = lf.run_ac(network, lf_parameters)
    for result in lf_results:
        print(result.status)
        assert result.status == lf.ComponentStatus.CONVERGED



if __name__ == "__main__":
    test()