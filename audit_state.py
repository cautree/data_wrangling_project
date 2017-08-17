filename = "boston_massachusetts.osm"
import xml.etree.cElementTree as ET
from collections import defaultdict


expected_state = ["MA"]


state_mapping = { "Ma": "MA",
            "ma": "MA",
            "MA- MASSACHUSETTS": "MA",
            "Arlington. MA": "Arlington",
            "MASSACHUSETTS": "MA",
            "Massachusetts": "MA"            
            }



def print_sorted_dict(d):
    keys = d.keys()
    keys = sorted(keys, key=lambda s: s.lower())
    for k in keys:
        v = d[k]
        print "%s: %d" % (k, v) 



def audit_state(unexpected, state): 
    cities = defaultdict(int)
      
    cities[state] += 1
    if state not in expected_state:
            unexpected[state]+=1
    return unexpected


def is_state_name(elem):
    return (elem.tag == "tag") and (elem.attrib['k'] == "addr:state")

def audit():
    unexpected = defaultdict(int) 
    for event, elem in ET.iterparse(filename):
        if is_state_name(elem):
            audit_state(unexpected, elem.attrib['v'])    
    print_sorted_dict(unexpected) 
    return unexpected

def update_name(name, mapping):
    if name in state_mapping.keys():
        name = state_mapping[name]
    print name
        
    return name

if __name__ == '__main__':
    audit()
