import xml.etree.ElementTree as ET
from variables import *
import sys
from JMRIlistAll import *
from importFiles import *
from basicImportedData import *
global tree
global root
def c_set_comm_port(portName):
        global tree
        global root
        try:
            for elem in root:
                for subelem in elem.findall('port'):
                       subelem.set("name", portName)
        except:
            print "port save to file failed"

def c_set_jmri_car_roster_path( pathName):
        global tree
        global root
        for elem in root:
            for subelem in elem.findall('file'):
                indentifier = str(subelem.get('name', default="None"))
                if indentifier == "cars":
                    subelem.set("path", str(pathName))

def c_set_jmri_location_roster_path( pathName):
        global tree
        global root
        print "path name = ", pathName
        for elem in root:
            for subelem in elem.findall('file'):
                indentifier = str(subelem.get('name', default="None"))
                if indentifier == "locations":
                    subelem.set("path", str(pathName) )    


def c_set_jmri_engine_roster_path( pathName):
        global tree
        global root
        for elem in root:
            for subelem in elem.findall('file'):
                indentifier = str(subelem.get('name', default="None"))
                if indentifier == "engines":
                    subelem.set("path", str(pathName) )    
                    
def open_config_file():
        try:
            global tree
            global root
            tree = ET.parse('RFIDconfig.xml')
            root = tree.getroot()
        except:
            print "no configuration file opened"
            print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]
            showMessageDialog('The program configuration file (RFIDconfig.xml)\ncon\'t be found or is corrupt. Open the configuration dialog\n and use it to fix the problem or close the program and\ngo find the file.\nPlace this file in the install directory.','Configuration Error')

def open_configuration():
        open_config_file()                                        
        c_get_mode()                                                 
        c_get_comm_port()
        c_get_jmri_car_roster_path()
        c_get_jmri_location_roster_path()
        c_get_jmri_engine_roster_path()
        
        basic_import_data()                                      # from JMRIimportedData.xml -- basicImportedData.py
        basic_get_installed_readers()
        basic_get_reader_assignments() 
        basic_get_available_reader()
        basic_read_loc_track_tags() 
        
        read_loc_track_tags()                                    # from JMRIimport.xml -- JMRIlistAll.py 
        read_engine_tags()                                         # from JMRIimport.xml -- JMRIlistAll.py 
        read_car_tags()                                              # from JMRIimport.xml -- JMRIlistAll.py 
                                 
        set_xmit_cmd("empty")                                 # to variable in variables.py
        
def c_get_jmri_car_roster_path():
    try:
        for elem in root:
            for subelem in elem.findall('file'):
                indentifier = str(subelem.get('name', default="None"))
                if indentifier == "cars":
                    path = subelem.get('path', default="NoPath")
                    global carPath
                    carPath = path
                    set_jmri_car_roster_path(carPath)
    except:
        print "get the jmri car roster path failed"
        print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]
        set_jmri_car_roster_path("unknown")

def c_get_jmri_location_roster_path():
    try:
        for elem in root:
            for subelem in elem.findall('file'):
                indentifier = str(subelem.get('name', default="None"))
                if indentifier == "locations":
                    path = subelem.get('path', default="NoPath")
                    global locationPath
                    locationPath = path
                    set_jmri_location_roster_path(locationPath)
    except:
        print "get the jmri location roster path failed"
        print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]
        set_jmri_location_roster_path("unknown")
    
def c_get_jmri_engine_roster_path():
    try:
        for elem in root:
            for subelem in elem.findall('file'):
                indentifier = str(subelem.get('name', default="None"))
                if indentifier == "engines":
                    path = subelem.get('path', default="NoPath")
                    global enginePath
                    enginePath = path
                    set_jmri_engine_roster_path(enginePath)
    except:
        print "c_get_jmri_engine_roster_path() failed"
        print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]
        set_jmri_engine_roster_path("unknown")
    
def c_get_mode():
    try:
        for elem in root:
            for subelem in elem.findall('op-mode'):
                currentMode = subelem.get('name', default="unknown")
                set_mode(currentMode)
    except:
        print "get mode failed"
        print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]
        set_mode("unknown")

def c_set_mode():
    try:
        for elem in root:
            for subelem in elem.findall('op-mode'):
                global currentMode
                currentMode = get_mode()
                subelem.set('name', currentMode )
                save_config_file()
    except:
        print "set mode failed"
        print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]
        set_mode("unknown")
    
def c_get_comm_port():
    try:
        for elem in root:
            for subelem in elem.findall('port'):
                portNumber =str(subelem.get('name', default="NoPort"))
                set_my_port_var(portNumber)
    except:
        print "config comm port failed"
        print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]
        set_my_port_var("unknown")
 
def save_config_file():
    global tree
    global root
    try:
        tree.write('RFIDconfig.xml')
    except:
        print "saving file failed"
        
def pretty_print(current, parent=None, index=-1, depth=0):
        ''' indents each child element and places it on its own line  '''
        for i, node in enumerate(current):
            pretty_print(node, current, i, depth + 1)
        if parent is not None:
            if index == 0:
                parent.text = '\n' + ('\t' * depth)
            else:
                parent[index - 1].tail = '\n' + ('\t' * depth)
            if index == len(parent) - 1:
                current.tail = '\n' + ('\t' * (depth - 1))
        #print(ET.tostring(root))
    
def set_rfid_attrib(currentCar, tagNumber):
    for elem in root:
        for subelem in elem.findall('car'):
            indentifier = str(subelem.get('id', default="None"))
            if indentifier == currentCar:
                subelem.set("rfid",tagNumber)
                return True  
    return False
   
if __name__ == '__main__':
        print 'running configRFIDXML'
        