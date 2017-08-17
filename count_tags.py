import xml.etree.cElementTree as ET
import pprint

def count_tags():
    filename = "boston_massachusetts.osm"
    osm_file = open(filename, "r", 1)  # q for buffering = 1
    context = ET.iterparse(osm_file, events=("start", "end"))
    # turn it into an iterator
    context = iter(context)
    event, root = context.next()
    
    tags = {}
    for event, elem in context: 
        if(event == "end"):
            tag = elem.tag        
            if(tag in tags.keys()):
                tags[tag] += 1   # increment by 1 if already in the tags dic
            else:
                tags[tag] = 1    # if not in the tag dic, put into the tag
            root.clear()
    pprint.pprint(tags)
    
if __name__ == '__main__':
    count_tags()
