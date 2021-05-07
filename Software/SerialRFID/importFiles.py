import xml.etree.ElementTree as ET
from variables import *
import sys

class ImportFiles:
    ''' Used ONLY to create the program JMRIImport.xml file.
    delete all items marked as import=yes then open JMRI OPS files /engines/cars/location and import a fresh copy.
    items marked as import=no will not be deleted. Uses CLASS Engines, Cars, Locations to prep new records.'''
    def __init__(self):
        try:
            global importRoot
            importTree = ET.parse('JMRIimport.xml')
            importRoot = importTree.getroot()
        except:
            print "something wrong with Import Class __init__"
            print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]   
            self.file_error()
          
        self.remove_last_import()                                                                                 # delete old import file
        
        self.myEngine = Engines()                                                                                # prep and add new engines
        engines = self.myEngine.read_engine_tags()
        set_import_engine_update(engines)
        serialEngines = self.myEngine.add_attributes_to_engine_tags(engines)
        for newEngine in serialEngines:
            add = importRoot.find('engines') 
            ET.SubElement(add, 'engine',newEngine)
        
        self.mycar = Cars()                                                                                             # prep and add new cars
        cars = self.mycar.read_car_tags()
        set_import_car_update(cars)
        serialCars = self.mycar.add_attributes_to_car_tags(cars)
        for newCar in serialCars:
            add = importRoot.find('cars') 
            ET.SubElement(add, 'car',newCar)
        
        self.myLocation = Locations()                                                                           # prep and add locations and tracks
        serialLocations = self.myLocation.read_loc_track_tags()
        for l in serialLocations:                                                                                       # add locations
            add = importRoot.find('locations') 
            ET.SubElement(add, 'location',l[0])
        
        for i in range ( len(serialLocations)):                                                                   # add tracks
            loc = serialLocations[i]
            base = loc[0]                                             # location dictionary
            sizeId = base.get('id')                                # location id
            trk = loc[1]
            for x in range (len(trk)):                            # list of track dictionary
                dictx = trk[x]                                         # individual track dictionary
                testId = dictx.get('id')                            # track id
                if len(sizeId) == 1:                                # determine size of location ID 1-9, 10-99, 100 - +++
                    match = testId[0]                              # extract location ID from track ID
                elif len(sizeId) == 2:
                    match = testId[0] + testId[1]
                elif len(sizeId) == 3:
                    match = testId[0] + testId[1] + testId[2]
                for child in importRoot.findall('locations'):
                    for t in child.findall('location'):
                        check = t.get('id', default='none')
                        if  str(check) == str(match):             # test that location and track ID match
                            ET.SubElement(t, 'track',dictx)    # add track to location
                                     
        self.pretty_print(importRoot)                           # create one line entries
        importTree.write("JMRIimport.xml")
        print "import completed"
        #with open('JMRIimport.xml', 'r') as f:
            #print(f.read())
        #f.close()
    def file_error(self):
        '''can't open engines file'''
        showMessageDialog('There is a problem trying to open.\n'
        'JMRIimport.xml',"File Error")
# ---------------------------------------------------------------------------------------------------------------------

    def remove_last_import(self):
        '''remove all child elements from locations/cars/engines  '''
        global importRoot
        for child in importRoot.findall("locations"):
            for profile in child.findall(".//location[@import='yes']"):
                child.remove(profile)
        
        for child in importRoot.findall("cars"):
            for profile in child.findall(".//car[@import='yes']"):
                child.remove(profile)
        
        for child in importRoot.findall("engines"):
            for profile in child.findall(".//engine[@import='yes']"):
                child.remove(profile)

        #print(ET.tostring(importRoot))

# ----------------------------------------------------------------------------------------------------------------
    def pretty_print(self, current, parent=None, index=-1, depth=0):
        ''' indents each child element and places it on its own line  '''
        for i, node in enumerate(current):
            #print "node = ", node
            self.pretty_print(node, current, i, depth + 1)
        if parent is not None:
            if index == 0:
                parent.text = '\n' + ('\t' * depth)
            else:
                parent[index - 1].tail = '\n' + ('\t' * depth)
            if index == len(parent) - 1:
                current.tail = '\n' + ('\t' * (depth - 1))
            
 # -----------------------------------------------------------------------------------------------------------------
            
    def save_import_xml_file(self):
        ''' permanently record changes for next session  '''
        importTree.write('JMRIimport.xml')
        print "file saved" 

# -----------------------------------------------------------------------------------------------------------------

class Engines:
    ''' Prep entries from OPS engine.xml file  '''
    def __init__(self):
        try:
            global engRoot
            engTree = ET.parse('OperationsEngineRoster.xml')
            engRoot = engTree.getroot()
            self.add_engine_rfid_tags()
            #engines = self.read_engine_tags()
            #serialEngines = self.add_attributes_to_engine_tags(engines)
        except:
            print "something wrong with Engine Class __init__"
            print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]   
            self.file_error()
    
    def file_error(self):
        '''can't open engines file'''
        showMessageDialog('There is a problem trying to open.\n'
        'OperationsEngineRoster.xml',"File Error")
        
    def read_engine_tags(self):
        ''' read in engine attributes as recorded in the JMRI OPS engine.xml file  '''
        engineList = []
        noSpaces = ""
        for elem in engRoot:
            for subelem in elem.findall('engine'):
                getEngineData = [0,1,2,3,4,5,6,7,8]    # using preset list index helped me to place data in a known order
                getEngineData[0] = subelem.get('rfid', default='none')
                getEngineData[1] = subelem.get('type', default='none')
                getEngineData[2] = subelem.get('model', default='none') # stored as color
                getEngineData[3] = subelem.get('roadName', default='none')
                getEngineData[4] = subelem.get('roadNumber', default='none')
                getEngineData[5] = subelem.get('owner', default='none')
                x = subelem.get('id', default='none')
                noSpaces = x.replace(" ", ".")  # used by engineGUI.py engine radio button event
                getEngineData[6] = noSpaces  # id with all spaces removed
                getEngineData[7] = subelem.get('locationId', default='none')
                getEngineData[8] = subelem.get('secLocationId', default='none')
                engineList.append(getEngineData)
        #set_jmri_engines(engineList)
        return engineList

    def add_engine_rfid_tags(self):
        ''' if JMRI file has no RFID tag recorded add a placeholder of 000000  '''
        for elem in engRoot:
            for subelem in elem.findall('engine'):
                exist = subelem.get('rfid', default='none')
                if str(exist) == 'none':
                    #print 'added tag'
                    subelem.set("rfid","111111")
  
    def add_attributes_to_engine_tags(self, JMRItags):
        ''' add attributes needed for SerialRFID to use  '''
        working = JMRItags   
        buildDict = {}
        addList = []
        for item in working:
            buildDict['rfid'] = str(item[0])
            buildDict['type'] = str(item[1])
            buildDict['color'] = str(item[2])  # used color as standard name in other code -- holds engine model
            buildDict['roadName'] = str(item[3])
            buildDict['roadNumber'] = str(item[4])
            buildDict['owner'] = str(item[5])
            buildDict['id'] = str(item[6])
            buildDict['location'] = str(item[7])       
            buildDict['secLocation'] = str(item[8])  
            buildDict['eng'] = "no"
            buildDict['imported'] = "yes"  
            buildDict['reader'] = "A"
            addList.append(buildDict)
            buildDict = {}
        return addList

# --------------------------------------------------------------------------------------------------------------------

class Cars:
    ''' Prep entries from OPS car.xml file  '''

    def __init__(self):
        try:
            global carTree
            global carRoot
            carTree = ET.parse('OperationsCarRoster.xml')
            carRoot = carTree.getroot()
            self.add_car_rfid_tags()
        except:
            print "something wrong with Cars Class __init__"
            print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]   
            self.file_error()
    
    def file_error(self):
        '''can't open engines file'''
        showMessageDialog('There is a problem trying to open.\n'
        'OperationsCarRoster.xml',"File Error")
    def read_car_tags(self):
        ''' read in car attributes as recorded in the JMRI OPS car.xml file  '''
        carList = []
        for elem in carRoot:
            for subelem in elem.findall('car'):
                getCarData = [0,1,2,3,4,5,6,7,8]    # using preset list index helped me to place data in a known order
                getCarData[0] = subelem.get('rfid', default='none')
                getCarData[1] = subelem.get('type', default='none')
                getCarData[2] = subelem.get('color', default='none')
                getCarData[3] = subelem.get('roadName', default='none')
                getCarData[4] = subelem.get('roadNumber', default='none')
                getCarData[5] = subelem.get('owner', default='none')
                getCarData[6] = subelem.get('id', default='none')
                getCarData[7] = subelem.get('locationId', default='none')
                getCarData[8] = subelem.get('secLocationId', default='none')
                carList.append(getCarData)
        return carList

    def add_car_rfid_tags(self):
        ''' if JMRI file has no RFID tag recorded add a placeholder of 000000  '''
        for elem in carRoot:
            for subelem in elem.findall('car'):
                exist = subelem.get('rfid', default='none')
                if str(exist) == 'none':
                    subelem.set("rfid","111111")
    
    def add_attributes_to_car_tags(self, JMRItags):
        ''' add attributes needed for SerialRFID to use  '''
        working = JMRItags   
        buildDict = {}
        addList = []
        for item in working:
            buildDict['rfid'] = str(item[0])
            buildDict['type'] = str(item[1])
            buildDict['color'] = str(item[2])
            buildDict['roadName'] = str(item[3])
            buildDict['roadNumber'] = str(item[4])
            buildDict['owner'] = str(item[5])
            buildDict['id'] = str(item[6])
            buildDict['location'] = str(item[7])       
            buildDict['secLocation'] = str(item[8])  
            buildDict['eng'] = "no"
            buildDict['imported'] = "yes" 
            buildDict['reader'] = "A" 
            addList.append(buildDict)
            buildDict = {}
        return addList               

# ----------------------------------------------------------------------------------------------------------------------

class Locations:
    ''' Prep entries from OPS location.xml file  '''

    def __init__(self):
        print "got to Locations class"
        try:
            global locTree
            global locRoot
            locTree = ET.parse('OperationsLocationRoster.xml')
            locRoot = locTree.getroot()
        except:
            print "something wrong with Locations Class __init__"
            print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]   
            self.file_error()
    
    def file_error(self):
        '''can't open engines file'''
        showMessageDialog('There is a problem trying to open.\n'
        'OperationsLocationRoster.xml',"File Error")
        
    def read_loc_track_tags(self):
        ''' read in location attributes as recorded in the JMRI OPS location.xml file 
        and add new SerialRFID attributes.'''
        locationList = []
        trackList = []
        for elem in locRoot:
            for subelem in elem.findall('location'):     
                getLocationData = {}                                                                               # temp dictionary for each location
                getLocationData['id']= subelem.get('id', default='none')
                getLocationData['name'] = subelem.get('name', default='none')
                getLocationData['saName'] = "A"
                getLocationData['reader'] = "A"
                getLocationData['imported'] = "yes"
                getLocationData['assigned'] = "no"
                getTrackData = {}                                                                                     # temp dictionary for each track
                for x in subelem.findall('track'):
                    getTrackData['id'] = x.get('id',  default='none')
                    getTrackData['name'] = x.get('name',  default='none')
                    getTrackData['saName'] = "A"
                    getTrackData['reader'] = "A"
                    getTrackData['imported'] = "yes"
                    getTrackData['assigned'] = "no"
                    trackList.append(getTrackData)                                                           # collect each track dictionary in a list
                    getTrackData = {}
                temp = []                                                                                                  
                temp.append(getLocationData)                                                                # temp[0] = location dictionary
                temp.append(trackList)                                                                            # temp[1] = list of track dictionaries
                trackList = []
                locationList.append(temp)                                                                       # [location dictionary, [trk dict, trk dict, trk dict] ]
        return locationList

# -----------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    myImport = Import()