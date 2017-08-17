filename = "boston_massachusetts.osm"
import xml.etree.cElementTree as ET
import re
import pprint
from collections import defaultdict


zip_mapping = { 
            "MA 02118":"02118",
            "MA":"N/A",            
            "MA 02186" : "02186",            
            "MA 02116" :"02116",
            "0239" :"02139"           
            }


def audit_zip(postcode):
    unexpected = []
    if not bool(re.match('^[0-9]{5}(?:-[0-9]{4})?$',postcode)):
        unexpected.append(postcode)
    
    if len(unexpected)>0:
        print unexpected


def is_zipcode(elem):
    return (elem.tag == "tag") and (elem.attrib['k'] == "addr:postcode")

def audit():
    for event, elem in ET.iterparse(filename):
        if is_zipcode(elem):
            audit_zip(elem.attrib['v'])    
    

def update_zipcode(zipcode, zip_mapping):
    
    if zipcode in zip_mapping.keys():
        zipcode = zip_mapping[zipcode]    
    print zipcode        
    return zipcode



if __name__ == '__main__':
    audit()
