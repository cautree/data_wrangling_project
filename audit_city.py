filename = "boston_massachusetts.osm"
import xml.etree.cElementTree as ET
from collections import defaultdict


expected_cities = ["Allston", "Arlington", "Belmont", "Boston", "Braintree", "Brighton", 
            "Brookline", "Cambridge", "Charlestown", 
            "Chelsea", "Chestnut Hill", "Dedham",
            "Dorchester","East Boston","Everett","Hingham","Hyde Park","Jamaica Plain","Malden",
           "Mattapan","Medford","Milton","Newton","Quincy","Revere",
           "Roslindale","Roxbury Crossing","Somerville","South Boston",
           "Watertown","West Roxbury","Weymouth","Winthrop"]


city_mapping = { ", Arlington, MA": "Arlington",
            "2067 Massachusetts Avenue": "Cambridge",
            "Arlington, MA": "Arlington",
            "Arlington. MA": "Arlington",
            "Belmont, MA": "Belmont",
            "BOSTON": "Boston",
            "boston": "Boston",
            "dedham":"Dedham",
            "Boston, MA": "Boston",
            "Brookline, MA": "Brookline",            
            "Cambridge, MA": "Cambridge",
            "Cambridge, Massachusetts": "Cambridge",
            "Newton Centre": "Newton",
            "somerville": "Somerville",
            "Roxbury": "Roxbury Crossing",
            "South End": "South Boston",
            "Watertown, MA": "Watertown",
            "winthrop": "Winthrop"            
            }



def print_sorted_dict(d):
    keys = d.keys()
    keys = sorted(keys, key=lambda s: s.lower())
    for k in keys:
        v = d[k]
        print "%s: %d" % (k, v) 



def audit_city(unexpected, city): 
    cities = defaultdict(int)
      
    cities[city] += 1
    if city not in expected_cities:
            unexpected[city]+=1
    return unexpected


def is_city_name(elem):
    return (elem.tag == "tag") and (elem.attrib['k'] == "addr:city")

def audit():
    unexpected = defaultdict(int) 
    for event, elem in ET.iterparse(filename):
        if is_city_name(elem):
            audit_city(unexpected, elem.attrib['v'])    
    print_sorted_dict(unexpected) 
    return unexpected

def update_name(name, mapping):
    if name in city_mapping.keys():
        name = city_mapping[name]
    print name
        
    return name

if __name__ == '__main__':
    audit()
