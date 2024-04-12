import pypowsybl as pp
import pandas as pd


def network_2_buses_connected_by_1_line():
    """
    A very small network. 
     G1        LD2
     |    L12   | 
     |  ------- | 
     B1         B2

    """
    network = pp.network.create_empty("network_2_buses_connected_by_1_line")
    network.create_substations(id=["S1", "S2"])
    voltage_levels = pd.DataFrame.from_records(index='id', 
                                               data=[{'substation_id': 'S1', 'id': 'VL1', 'topology_kind': 'BUS_BREAKER', 'nominal_v': 400},
                                                    {'substation_id': 'S2', 'id': 'VL2', 'topology_kind': 'BUS_BREAKER', 'nominal_v': 400},])
    network.create_voltage_levels(voltage_levels)
    network.create_buses(id=['B1', 'B2'], voltage_level_id=['VL1', 'VL2'])
    network.create_lines(id='LINE', voltage_level1_id='VL1', bus1_id='B1',
                     voltage_level2_id='VL2', bus2_id='B2',
                     b1=0, b2=0, g1=0, g2=0, r=0.5, x=10)
    network.create_loads(id='LOAD', voltage_level_id='VL2', bus_id='B2', p0=100, q0=10)
    network.create_generators(id='GEN', voltage_level_id='VL1', bus_id='B1',
                                min_p=0, max_p=200, target_p=100,
                                voltage_regulator_on=True, target_v=400)
    return network

def network_3_nodes_connected_by_2_lines():
    """
    A very small network to test with more than 1 line.
     G1        LD2       LD3
     |    L12   |   L23   |
     |  ------- | ------- |
     B1         B2        B3

    """
    network = pp.network.create_empty()
    network.create_substations(id=["S1", "S2", "S3"])
    voltage_levels = pd.DataFrame.from_records(index='id', 
                                               data=[{'substation_id': 'S1', 'id': 'VL1', 'topology_kind': 'BUS_BREAKER', 'nominal_v': 400},
                                                     {'substation_id': 'S2', 'id': 'VL2', 'topology_kind': 'BUS_BREAKER', 'nominal_v': 400},
                                                     {'substation_id': 'S3', 'id': 'VL3', 'topology_kind': 'BUS_BREAKER', 'nominal_v': 400}])
    network.create_voltage_levels(voltage_levels)
    network.create_buses(id=['B1', 'B2', 'B3'], voltage_level_id=['VL1', 'VL2', 'VL3'])
    network.create_lines(id='LINE12', voltage_level1_id='VL1', bus1_id='B1',
                     voltage_level2_id='VL2', bus2_id='B2',
                     b1=0, b2=0, g1=0, g2=0, r=0.5, x=10)
    network.create_lines(id='LINE23', voltage_level1_id='VL2', bus1_id='B2',
                     voltage_level2_id='VL3', bus2_id='B3',
                     b1=0, b2=0, g1=0, g2=0, r=0.5, x=10)
    network.create_loads(id='LOAD2', voltage_level_id='VL2', bus_id='B2', p0=5, q0=2)
    network.create_loads(id='LOAD3', voltage_level_id='VL3', bus_id='B3', p0=100, q0=10)
    network.create_generators(id='GEN1', voltage_level_id='VL1', bus_id='B1',
                                min_p=0, max_p=200, target_p=100,
                                voltage_regulator_on=True, target_v=400)
    return network


def network_3_nodes_connected_by_2_lines_with_1_shunt():
    """
    A very small network to test with a shunt (with 1 section).
     G1        LD2       SHUNT
     |    L12   |   L23   |
     |  ------- | ------- |
     B1         B2        B3

    """
    network = pp.network.create_empty()
    network.create_substations(id=["S1", "S2"])
    voltage_levels = pd.DataFrame.from_records(index='id', 
                                               data=[{'substation_id': 'S1', 'id': 'VL1', 'topology_kind': 'BUS_BREAKER', 'nominal_v': 400},
                                                     {'substation_id': 'S2', 'id': 'VL2', 'topology_kind': 'BUS_BREAKER', 'nominal_v': 400},
                                                     {'substation_id': 'S2', 'id': 'VL3', 'topology_kind': 'BUS_BREAKER', 'nominal_v': 400}])
    network.create_voltage_levels(voltage_levels)
    network.create_buses(id=['B1', 'B2', 'B3'], voltage_level_id=['VL1', 'VL2', 'VL3'])
    network.create_lines(id='LINE12', voltage_level1_id='VL1', bus1_id='B1',
                     voltage_level2_id='VL2', bus2_id='B2',
                     b1=0, b2=0, g1=0, g2=0, r=1, x=3)
    network.create_lines(id='LINE23', voltage_level1_id='VL2', bus1_id='B2',
                     voltage_level2_id='VL3', bus2_id='B3',
                     b1=0, b2=0, g1=0, g2=0, r=1, x=3)
    network.create_loads(id='LOAD2', voltage_level_id='VL2', bus_id='B2', p0=101, q0=150)
    network.create_generators(id='GEN1', voltage_level_id='VL1', bus_id='B1',
                                min_p=0, max_p=150, target_p=101.3664,
                                voltage_regulator_on=True, target_v=390)
    shunt_df = pd.DataFrame.from_records(
        index='id',
        columns=['id', 'name', 'model_type', 'section_count', 'target_v',
                 'target_deadband', 'voltage_level_id', 'bus_id'],
        data=[('SHUNT_TEST', '', 'LINEAR', 1, 393, 5.0, 'VL3', 'B3')])
    model_df = pd.DataFrame.from_records(
        index='id',
        columns=['id', 'g_per_section', 'b_per_section', 'max_section_count'],
        data=[('SHUNT_TEST', 0., 3e-3, 2)])
    network.create_shunt_compensators(shunt_df, model_df)
    return network


def network_3_nodes_connected_by_1_line_and_1_transformer():
    """
    A very small network to test with a transformer.
    G1        LD2      
    |    L12   |       
    |  ------- |       
    B1         B2      B3
                 \    /
                  T2WT
    """
    network = pp.network.create_empty()
    network.create_substations(id=["S1", "S2"])
    voltage_levels = pd.DataFrame.from_records(index='id', 
                                               data=[{'substation_id': 'S1', 'id': 'VL1', 'topology_kind': 'BUS_BREAKER', 'nominal_v': 400},
                                                     {'substation_id': 'S2', 'id': 'VL2', 'topology_kind': 'BUS_BREAKER', 'nominal_v': 400},
                                                     {'substation_id': 'S2', 'id': 'VL3', 'topology_kind': 'BUS_BREAKER', 'nominal_v': 400}])
    network.create_voltage_levels(voltage_levels)
    network.create_buses(id=['B1', 'B2', 'B3'], voltage_level_id=['VL1', 'VL2', 'VL3'])
    network.create_lines(id='LINE12', voltage_level1_id='VL1', bus1_id='B1',
                     voltage_level2_id='VL2', bus2_id='B2',
                     b1=0, b2=0, g1=0, g2=0, r=1, x=3)
    network.create_loads(id='LOAD2', voltage_level_id='VL2', bus_id='B2', p0=101, q0=150)
    network.create_generators(id='GEN1', voltage_level_id='VL1', bus_id='B1',
                                min_p=0, max_p=150, target_p=101.3664,
                                voltage_regulator_on=True, target_v=390)
    network.create_2_windings_transformers(id='T-23', voltage_level1_id='VL2', bus1_id='B2',
                                       voltage_level2_id='VL3', bus2_id='B3',
                                       b=1e-6, g=1e-6, r=0.5, x=10, rated_u1=400, rated_u2=225)
    return network


def network_3_nodes_connected_by_1_line_and_1_transformer_with_rtc():
    """
    A very small network to test with a ratio tap changer.
    """
    network = network_3_nodes_connected_by_1_line_and_1_transformer()
    # add a ratio tap changer to the transformer
    rtc_df = pd.DataFrame.from_records(
        index='id',
        columns=['id', 'target_deadband', 'target_v', 'on_load', 'low_tap', 'tap'],
        data=[('T-23', 2, 200, False, 0, 1)])
    steps_df = pd.DataFrame.from_records(
        index='id',
        columns=['id', 'b', 'g', 'r', 'x', 'rho'],
        data=[('T-23', 2, 2, 1, 1, 0.5),
            ('T-23', 2, 2, 1, 1, 0.5),
            ('T-23', 2, 2, 1, 1, 0.8)])
    network.create_ratio_tap_changers(rtc_df, steps_df)
    return network


def network_3_nodes_connected_by_1_line_and_1_transformer_with_ptc():
    """
    A very small network to test with a phase tap changer.
    """
    network = network_3_nodes_connected_by_1_line_and_1_transformer()
    # add a phase tap changer to the transformer
    ptc_df = pd.DataFrame.from_records(
        index='id',
        columns=['id', 'target_deadband', 'regulation_mode', 'low_tap', 'tap'],
        data=[('T-23', 2, 'FIXED_TAP', 0, 1)])
    steps_df = pd.DataFrame.from_records(
        index='id',
        columns=['id', 'b', 'g', 'r', 'x', 'rho', 'alpha'],
        data=[('T-23', 2, 2, 1, 1, 0.5, 0.1),
            ('T-23', 2, 2, 1, 1, 0.5, 0.2),
            ('T-23', 2, 2, 1, 1, 0.8, 0.1)])
    network.create_phase_tap_changers(ptc_df, steps_df)
    return network