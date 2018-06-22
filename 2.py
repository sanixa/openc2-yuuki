import subprocess
import os
import json
import types
import re
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from xml2dic import XmlDictConfig


def main():
    tree = ET.ElementTree(file='add_group.xml')
    for elem in tree.iter():
        elem.tag = elem.tag[32:]
        if isinstance(elem.tag,str):
            elem.tag = elem.tag.decode('utf-8')
        if isinstance(elem.text,str):
            elem.text = elem.text.decode('utf-8')
    root = tree.getroot()
    xmldict = XmlDictConfig(root)
    print xmldict

    group = os.popen('ovs-ofctl dump-groups s1 -O Openflow13').read() #"ovs-ofctl dump-groups s1 -O Openflow13"
    if group.find("group_id") == -1:
        return "",0
    group = group[group.find("group_id"):]
    group = group[:len(group)-1]
    group = group.replace("watch_port:", "watch_port=")
    group = group.replace("watch_group:", "watch_group=")
    group = group.replace("\n", "")
    group = re.split(r", | |,", group)
    group_table = {}
    single_group = {}
    count = 0       # group#
    for elem in group:
        temp = elem.split("=")
        if temp[0] == "group_id" and single_group != {}:
            group_table.update({count:single_group})
            count += 1
            single_group = {temp[0]:temp[1]}
        else:
            single_group.update({temp[0]:temp[1]})
    group_table.update({count:single_group})
    #print group_table,count

    gid = -1
    for i in range(count):
        if group_table[i]['group_id'] == xmldict['group-id']:
            gid = i

    result = "correct"
    try:
        gtype = xmldict['group-type']
    except KeyError:
        pass
    else:
        gtype = gtype[6:]
        if gtype != group_table[gid]['type']:
            result = "error"
    try:
        action = xmldict['buckets']['bucket']['action']['pop-vlan-action']
    except KeyError:
        pass
    else:
        if  "pop_vlan" != group_table[gid]['actions']:
            result = "error"
    print result
if __name__ == "__main__":

    main()

