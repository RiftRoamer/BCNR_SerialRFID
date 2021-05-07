''' This module used to display ready only lists from JMRI files when using JMRI mode
AND to update JMRI file rfid tags'''

import xml.etree.ElementTree as ET
from variables import *
global locTree
def read_loc_track_tags():
    #print "got to Locations listAll"
    locFile = get_jmri_location_roster_path()
    global locTree
    locTree = ET.parse(locFile)
    locRoot = locTree.getroot()
    locationList = []
    trackList = []
    for elem in locRoot:
        for subelem in elem.findall('location'):
            getLocationData = {}
            getLocationData['id']= subelem.get('id', default='None')
            getLocationData['name'] = subelem.get('name', default='None')
            getTrackData = {}
            for x in subelem.findall('track'):
                getTrackData['id'] = x.get('id',  default='None')
                getTrackData['name'] = x.get('name', default='None')
                trackList.append(getTrackData)
                getTrackData = {}
            temp = []
            temp.append(getLocationData)
            temp.append(trackList)
            trackList = []
            locationList.append(temp)
    set_jmri_loc_track_tags(locationList)

# -----------------------------------------------------------------------------------------------------------------------------------

def read_engine_tags():
        global engRoot
        global engTree
        engFile = get_jmri_engine_roster_path()
        engTree = ET.parse(engFile)
        engRoot = engTree.getroot()
        add_engine_rfid_tags()
        engineList = []
        noSpaces = ""
        for elem in engRoot:
            for subelem in elem.findall('engine'):
                getEngineData = [0,1,2,3,4,5,6,7]    # using preset list index helped me to place data in a known order
                getEngineData[0] = subelem.get('rfid', default='None')
                getEngineData[1] = subelem.get('type', default='None')
                getEngineData[2] = subelem.get('model', default='None')
                getEngineData[3] = subelem.get('roadName', default='None')
                getEngineData[4] = subelem.get('roadNumber', default='None')
                getEngineData[5] = subelem.get('owner', default='None')
                x = subelem.get('id', default='None')
                noSpaces = x.replace(" ", ".")  # used by engineGUI.py engine radio button event
                getEngineData[6] = noSpaces  # id with all spaces removed
                getEngineData[7] = subelem.get('locationId', default='None')
                engineList.append(getEngineData)
        set_jmri_engines(engineList)

def add_engine_rfid_tags():
        global engRoot
        global engTree
        for elem in engRoot:
            for subelem in elem.findall('engine'):
                exist = subelem.get('rfid', default='None')
                if str(exist) == 'None':
                    subelem.set("rfid","111111")

def update_engine_rfid_tags(engine, tag):
        ''' record new rfid tag value for JMRI file'''
        global engRoot
        global engTree
        for elem in engRoot:
            for subelem in elem.findall('engine'):
                exist = subelem.get('id', default='None')
                if str(exist) == engine:
                    subelem.set("rfid",str(tag))

def save_engine_xml_file():
        ''' save to JMRI Ops file'''
        global engRoot
        global engTree
        engFile = get_jmri_engine_roster_path()
        engTree.write(engFile)
        read_engine_tags()
        print "engine file saved"                     
                    
# ----------------------------------------------------------------------------------------------------------------------------------------

def read_car_tags():
        global carRoot
        global carTree
        carFile = get_jmri_car_roster_path()
        carTree = ET.parse(carFile)
        carRoot = carTree.getroot()
        add_car_rfid_tags()

        carList = []
        for elem in carRoot:
            for subelem in elem.findall('car'):
                getCarData = [0,1,2,3,4,5,6,7]    # using preset list index helped me to place data in a known order
                getCarData[0] = subelem.get('rfid', default='None')
                getCarData[1] = subelem.get('type', default='None')
                getCarData[2] = subelem.get('color', default='None')
                getCarData[3] = subelem.get('roadName', default='None')
                getCarData[4] = subelem.get('roadNumber', default='None')
                getCarData[5] = subelem.get('owner', default='None')
                getCarData[6] = subelem.get('id', default='None')
                getCarData[7] = subelem.get('locationId', default='None')
                carList.append(getCarData)
        set_jmri_cars(carList)

def add_car_rfid_tags():
        global carRoot
        global carTree
        for elem in carRoot:
            for subelem in elem.findall('car'):
                exist = subelem.get('rfid', default='None')
                if str(exist) == 'None':
                    subelem.set("rfid","000000")
                    #print 'added tag'

def update_car_rfid_tags(saveCar, tag):
        ''' record new rfid tag value for JMRI file'''
        global carRoot
        global carTree
        for elem in carRoot:
            for subelem in elem.findall('car'):
                exist = subelem.get('id', default='None')
                if str(exist) == saveCar:
                    subelem.set("rfid",str(tag))

def save_car_xml_file():
        ''' save to JMRI Ops file'''
        global carRoot
        global carTree
        carFile = get_jmri_car_roster_path()
        carTree.write(carFile)
        read_car_tags()
        print "car file saved"      



if __name__ == '__main__':
        print 'running JMRIlistAll.py'
        #read_engine_tags()
        update_engine_rfid_tags("MILW1", "123456")
        save_engine_xml_file()
        #read_engine_tags()