#! /usr/bin/env python3
#
# Molecule forces us to use old PyYAMl ...
# requires workaround to fix indention for yamlint

import sys
from ruamel.yaml import YAML
import requests

with open('../defaults/main.yml','r') as inp:
    yaml = YAML(typ='safe')
    url = yaml.load(inp)['grid_voinfo_url']

data = requests.get(url).json()

voinfo={}
for vo in data['voVoms']:
    name = vo['name']
    voinfo[name] = []
    for voms in vo['Vo']:
        try:
            voms_server = voms['VoVomsServer'][0]['VoVomsServer'][2]
        except IndexError:
            continue
        voinfo[name].append({
          'dn' : voms_server['X509Cert'][0]['DN'][0],
          'ca_dn' : voms_server['X509Cert'][1]['CA_DN'][0],
          'hostname' : voms_server['host'],
          'port' : int(voms['VoVomsServer'][0]['vomses_port'])
        })

with open('voinfo.yml','w') as out:
    yaml = YAML()
    yaml.indent(mapping=2, sequence=4, offset=2)
    yaml.explicit_start = True
    yaml.dump(voinfo,out)
