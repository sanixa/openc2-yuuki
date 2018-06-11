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
    tree = ET.ElementTree(file='add.xml')
    for elem in tree.iter():
        elem.tag = elem.tag[31:]
        if isinstance(elem.tag,str):
            elem.tag = elem.tag.decode('utf-8')
        if isinstance(elem.text,str):
            elem.text = elem.text.decode('utf-8')
    root = tree.getroot()
    xmldict = XmlDictConfig(root)  # xml to dict
    #print xmldict
    flow = os.popen("ovs-ofctl dump-flows s1").read()
    flow = flow[flow.find("cookie"):]
    flow = flow[:len(flow)-1]
    flow = flow.replace("\n",",")
    flow = flow.replace(",ip,",",")
    flow = re.split(r", | |,", flow)
    flow_table = {}
    single_flow = {}
    count = 0       # flow#
    for elem in flow:
        temp = elem.split("=")
        if temp[0] == "actions":
            single_flow.update({temp[0]:temp[1]})
            flow_table.update({count:single_flow})
            count += 1
            single_flow = {}
        else:
            single_flow.update({temp[0]:temp[1]})
    #print flow_table
    #print xmldict
    #for i in range(count):
    #    print flow_table[i]
    fid = -1         
    for i in range(count):
        temp_l = []
        flow_l = [flow_table[i]['cookie'],flow_table[i]['priority'],flow_table[i]['table']]
        if 'cookie' in xmldict:
            temp_l.append(hex(int(xmldict['cookie'])))
        else:
            temp_l.append(hex(0))
        if 'priority' in xmldict:
            temp_l.append(xmldict['priority'])
        else:
            temp_l.append(int(0))
        if 'table_id' in xmldict:
            temp_l.append(xmldict['table_id'])
        else:
            temp_l.append(int(0))
        if temp_l == flow_l:
            fid = i
        #print temp_l
        #print flow_l
        temp_l = []
    #print fid

    result = "correct"
    action = xmldict['instructions']['instruction']['apply-actions']['action']['output-action']['output-node-connector']
    #print action
    if 'dl_src' in xmldict:
        if xmldict['dl_src'] != flow_table[fid]['dl_src']:
            result = "error"
    if 'dl_dst' in xmldict:
        if xmldict['dl_dst'] != flow_table[fid]['dl_dst']:
            result = "error"
    if 'nw_src' in xmldict:
        if xmldict['nw_src'] != flow_table[fid]['nw_src']:
            result = "error"
    if 'nw_dst' in xmldict:
        if xmldict['nw_dst'] != flow_table[fid]['nw_dst']:
            result = "error"
    try:
        i = int(action)
    except ValueError:
        if action == "INPORT":
            if flow_table[fid]['actions'] != "IN_PORT":
                result = "error"
        else:
           if flow_table[fid]['actions'] != action:
                result = "error"
    else:
        if flow_table[fid]['actions'] != "output:" + str(i):
            print flow_table[fid]['actions']
            result = "error"

    print result

if __name__ == "__main__":

    main()

