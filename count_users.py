import xml.etree.cElementTree as ET
import pprint

def count_users():
    filename = "boston_massachusetts.osm"
    osm_file = open(filename, "r", 1)
    context = ET.iterparse(osm_file, events=("start", "end"))
    context = iter(context)
    users = set()
    for event, elem in context:
        if(event == "end"):
            tag = elem.tag
            if('user' in elem.attrib.keys()):
                user = elem.attrib['user']               
                if(user != None):
                    users.add(user)
    print len(users)    
    return users
if __name__ == '__main__':
    count_users()
