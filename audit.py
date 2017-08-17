import xml.etree.cElementTree as ET
import re
import pprint
from collections import defaultdict



OSMFILE = "boston_massachusetts.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


street_expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons","Terrace", "Way","Center","Park","Circle","Highway","Row"]

street_mapping = { 
            "Ave.":"Avenue",
            "Ave":"Avenue",            
            "Driveway" : "Drive",            
            "HIghway" :"Highway",
            "Hwy" :"Highway",
            "Pkwy" : "Parkway",            
            "Sq." :"Square",            
            "St," :"Street",
            "St." :"Street",           
            "Street." :"Street",
            "street":"Street",
            "St" :"Street",
            'Rd':"Road",
            'rd.':'Road'
            }


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m is not None:
        street_type = m.group()
        if street_type not in street_expected:
            street_types[street_type].add(street_name)

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types


def update_name(name, street_mapping):
    if street_type_re.search(name) is not None:
        m = street_type_re.search(name).group()
        #print m        
        if m in street_mapping.keys():
            name = street_type_re.sub(street_mapping[m], name)            
            #print name        
    return name



def test():
    st_types = audit(OSMFILE)
    
    pprint.pprint(dict(st_types))
    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, street_mapping)
            print name, "=>", better_name
            

if __name__ == '__main__':
    test()
