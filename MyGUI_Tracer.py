import os
import json
import xml.etree.ElementTree as ET
import glob
from shutil import copyfile

START_DIR = os.getcwd()
stringTable = {}
lastType = ""

def UpdateList(start, child, jsonData):
    global stringTable
    global lastType
    final = jsonData
    final1 = start.attrib.copy()
    for i in start.attrib:
        if not type(final1[i]) == list:
            final1[i] = []
        if not type(start.attrib[i]) == list:
            if i == "type":
                lastType = start.attrib[i]
                if not lastType in stringTable:
                    stringTable[lastType] = {}
                if not start.attrib[i] in final1[i]:
                    final1[i].append(start.attrib[i])
            elif str(i) in [ "position_real", "position" ]:
                if not "Float, Float, Float, Float" in final1[i]:
                    final1[i].append("Float, Float, Float, Float")
            elif not start.attrib[i] in final1[i]:
                final1[i].append(start.attrib[i])
        else:
            final1[i].append(start.attrib[i])
    if not str(start.tag) in final:
        final[str(start.tag)] = { }
    if not lastType in final[str(start.tag)]:
        final[str(start.tag)][lastType] =  { "Properties": final1 }
    key = ""
    value = ""
    isKey = False
    for i in child.attrib:
        if i == "key":
            key = str(child.attrib[i])
            if not key in stringTable[lastType]:
                stringTable[lastType][key] = {"String": []}
            isKey = True
        else:
            value = str(child.attrib[i])
            isKey = False
        numberTest = value.replace(".", "").replace(" ", "")
        if not isKey:
            if len(value) > 0:
                if not key in final[str(start.tag)][lastType]:
                        final[str(start.tag)][lastType][key] = []
                if value in ["true", "false", "True", "False"]:
                    if not "Bool" in final[str(start.tag)][lastType][key]:
                        final[str(start.tag)][lastType][key].append("Bool")
                elif numberTest.isdigit() or numberTest.isdecimal():
                    vSplit = value.split(" ")
                    numberOfFloat = len(vSplit)
                    retNum = ""
                    for i in range(numberOfFloat):
                        if vSplit[i].isdigit():
                            retNum += "Int"
                        else:
                            retNum += "Float"
                        if not i == numberOfFloat-1:
                            retNum += ", "
                    if not retNum in final[str(start.tag)][lastType][key]:
                        final[str(start.tag)][lastType][key].append(retNum)
                elif value.endswith(".png"):
                    if not "Image.png" in final[str(start.tag)][lastType][key]:
                        final[str(start.tag)][lastType][key].append("Image.png")
                elif value.endswith(".jpg"):
                    if not "Image.jpg" in final[str(start.tag)][lastType][key]:
                        final[str(start.tag)][lastType][key].append("Image.jpg")
                else:
                    if not stringTable[lastType][key] in final[str(start.tag)][lastType][key]:
                        final[str(start.tag)][lastType][key].append(stringTable[lastType][key])
                    indexV = final[str(start.tag)][lastType][key].index(stringTable[lastType][key])
                    if not value in final[str(start.tag)][lastType][key][indexV]["String"]:
                        final[str(start.tag)][lastType][key][indexV]["String"].append(value)
                    stringTable[lastType][key] = final[str(start.tag)][lastType][key][indexV]
    return final

def GetChildren(start, jsonData):
    for child in start:
        info = { str(child.tag): child.attrib }
        if not child.tag == "Widget":
            for item in child.attrib:
                jsonData = UpdateList(start, child, jsonData)
    for child in start:
        if child.tag == "Widget":
            jsonData = GetChildren(child, jsonData)
    return jsonData

def OutPutFiles(startDir, jsonData):
    for path in os.listdir(startDir):
        if path.endswith(".layout"):
            tree = ET.parse(startDir + "\\" + path)
            root = tree.getroot()
            jsonData = GetChildren(root, jsonData)
            originalFile = startDir + "\\" + path
            directory = START_DIR + "\\MyGUI_Tracer" + startDir.replace(START_DIR+"\\Gui", "") + "\\" + path.split(".")[0]
    return jsonData

def GetDirectories(startDir, jsonData):
    for directory in [f.path for f in os.scandir(startDir) if f.is_dir()]:
        d = START_DIR + "\\MyGUI_Tracer" + directory.replace(START_DIR + "\\Gui", "")
        jsonData = OutPutFiles(directory, jsonData)
        jsonData = GetDirectories(directory, jsonData)
    return jsonData

if not os.path.isdir(START_DIR + "\\MyGUI_Tracer"):
    os.mkdir(START_DIR + "\\MyGUI_Tracer")
    
jsonData = GetDirectories(START_DIR + "\\Gui", {'MyGUI': {'type': 'Layout', 'version': '3.2.0'}})

with open(START_DIR + "\\MyGUI_Tracer\\MyGUI_Trace.json", "w" ) as outfile:
    outfile.write(json.dumps(jsonData, indent=4))
    

