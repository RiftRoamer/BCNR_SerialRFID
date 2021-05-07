
# File Menu
from configGUI import *
from importJMRIFiles import *
# Locations Menu
from listAllJmriLocations import *
from listCarsFromReader import *
from linkJmriLocationsToReader import *
from ReaderSet import *
# Engines Menu
from listAllJmriEngines import *
from createEngine import *
from assignToLocation import *
from enginePickupDropOffCar import *
from listCarsInEngine import *
from terminateEngine import *
from deleteEngine import *
# Readers Menu
# see readerSet under locations Menu
from ReaderAdd import *
from ReaderDelete import *
# Cars Menu
from listAllJMRIcars import *
from assignRFIDtagToCar import *
from standAloneProgramming import *
from deleteCar import *


import sys
from mycommport import *
from variables import *

class Switcher(object):
    '''Match menu selection to a function'''
    def get_selection(self, argument):
        """Convert menu text to a function"""
        method_name = str(argument)
        method = getattr(self, method_name, lambda: "Invalid Pick")
        #print "**********  method  = ",method_name
        # Call the method as we return it
        return method()
    
    # -------------- File Menu  ---------------------------------------------
    
    def configure(self):
         '''Set the serial port default = None'''
         x = ProgramConfig()
         x.show()

    def import_jmri_files(self):
        ''' get JMRI files to use with stand alone mode '''
        ImportJMRIFiles()

    def exit(self): 
        '''end program'''
        a = get_active_port()
        a.close_port()
        sys.exit()

        # ------------- Polling Menu -----------------------------------------
        
    def enable_polling(self): 
        '''turn on / off comm port polling in stand alone mode'''
        set_polling(True)
    
    def disable_polling(self): 
        '''turn off comm port polling'''
        set_polling(False)

    # ------------------- Mode menu ---------------------------------------
    
    def stand_alone(self): 
        '''reserved for things to do when mode changes to stand alone'''
        set_mode("stand alone")
        c_set_mode()
        x = get_desktop_gui()
        x.enable.doClick()    # toggle to polling automatically for the mode
        print "--------- stand alone mode"
        #set_polling(True)
         
    def jmri(self): 
        '''reserved for things to do when mode changes to JMRI'''
        set_mode("jmri")
        c_set_mode()
        x = get_desktop_gui()
        x.disable.doClick()   # no polling in this mode -- process commands allowed
        print "--------- jmri mode"


 # ----------------- Location Menu --------------------------------------

    def list_all_jmri_locations(self):
        ''' run JMRI XML file and get layout locations.'''
        ListAllJmriLocations()

    def list_cars_from_a_reader(self):    # stand alone mode
        ''' list cars in a reader SD Card'''
        ListCarsFromReader()
        
    def link_jmri_location_to_a_reader(self):  # stand alone mode
        '''asign location(s) to a reader'''
        LinkJmriLocationsToReader()

    def  add_text_location_to_a_reader(self):   # stand alone mode
        '''stand alone mode add text'''
        ReaderSet()
        
  # -------------------- Engines Menu -----------------------------------      
 
    def list_all_jmri_engines(self):
        #print "************* got to switch for list all jmri engines *************"
        ListAllJmriEngines()
     
    def create_engine(self):
        '''Make a RFID train for readers to use'''
        CreateEngine()
    
    def asign_to_location(self):
        '''RFID engine is working this reader'''
        AssignToLocation()

    def pick_up_drop_off_car(self):
        ''' Pull car off of reader and assign to RFID train'''
        EnginePickupDropoffCar()
    
    def list_cars_in_engine(self):
       '''Display cars in selected train'''
       #print "car list"
       ListCarsInEngine()
    
    def terminate_engine(self):
        '''Take all cars off of the engine and assign to reader'''
        TerminateEngine()
    
    def delete_engine(self):
        '''Delete engine from the systemr'''
        DeleteEngine() 
 
# ------------------------  Readers Menu ----------------------------------------------
 
    def set_active_reader(self):
        '''List all readers installed in the system'''
        ReaderSet()
 
    def add_reader(self):
        ''' Add new reader to system'''
        ReaderAdd()
        
    def delete_reader(self):
        '''Remove reader from the system'''
        ReaderDelete() 
 
 # -----------------  Cars Menu ----------------------------------------
 
    def list_all_jmri_cars(self):
        '''Get JMRI cars with no RFID tag assigned'''
        ListAllJMRICars()
    
    def assign_rfid_tag_to_car(self):
        '''Assign RFID tag to car in JMRI XML file. Write JMRI data to the reader rfid tag'''
        AssignRFIDtagToCar()
        
    def stand_alone_mode_car_programming(self):
         '''Write manual data entered to the reader rfid tag'''
         StandAloneProgramming() 
 
    def delete_car(self):
        '''Delete car from the systemr'''
        DeleteCar() 
      
if __name__ == '__main__':
    print "running switcher.py"
 