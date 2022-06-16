# -*- coding: utf-8 -*-
"""
Simple set of utilites for reading the config file

"""

import configparser
import os
import gmag

from pathlib import Path

def get_config_file():
    """Return location of configuration file

    In order
    1. ~/.magpy/gmagrc
    2. The installation folder of gmag

    Returns
    -------
    loc : string
        File path of the gmagrc configuration file

    References
    ----------
    modeled completely from helipy/util/config.py
    """
    config_filename = 'gmagrc'

    # Get user configuration location
    home_dir = Path.home()
    config_file_1 = home_dir / 'gmagrc' / config_filename

    module_dir = Path(gmag.__file__)
    config_file_2 = module_dir / '..' / config_filename
    config_file_2 = config_file_2.resolve()

    for f in [config_file_1, config_file_2]:
        if f.is_file():
            return str(f)    




def load_config():
    """Read in configuration file neccessary for downloading and
    loading data.

    Returns
    -------
    config_dic : dict
        Dictionf containing all options from configuration file.
    """
    
    config_path = get_config_file()
    configf = configparser.ConfigParser()
    configf.read(config_path)
    
    config_dic = {}

    data_dir = os.path.expanduser(configf['DEFAULT']['data_dir'])

    #modify directory for windows
    if os.name == 'nt':
        data_dir = data_dir.replace('/', '\\')
    config_dic['data_dir'] = data_dir

    # Create data directory if not created
    if not os.path.isdir(data_dir):
        print('Creating data directory {}'.format(data_dir))
        os.makedirs(data_dir)
    
    # Read in configuration setting for downloading
    # data set
    # Carisma download address
    if configf['DEFAULT']['ca_http']:
        config_dic['ca_http'] = configf['DEFAULT']['ca_http']
    else:
        config_dic['ca_http'] = None
    # IMAGE download address
    if configf['DEFAULT']['im_http']:
        config_dic['im_http'] = configf['DEFAULT']['im_http']
    else:
        config_dic['im_http'] = None
    # THEMIS download address
    if configf['DEFAULT']['th_http']:
        config_dic['th_http'] = configf['DEFAULT']['th_http']
    else:
        config_dic['th_http'] = None
    return config_dic


