import pypowsybl as pp
import math

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
    network = pp.network.create_ieee9()
    params = pp.voltage_initializer.VoltageInitializerParameters()
    add_voltage_limit_overrides(network, params)
    # run open reac
    pp.voltage_initializer.run(network, params, True)

if __name__ == "__main__":
    test()