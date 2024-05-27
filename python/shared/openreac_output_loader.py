import pandas as pd

def load_open_reac_indicators(path, to_ignore=[]):
    """
    Load open reac indicators in a python dictionnary.
    
    Args:
        path: Path towards open reac indicators file.
        to_ignore: Indices of the indicators that will not be included in the dictionnary.
    """
    indicators = {}
    file = open(path)
    for num, line in enumerate(list(filter(lambda a: a != "\n" and a != "", file.readlines()))):
        # avoid ignored indicators
        if num in to_ignore:
            continue
        values = line.split(" ", 1)
        indicators[values[0]] = values[1].replace("\n", "")
    return indicators

def load_cc_output(output_path):
    """
    Load the output of the DCOPF. It consists of null phase bus and 
    buses in the main connected component.

    Args:
        path: Path towards dcopf output.
    """
    bus_cc_file = "connected_component_results.txt"
    null_phase_bus_file = "null_phase_bus.txt"

    # import bus_cc file result
    bus_cc = pd.read_csv(output_path / bus_cc_file, sep=" ", header=0)
    bus_cc.rename(columns=lambda x: x.replace('#', ''), inplace=True)

    # import null_phase_bus result
    with open(output_path / null_phase_bus_file, 'r') as f:
        next(f) # first line is a comment
        null_phase_bus = int(next(f).strip())

    return bus_cc, null_phase_bus

def load_dcopf_output(path):
    """
    Load the output of the DCOPF. It consists of voltage angles computed 
    for each bus of the main connected component.

    Args:
        path: Path towards dcopf output.
    """
    angle_results_file = "dcopf_angle_results.txt"
    angle_results = pd.read_csv(path / angle_results_file, sep=" ", header=0)
    angle_results.rename(columns=lambda x: x.replace('#', ''), inplace=True)
    return angle_results

def load_acopf_output(path):
    """
    Load the output of the ACOPF. It consists of voltage results for each bus, 
    and flows for each branch of the main CC.

    Args:
        path: Path towards acopf output.
    """
    voltage_results_file_name = "acopf_voltage_results.txt"
    voltage_results = pd.read_csv(path / voltage_results_file_name, sep=" ", header=0)
    voltage_results.rename(columns=lambda x: x.replace('#', ''), inplace=True)

    flows_results_file_name = "acopf_flows_results.txt"
    flows_results = pd.read_csv(path / flows_results_file_name, sep=" ", header=0)
    flows_results.rename(columns=lambda x: x.replace('#', ''), inplace=True)
    
    return voltage_results, flows_results

def load_acopf_preprocessing_output(path):
    """
    Load the output of the ACOPF preprocessing block. It consists of bounds for each active generator. 

    Args:
        path: Path towards acopf preprocessing output.
    """
    generators_bounds_file_name = "acopf_preprocessing_results.txt"
    generators_bounds = pd.read_csv(path / generators_bounds_file_name, sep=" ", header=0)
    generators_bounds.rename(columns=lambda x: x.replace('#', ''), inplace=True)
    
    return generators_bounds