#!/usr/bin/env python

# parse Illumina HiSeq 2000 run parameters for
# ISAtab

from lxml import etree
import sys
import collections

# parse RunInfo.xml
doc1 = etree.parse(sys.argv[1])

# parse DemultiplexConfig.xml
doc2 = etree.parse(sys.argv[2])

root1 = doc1.getroot()
root2 = doc2.getroot()
illumina_run = collections.OrderedDict()

for child in root1[0]:
    if child.tag == "Flowcell":
        illumina_run["Flowcell"] = child.text
    if child.tag == "Date":
        illumina_run["Date"] = child.text
    if child.tag == "Instrument":
        illumina_run["Instrument"] = child.text

for element in root2.iter():
    if element.tag == "Software":
        software_name = element.attrib["Name"]
        if software_name not in illumina_run:
            illumina_run[software_name] = element.attrib["Version"]
        elif illumina_run[software_name] == element.attrib["Version"]:
            print(software_name + " software with same version found twice")
        elif illumina_run[software_name] != element.attrib["Version"]:
            print(software_name + " software found twice with two different versions")
            
headers = "\t".join(illumina_run.keys()) + "\n"
run_values = "\t".join(illumina_run.values())
f = open('illumina_run4isa.txt', 'w')
f.write(headers)
f.write(run_values)
f.close()

