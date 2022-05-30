import os
from configparser import ConfigParser
curr_dir = os.path.dirname(os.path.abspath(__file__))
config_file = os.path.join(curr_dir, "database.ini")
def config(filename=config_file, section='postgresql'):
    # creation du parser
    parser = ConfigParser()
    # lecture du fchier de configuration
    parser.read(filename)

    # lecture de la section postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db