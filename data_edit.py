#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
import audit
import audit_city
import audit_zip
import audit_state
import audit_country
"""
Transforms the downloaded OSM xml data into a JSON file.

Your task is to wrangle the data and transform the shape of the data
into the model we mentioned earlier. The output should be a list of dictionaries
that look like this:

{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}

You have to complete the function 'shape_element'.
We have provided a function that will parse the map file, and call the function with the element
as an argument. You should return a dictionary, containing the shaped data for that element.
We have also provided a way to save the data in a file, so that you could use
mongoimport later on to import the shaped data into MongoDB. 

Note that in this exercise we do not use the 'update street name' procedures
you worked on in the previous exercise. If you are using this code in your final
project, you are strongly encouraged to use the code from previous exercise to 
update the street names before you save them to JSON. 

In particular the following things should be done:
- you should process only 2 types of top level tags: "node" and "way"
- all attributes of "node" and "way" should be turned into regular key/value pairs, except:
    - attributes in the CREATED array should be added under a key "created"
    - attributes for latitude and longitude should be added to a "pos" array,
      for use in geospacial indexing. Make sure the values inside "pos" array are floats
      and not strings. 
- if the second level tag "k" value contains problematic characters, it should be ignored
- if the second level tag "k" value starts with "addr:", it should be added to a dictionary "address"
- if the second level tag "k" value does not start with "addr:", but contains ":", you can
  process it in a way that you feel is best. For example, you might split it into a two-level
  dictionary like with "addr:", or otherwise convert the ":" to create a valid key.
- if there is a second ":" that separates the type/direction of a street,
  the tag should be ignored, for example:

<tag k="addr:housenumber" v="5158"/>
<tag k="addr:street" v="North Lincoln Avenue"/>
<tag k="addr:street:name" v="Lincoln"/>
<tag k="addr:street:prefix" v="North"/>
<tag k="addr:street:type" v="Avenue"/>
<tag k="amenity" v="pharmacy"/>

  should be turned into:

{...
"address": {
    "housenumber": 5158,
    "street": "North Lincoln Avenue"
}
"amenity": "pharmacy",
...
}

- for "way" specifically:

  <nd ref="305896090"/>
  <nd ref="1719825889"/>

should be turned into
"node_refs": ["305896090", "1719825889"]
"""


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]



street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

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
            "street." :"street"
            }


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

zip_mapping = { 
            "MA 02118":"02118",
            "MA":"N/A",            
            "MA 02186" : "02186",            
            "MA 02116" :"02116",
            "0239" :"02139"           
            }

state_mapping = { "Ma": "MA",
            "ma": "MA",
            "MA- MASSACHUSETTS": "MA",
            "Arlington. MA": "Arlington",
            "MASSACHUSETTS": "MA",
            "Massachusetts": "MA"            
            }


country_mapping = { "USA": "US"            
            }


def shape_element(element):
    node = {"created":{}, "address": {}, "tags": {}}

    if element.tag == "node" or element.tag == "way" :
        node["type"] = element.tag

        # Parse element attributes
        attributes = element.attrib
        lat = 0.0
        lon = 0.0
        for attribute in attributes.keys():
            value = attributes[attribute]

            if(attribute in CREATED):
                node["created"][attribute] = value
            elif(attribute == "lat"):
                lat = float(value)
            elif(attribute == "lon"):
                lon = float(value)
            else:
                node[attribute] = value

        if(lat != 0.0 and lon != 0.0):
            node["pos"] = [lat, lon]

        # Parse child elements of "Node" and "Way" elements
        childtags = element.findall('tag')
        if(len(childtags) > 0):


            for childtag in childtags:
                if not(('k' in childtag.attrib.keys()) and ('v' in childtag.attrib.keys())):
                    continue

                k = childtag.attrib['k']
                v = childtag.attrib['v']

                if(re.match(problemchars, k) != None):
                    continue

                if(k.startswith('addr:')):
                    spl = k.split(':')
                    if(len(spl) > 2):
                        continue
                    attrname = spl[1]
                    print attrname
                    if attrname == 'street':
                        # print v
                        # print audit.update_name(v,street_mapping)
                        node["address"][attrname] = audit.update_name(v,street_mapping)
                    elif attrname == 'city':                        
                        # print v
                        # print audit_city.update_name(v,city_mapping)
                        node["address"][attrname] = audit_city.update_name(v,city_mapping)
                    elif attrname == 'postcode':                        
                        # print v
                        # print audit_zip.update_zipcode(v,zip_mapping)
                        node["address"][attrname] = audit_zip.update_zipcode(v,zip_mapping)
                    elif attrname == 'state':                        
                        # print v
                        # print audit_state.update_name(v,state_mapping)
                        node["address"][attrname] = audit_state.update_name(v,state_mapping)

                    elif attrname == 'country':                        
                        # print v
                        # print audit_country.update_name(v,country_mapping)
                        node["address"][attrname] = audit_country.update_name(v,country_mapping)
                    else:          
                        node["address"][attrname] = v
                else:
                    node["tags"][k] = v

        # Parse child noderef elements
        noderefs = element.findall('nd')
        if(len(noderefs) > 0):
            node["node_refs"] = []
            for nr in noderefs:
                if 'ref' in nr.attrib.keys():
                    node["node_refs"].append(nr.attrib['ref'])

        # Remove address and/or tags from node if they are empty
        if len(node["address"]) == 0:
            del(node["address"])
        if len(node["tags"]) == 0:
            del(node["tags"])

        return node
    else:
        return None


def process_map(file_in, pretty = False):
    file_out = "{0}.json".format(file_in[:-4])
    data = []
    with codecs.open(file_out, "w") as fo:
        context = ET.iterparse(file_in, events=("start", "end"))
        for event, element in context:
            if event == "end":
                el = shape_element(element)
                if el:
                    data.append(el)
                    if pretty:
                        fo.write(json.dumps(el, indent=2)+"\n")
                    else:
                        fo.write(json.dumps(el) + "\n")

                if element.tag == "node" or element.tag == "way":
                    element.clear()
    return data


def main():
    #process_map("data.xml")
    #boston_massachusetts.osm
    process_map("boston_massachusetts.osm")

if __name__ == "__main__":
    main()
