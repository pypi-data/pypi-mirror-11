import imp
import os.path


__version__ = '0.2.6'


BALANCING_AUTHORITIES = {
    'BPA': {'module': 'bpa', 'class': 'BPAClient'},
    'CAISO': {'module': 'caiso', 'class': 'CAISOClient'},
    'ERCOT': {'module': 'ercot', 'class': 'ERCOTClient'},
    'ISONE': {'module': 'isone', 'class': 'ISONEClient'},
    'MISO': {'module': 'miso', 'class': 'MISOClient'},
    'NEVP': {'module': 'nvenergy', 'class': 'NVEnergyClient'},
    'NYISO': {'module': 'nyiso', 'class': 'NYISOClient'},
    'PJM': {'module': 'pjm', 'class': 'PJMClient'},
    'SPPC': {'module': 'nvenergy', 'class': 'NVEnergyClient'},
    'SPP': {'module': 'spp', 'class': 'SPPClient'},
}


def client_factory(client_name, **kwargs):
    """Return a client for an external data set"""
    # set up
    dir_name = os.path.dirname(os.path.abspath(__file__))
    error_msg = 'No client found for name %s' % client_name
    client_key = client_name.upper()

    # find client
    try:
        client_vals = BALANCING_AUTHORITIES[client_key]
        module_name = client_vals['module']
        class_name = client_vals['class']
    except KeyError:
        raise ValueError(error_msg)

    # find module
    try:
        fp, pathname, description = imp.find_module(module_name, [dir_name])
    except ImportError:
        raise ValueError(error_msg)

    # load
    try:
        mod = imp.load_module(module_name, fp, pathname, description)
    finally:
        # Since we may exit via an exception, close fp explicitly.
        if fp:
            fp.close()

    # instantiate class
    try:
        client_inst = getattr(mod, class_name)(**kwargs)
    except AttributeError:
        raise ValueError(error_msg)

    # set name
    client_inst.NAME = client_name

    return client_inst
