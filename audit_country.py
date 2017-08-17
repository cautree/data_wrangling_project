filename = "boston_massachusetts.osm"
import xml.etree.cElementTree as ET
from collections import defaultdict


expected_country = ["US"]


country_mapping = { "USA": "US"      
            }



def print_sorted_dict(d):
    keys = d.keys()
    keys = sorted(keys, key=lambda s: s.lower())
    for k in keys:
        v = d[k]
        print "%s: %d" % (k, v) 


def audit_country(unexpected, country):     
    if country not in expected_country:
            unexpected[country]+=1
    return unexpected


def is_country_name(elem):
    return (elem.tag == "tag") and (elem.attrib['k'] == "addr:country")

def audit():
    unexpected = defaultdict(int) 
    for event, elem in ET.iterparse(filename):
        if is_country_name(elem):
            audit_country(unexpected, elem.attrib['v'])    
    print_sorted_dict(unexpected) 
    return unexpected

def update_name(name, mapping):
    if name in country_mapping.keys():
        name = country_mapping[name]
    print name
        
    return name

if __name__ == '__main__':
    audit()
