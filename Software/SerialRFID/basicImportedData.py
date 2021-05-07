import xml.etree.ElementTree as ET
import sys
from variables import *
from swingutils.dialogs.basic import  showMessageDialog

def basic_import_data():
        global workRoot
        global workTree
        try:
            workTree =  ET.parse('JMRIimportedData.xml')
            workRoot = workTree.getroot()
        except:
            print "basicImportedData.py -- no basic_import_data() file opened"
            print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]
            showMessageDialog('The program import file (JMRIimportedData.xml)\ncon\'t be found or is corrupt.\n Fix the problem or find the file.\nPlace this file in the install directory.','Import file Error')

def basic_list_cars_engines_from_reader():
    ''' the list will include engines too'''
    global workRoot
    global workTree
    addList = []
    fullList = []
    reading = get_active_reader()
    for elem in workRoot:
        for subelem in elem.findall('car'):
            indentifier = str(subelem.get('reader', default="None"))
            if indentifier == reading:
                addList.append(str(subelem.get('rfid', default="None")))
                addList.append(str(subelem.get('type', default="None")))
                addList.append(str(subelem.get('color', default="None")))
                addList.append(str(subelem.get('roadName', default="None")))
                addList.append(str(subelem.get('roadNumber', default="None")))
                addList.append(str(subelem.get('owner', default="None")))
                addList.append(str(subelem.get('id', default="None")))
                addList.append(str(subelem.get('location', default="None")))
                addList.append(str(subelem.get('secLocation', default="None")))
                addList.append(str(subelem.get('eng', default="None")))
                addList.append(str(subelem.get('imported', default="None")))
                addList.append(str(subelem.get('reader', default="None")))
                fullList.append(addList)
                addList = []
    for elem in workRoot:
        for subelem in elem.findall('engine'):
            indentifier = str(subelem.get('reader', default="None"))
            if indentifier == reading:
                addList.append(str(subelem.get('rfid', default="None")))
                addList.append(str(subelem.get('type', default="None")))
                addList.append(str(subelem.get('color', default="None")))
                addList.append(str(subelem.get('roadName', default="None")))
                addList.append(str(subelem.get('roadNumber', default="None")))
                addList.append(str(subelem.get('owner', default="None")))
                addList.append(str(subelem.get('id', default="None")))
                addList.append(str(subelem.get('location', default="None")))
                addList.append(str(subelem.get('secLocation', default="None")))
                addList.append(str(subelem.get('eng', default="None")))
                addList.append(str(subelem.get('imported', default="None")))
                addList.append(str(subelem.get('reader', default="None")))
                fullList.append(addList)
                addList = []
    #print fullList
    return fullList             

def basic_get_reader_assignments():
    #print "got to reader assignments"
    global workRoot
    global workTree
    try:
        assignmentList =[]
        entryList = []
        for elem in workRoot:
            for subelem in elem.findall('location'):
                for tk in subelem.findall('track'):
                    indentifier = str(tk.get('assigned', default="None"))
                    if indentifier == "yes":
                        entryList.append( tk.get('reader', default="No Node"))
                        entryList.append( tk.get('id', default="No ID"))    
                        name = tk.get('name', default='None')
                        if name == "alone":
                           name = tk.get('saName', default='None')
                        entryList.append(name) 
                        entryList.append( tk.get('saName', default="No Name"))
                        assignmentList.append(entryList)
                        entryList = []
        #print "full list = ",assignmentList 
        set_basic_reader_assignments(assignmentList)
    except:
        print "basicImportedData.py -- basic_get_reader_assignments() failed"
        print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]
        set_basic_reader_assignments("unknown")
    
def basic_update_track_assignments(assignList): 
    global workRoot
    global workTree
    track = assignList
    emptyList = False
    test = track[0]
    trackID = str(test[0])
    reader = str(get_active_reader())
    if trackID == 'empty':
        emptyList = True            # all assignments for this reader have been removed
    try:
                for elem in workRoot:                                                 # remove all previous assignments to this reader
                    for subelem in elem.findall('location'):
                        for tk in subelem.findall('track'):
                            indentifier = str(tk.get('reader', default="None"))
                            if indentifier == reader:                   # remove for this reader only
                                tk.set('assigned', 'no')
                                tk.set('reader', 'none') 
    except:
                print "basicImportedData.py -- basic_update_track_assignments() [remove] failed"
                print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]
                
    if not emptyList:
        for each in track:
            trackID = str(each[0])
            toReader = str(each[1])
            if toReader == reader:                                                                 # is this track to be assigned to the current reader
                try:
                    for elem in workRoot:                                                  # record new assignments for this reader
                        for subelem in elem.findall('location'):
                            for tk in subelem.findall('track'):
                                indentifier = str(tk.get('id', default="None"))
                                if indentifier == trackID:
                                    tk.set('assigned', 'yes') 
                                    tk.set('reader', toReader) 
                                    #print (tk.get('assigned', default="Not assigned"))
                                    #print (tk.get('reader', default="No reader"))
                except:
                        print "basicImportedData.py -- update_track_assignments() [record] failed"
                        print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]
    save_basic_import_data_file()
    basic_get_reader_assignments()

def basic_update_engine_rfid_tags(engine, tag):
        ''' record new rfid tag value for JMRI file'''
        global workRoot
        global workTree
        for elem in workRoot:
            for subelem in elem.findall('engine'):
                exist = subelem.get('id', default='None')
                if str(exist) == engine:
                    subelem.set("rfid",str(tag))    

def basic_update_car_rfid_tags(saveCar, tag):
        ''' record new rfid tag value for JMRI file'''
        global workRoot
        global workTree  
        for elem in workRoot:
            for subelem in elem.findall('car'):
                exist = subelem.get('id', default='None')
                if str(exist) == saveCar:
                    subelem.set("rfid",str(tag))
    
def save_basic_import_data_file():
    global workRoot
    global workTree
    pretty_print(workRoot)                           # create one line entries
    try:
        workTree.write('JMRIimportedData.xml')
        print "file saved" 
    except:
        print "basicImportedData.py -- save_basic_import_data_file() failed"
        print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]

def pretty_print(current, parent=None, index=-1, depth=0):
        ''' indents each child element and places it on its own line  '''
        for i, node in enumerate(current):
            #print "node = ", node
            pretty_print(node, current, i, depth + 1)
        if parent is not None:
            if index == 0:
                parent.text = '\n' + ('\t' * depth)
            else:
                parent[index - 1].tail = '\n' + ('\t' * depth)
            if index == len(parent) - 1:
                current.tail = '\n' + ('\t' * (depth - 1))
        #print(ET.tostring(workRoot))
        
def basic_read_loc_track_tags():
    #print "got to basic read loc tags"
    global workRoot
    global workTree
    locationList = []
    trackList = []
    for elem in workRoot:
        for subelem in elem.findall('location'):
            getLocationData = {}
            indentifier = str(subelem.get('name', default="None"))
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
    set_basic_loc_track_tags(locationList)
    #print "LOc list = ", locationList
        
def basic_get_installed_readers():
    global workRoot
    global workTree
    try:
        installed ={}
        readers =[]
        for elem in workRoot:
            for subelem in elem.findall('reader'):
                indentifier = str(subelem.get('installed', default="None"))
                if indentifier == "yes":
                    address = subelem.get('address', default="NoAddress") # Node address
                    name = subelem.get('name', default="NoName")           #stand alone mode name
                    installed["address"] = address
                    installed["name"] = name
                    readers.append(installed)
                    installed = {}
        #print "installed readers = ",readers
        set_installed_readers(readers)
    except:
        print "basicImportedData.py -- basic_get_installed_readers() failed"
        print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]
        set_installed_readers("unknown")             

def basic_set_stand_alone_names(addName):
    try:
        for item in addName:                  # list of names
            oldName = item[0]
            newName = item[1]
            for elem in workRoot:
                for subelem in elem.findall('reader'):
                    indentifier = str(subelem.get('name', default="None"))
                    if indentifier == oldName:
                        name = subelem.set('name', newName)
        basic_get_installed_readers()                                                        # read from tree
        save_basic_import_data_file()
    except:
        print "basicImportedData.py -- basic_set_stand_alone_names() failed"
        print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]     

def basic_del_installed_reader(delReader):     
    try:                                                            
        deleteReader = delReader
        for elem in workRoot:
            for subelem in elem.findall('reader'):
                indentifier = str(subelem.get('address', default="None"))
                if indentifier == deleteReader:
                    address = subelem.set('installed', "no") 
                    name = subelem.set('name', deleteReader)           
        basic_get_installed_readers()                                                # read from tree
        save_basic_import_data_file()
    except:
        print "basicImportedData.py -- basic_del_installed_reader() failed"
        print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]        

def basic_get_available_reader():
    try:
        next = "full"
        for elem in workRoot:
            for subelem in elem.findall('reader'):
                indentifier = str(subelem.get('installed', default="None"))
                if indentifier == "no":
                    next = subelem.get('address', default="NoAddress") # Node address
                    #print "available reader = ",next
                    set_available_reader(next)
                    break
    except:
        print "basicImportedData.py -- basic_get_available_reader()  failed"
        print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]
        save_basic_import_data_file("unknown")        
       
def basic_set_installed_reader(addReader):     # addReader is list
    try:                                                             # only 1 reader can be added at a time
        newReader = addReader[0]
        newName = addReader[1]
        for elem in workRoot:
            for subelem in elem.findall('reader'):
                indentifier = str(subelem.get('address', default="None"))
                if indentifier == newReader:
                    address = subelem.set('installed', "yes") 
                    name = subelem.set('name', newName)           
        basic_get_installed_readers()                                                # read from tree
        save_basic_import_data_file()
    except:
        print "basicImportedData.py -- basic_set_installed_reader() failed"
        print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]        
        
def basic_get_list_of_engines():
    try:
        engineList = []
        getList = [0,1,2,3,4,5,6,7]
        for elem in workRoot:
            for subelem in elem.findall('engine'):
                getList[0] = subelem.get('rfid', default="No RFID")
                getList[1] = subelem.get('type', default="No type")
                getList[2] = subelem.get('color', default="No Model")
                getList[3] = subelem.get('roadName', default="No roadName")
                getList[4] = subelem.get('roadNumber', default="No roadNumber")
                getList[5] = subelem.get('owner', default="No owner")
                getList[6] = subelem.get('id', default="No ID")
                getList[7] = subelem.get('location', default="No Location")
                engineList.append(getList)
                getList = [0,1,2,3,4,5,6,7]
        #set_serial_rfid_engines(engineList)
        return engineList
    except:
        print "basicImportedData.py -- basic_get_list_of_engines() failed"
        print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]
        #set_serial_rfid_engines("unknown")        

def basic_get_list_of_cars():
    try:
        carList = []
        getList = [0,1,2,3,4,5,6,7]
        for elem in workRoot:
            for subelem in elem.findall('car'):
                getList[0] = subelem.get('rfid', default="No RFID")
                getList[1] = subelem.get('type', default="No type")
                getList[2] = subelem.get('color', default="No Color")
                getList[3] = subelem.get('roadName', default="No roadName")
                getList[4] = subelem.get('roadNumber', default="No roadNumber")
                getList[5] = subelem.get('owner', default="No owner")
                getList[6] = subelem.get('id', default="No ID")
                getList[7] = subelem.get('location', default="No Location")
                carList.append(getList)
                getList = [0,1,2,3,4,5,6,7]
        #set_serial_rfid_engines(engineList)
        return carList
    except:
        print "basicImportedData.py -- basic_get_list_of_cars() failed"
        print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]
        #set_serial_rfid_engines("unknown")           
   
def basic_get_cars_for_pull_drop(forEngine):
        try:
                carList = []
                getEngine = forEngine
                manifest = [0,1,2,3,4,5,6,7]
                for elem in workRoot:
                    for subelem in elem.findall('car'):
                        indentifier = str(subelem.get('eng', default="None"))
                        if indentifier == getEngine:
                                manifest[0] = subelem.get('rfid', default="No RFID")
                                manifest[1] = subelem.get('type', default="No type")
                                manifest[2] = subelem.get('color', default="No Model")
                                manifest[3] = subelem.get('roadName', default="No roadName")
                                manifest[4] = subelem.get('roadNumber', default="No roadNumber")
                                manifest[5] = subelem.get('owner', default="No owner")
                                manifest[6] = subelem.get('id', default="No ID")
                                manifest[7] = subelem.get('location', default="No Location")
                                carList.append(manifest)
                                manifest = [0,1,2,3,4,5,6,7]
                for elem in workRoot:
                    for subelem in elem.findall('engine'):
                        indentifier = str(subelem.get('eng', default="None"))
                        if indentifier == getEngine:
                                manifest[0] = subelem.get('rfid', default="No RFID")
                                manifest[1] = subelem.get('type', default="No type")
                                manifest[2] = subelem.get('color', default="No Model")
                                manifest[3] = subelem.get('roadName', default="No roadName")
                                manifest[4] = subelem.get('roadNumber', default="No roadNumber")
                                manifest[5] = subelem.get('owner', default="No owner")
                                manifest[6] = subelem.get('id', default="No ID")
                                manifest[7] = subelem.get('location', default="No Location")
                                carList.append(manifest)
                                manifest = [0,1,2,3,4,5,6,7]
                return carList
        except:
            print "basicImportedData.py -- basic_get_cars_for_pull_drop failed"
            print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]
            #set_serial_rfid_cars("unknown")        

        
def basic_get_location_for_pull_drop(forLocation):
        try:
                carList = []
                carsAt = forLocation
                manifest = [0,1,2,3,4,5,6,7]
                for elem in workRoot:
                    for subelem in elem.findall('car'):
                        indentifier = str(subelem.get('reader', default="None"))   # match reader for this location
                        if indentifier == carsAt:
                            indentifier = str(subelem.get('eng', default="None"))    # test if assigned to an engine
                            if indentifier == 'no':
                                    manifest[0] = subelem.get('rfid', default="No RFID")
                                    manifest[1] = subelem.get('type', default="No type")
                                    manifest[2] = subelem.get('color', default="No Color")
                                    manifest[3] = subelem.get('roadName', default="No roadName")
                                    manifest[4] = subelem.get('roadNumber', default="No roadNumber")
                                    manifest[5] = subelem.get('owner', default="No owner")
                                    manifest[6] = subelem.get('id', default="No ID")
                                    manifest[7] = subelem.get('location', default="No Location")
                                    carList.append(manifest)
                                    manifest = [0,1,2,3,4,5,6,7]
                for elem in workRoot:
                    for subelem in elem.findall('engine'):
                        indentifier = str(subelem.get('reader', default="None"))   # match reader for this location
                        if indentifier == carsAt:
                            indentifier = str(subelem.get('eng', default="None"))    # test if assigned to an engine
                            if indentifier == 'no':
                                    manifest[0] = subelem.get('rfid', default="No RFID")
                                    manifest[1] = subelem.get('type', default="No type")
                                    manifest[2] = subelem.get('color', default="No Model")
                                    manifest[3] = subelem.get('roadName', default="No roadName")
                                    manifest[4] = subelem.get('roadNumber', default="No roadNumber")
                                    manifest[5] = subelem.get('owner', default="No owner")
                                    manifest[6] = subelem.get('id', default="No ID")
                                    manifest[7] = subelem.get('location', default="No Location")
                                    carList.append(manifest)
                                    manifest = [0,1,2,3,4,5,6,7]
                return carList
        except:
            print "basicImportedData.py -- basic_get_location_for_pull_drop() failed"
            print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]
            #set_serial_rfid_cars("unknown")                
        
        
def basic_create_engine_tags(EngineData):
        ''' add attributes needed for SerialRFID to use  '''
        working = EngineData   
        buildDict = {}
        addEngine = []
        buildDict['rfid'] = str(working[0])
        buildDict['type'] = str(working[1])
        buildDict['color'] = str(working[2])  # used color as standard name in other code -- holds engine model
        buildDict['roadName'] = str(working[3])
        buildDict['roadNumber'] = str(working[4])
        buildDict['owner'] = str(working[5])
        buildDict['id'] = str(working[6])
        buildDict['location'] = 'None'      
        buildDict['secLocation'] = 'None' 
        buildDict['eng'] = "no"
        buildDict['imported'] = "no"  
        buildDict['reader'] = "A"
        addEngine.append(buildDict)
        try:
            add = workRoot.find('engines') 
            print "add = ", add
            ET.SubElement(add, 'engine',buildDict)
            pretty_print(workRoot)
            save_basic_import_data_file()
        except:
            print "basicImportedData.py -- basic_create_engine_tags() failed"
            print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]

def basic_create_car_tags(CarData):
        ''' add attributes needed for SerialRFID to use  '''
        working = CarData   
        buildDict = {}
        addEngine = []
        buildDict['rfid'] = str(working[0])
        buildDict['type'] = str(working[1])
        buildDict['color'] = str(working[2])  # used color as standard name in other code -- holds engine model
        buildDict['roadName'] = str(working[3])
        buildDict['roadNumber'] = str(working[4])
        buildDict['owner'] = str(working[5])
        buildDict['id'] = str(working[6])
        buildDict['location'] = 'None'      
        buildDict['secLocation'] = 'None' 
        buildDict['eng'] = "no"
        buildDict['imported'] = "no"  
        buildDict['reader'] = "A"
        addEngine.append(buildDict)
        try:
            add = workRoot.find('cars') 
            print "add = ", add
            ET.SubElement(add, 'car',buildDict)
            pretty_print(workRoot)
            save_basic_import_data_file()
        except:
            print "basicImportedData.py -- basic_create_car_tags() failed"
            print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]
        
def basic_add_car_to_engine(forEngine, thisCar):     
    print "got to basic_add_car_to_engine "
    print "forEngine = ", forEngine
    print "thisCar = ", thisCar
    try:                                                             
        for elem in workRoot:
            for subelem in elem.findall('car'):
                indentifier = str(subelem.get('id', default="None"))
                if indentifier == thisCar:
                    subelem.set('eng', forEngine)
                    subelem.set('reader', 'none')
        for elem in workRoot:
            for subelem in elem.findall('engine'):
                indentifier = str(subelem.get('id', default="None"))
                if indentifier == thisCar:
                    subelem.set('eng', forEngine)
                    subelem.set('reader', 'none')
        save_basic_import_data_file()
    except:
        print "basicImportedData.py -- basic_add_car_to_engine() failed"
        print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]           
       
def basic_drop_car_to_location(forLocation, thisCar):     
    print "got to basic_drop_car_to_location "
    print "forLocation = ", forLocation
    print "thisCar = ", thisCar
    try:                                                             
        for elem in workRoot:
            for subelem in elem.findall('car'):
                indentifier = str(subelem.get('id', default="None"))
                if indentifier == thisCar:
                    subelem.set('eng', 'no')    
                    subelem.set('reader', forLocation)
        for elem in workRoot:
            for subelem in elem.findall('engine'):
                indentifier = str(subelem.get('id', default="None"))
                if indentifier == thisCar:
                    subelem.set('eng', 'no')    
                    subelem.set('reader', forLocation)
        save_basic_import_data_file()
    except:
        print "basicImportedData.py -- basic_drop_car_to_location() failed"
        print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]                 
  
def basic_terminate_engine():
    assignment =   get_rfid_eng_assign()
    engine = assignment[0]
    location = assignment[1]
    reader = assignment[2]
    try:                                                             
        for elem in workRoot:
            for subelem in elem.findall('car'):
                indentifier = str(subelem.get('eng', default="None"))
                if indentifier == engine:
                    subelem.set('eng', 'no')    # drop all 'pulled' cars
                    subelem.set('reader', reader)
        for elem in workRoot:
            for subelem in elem.findall('engine'):
                indentifier = str(subelem.get('eng', default="None"))
                if indentifier == engine:
                    subelem.set('eng', 'no')         # drop all 'pulled' engines
                    subelem.set('reader', reader)
                indentifier = str(subelem.get('id', default="None"))
                if indentifier == engine:
                    subelem.set('reader', reader)  # park current engine at this location
        save_basic_import_data_file()
    except:
        print "basicImportedData.py -- basic_terminate_engine() failed"
        print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]        
        
def basic_delete_engine( thisEngine):     
    #print "got to basic_delete_engine() "
    #print "thisEngine = ", thisEngine
    try:                                                             
        for elem in workRoot:
            for subelem in elem.findall('engine'):
                indentifier = str(subelem.get('id', default="None"))
                if indentifier == thisEngine:
                    elem.remove(subelem)
        save_basic_import_data_file()
    except:
        print "basicImportedData.py -- basic_delete_engine() failed"
        print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]         

def basic_delete_car( thisCar):     
    #print "got to basic_delete_car() "
    #print "thisCar = ", thisCar
    try:                                                             
        for elem in workRoot:
            for subelem in elem.findall('car'):
                indentifier = str(subelem.get('id', default="None"))
                if indentifier == thisCar:
                    elem.remove(subelem)
        save_basic_import_data_file()
    except:
        print "basicImportedData.py -- basic_delete_car() failed"
        print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]             
        
if __name__ == '__main__':
        print 'running basicImportedData'   
        basic_import_data()
        list_cars_engines_from_reader()
        