import configparser
indicator = [1,3,4,6,7]
def create_config(indicator):
    config = configparser.ConfigParser()
    config.read('./NEAT-Try/XOR-conf')
    print("Loading config!")
    config['DefaultGenome']['num_inputs'] = str(len(indicator))
    config.add_section('Inputs')
    config.set('Inputs','Indicators', str(indicator))
    with open('temp.conf','w') as f:
        config.write(f)
    print("Temp config created!")

create_config(indicator)