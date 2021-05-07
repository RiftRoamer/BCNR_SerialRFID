
import time

#*******************************************
def get_available_reader():  
    ''' find next available reader (installed = NO) from RFIDconfig.XML'''
    try:
        global NextReaderVar
        return NextReaderVar
    except:
        return "unknown"

def set_available_reader(var):
    global NextReaderVar
    NextReaderVar = var
    #print "set the next avaialable reader = ",NextReaderVar



#*******************************************
def get_basic_reader_assignments():  
    ''' reads JMRIimport.xml for stored record of assign names to reader'''
    try:
        global AssignedVar
        return AssignedVar
    except:
        return "assignment unknown"

def set_basic_reader_assignments(var):
    global AssignedVar
    AssignedVar = var
    print "set list of  location names assigned to a reader = ", AssignedVar

#*******************************************
def get_installed_readers():  
    ''' from RFIDconfig.XML'''
    try:
        global InstalledVar
        return InstalledVar
    except:
        return "unknown"

def set_installed_readers(var):
    global InstalledVar
    InstalledVar = var
    print "set list of installed readers = ",InstalledVar

#******************************************
def get_mode():  
    ''' from RFIDconfig.XML'''
    try:
        global ModeVar
        return ModeVar
    except:
        return "unknown"

def set_mode(var):
    global ModeVar
    ModeVar = var
    #print "set mode of operation = ",ModeVar

#******************************************
def get_polling():  
    ''' not stored between startups defaults to polling active'''
    try:
        global PollVar
        return PollVar
    except:
        return "unknown"

def set_polling(var):   
    ''' triggered from main menu polling options and error message dialog'''
    global PollVar
    PollVar = var
    #print "set polling state to = ",PollVar

#******************************************
def get_xmit_cmd():    
    ''' acts as command stack pop(FIFO) overrides normal polling sequence'''
    try:
        global XmitCmdVar
        return XmitCmdVar
    except:
        return "unknown"

def set_xmit_cmd(var):
    global XmitCmdVar
    try:                                           # add command to stack
        if var == "empty":
            XmitCmdVar = []
        else:
            XmitCmdVar.append(var)
    except:                                     # allows configRFID to create empty list
        XmitCmdVar = []
    #print "set transmit command to = ", XmitCmdVar
    
#*******************************************
def get_jmri_engine_roster_path():
    try:
        global EngFileVar
        return EngFileVar
    except:
        return "unknown"

def set_jmri_engine_roster_path(var): # set by config menu 
    global EngFileVar
    EngFileVar = var
    #print "set engine roster path = ",EngFileVar

#******************************************
def get_jmri_car_roster_path():
    try:
        global CarFileVar
        return CarFileVar
    except:
        return "unknown"

def set_jmri_car_roster_path(var): # set by config menu
    global CarFileVar
    CarFileVar = var
    #print "set car roster path = ",CarFileVar

#*******************************************
def get_jmri_location_roster_path():
    try:
        global LocFileVar
        return LocFileVar
    except:
        return "unknown"
    
def set_jmri_location_roster_path(var): # set by config menu
    global LocFileVar
    LocFileVar = var
    #print "set locations roster path = ",LocFileVar

#*******************************************
def get_my_port_var():  
    ''' stored in RFIDconfig.XML    ??????????????????????????????????????????????????????????'''
    try:
        global PortVar
        return PortVar
    except:
        return "unknown"

def set_my_port_var(port):
    global PortVar
    PortVar = port
    #print "set my port = ",PortVar

#*******************************************
def get_locations():
    '''use JMRI "locations roster" XMLfile and build variable list'''
    try:
        global JmriLocVar
        return JmriLocVar
    except:
        return "unknown"

def set_locations(var):
    global JmriLocVar
    JmriLocVar = var
    #print "set_locations variable is never used ",JmriLocVar
 
#*******************************************
def get_jmri_cars():
    '''use JMRI "Car roster" XMLfile and build variable list of cars without a RFID tag'''
    try:
        global JmriStockVar
        return JmriStockVar
    except:
        return "unknown"

def set_jmri_cars(var):
    global JmriStockVar
    JmriStockVar = var
    #print "set_jmri_cars variable ",JmriStockVar
    
#*******************************************
def get_jmri_engines():
    '''use JMRI "Engine roster" XMLfile and build variable list'''
    try:
        global JmriEngVar
        return JmriEngVar
    except:
        return "unknown"

def set_jmri_engines(var):
    global JmriEngVar
    JmriEngVar = var
    #print "set_jmri_engines variable ",JmriEngVar

#*********************************************

def get_desktop_gui():
    '''holds desktop frame object'''
    try:
        global DesktopGuiVar
        return DesktopGuiVar
    except:
        return "unknown"

def set_desktop_gui(obj):
    global DesktopGuiVar
    DesktopGuiVar = obj
    #print "set_desktop_gui variable  ",DesktopGuiVar
    
#*********************************************
def get_basic_loc_track_tags():
    '''holds a combined list of JMRI locations and tracks from location roster XML'''
    try:
        global BasicLocationTrackVar
        return BasicLocationTrackVar
    except:
        return "unknown"

def set_basic_loc_track_tags(var):
    global BasicLocationTrackVar
    BasicLocationTrackVar = var
    #print "From basicImportData.py -- set_basic_loc_track_tags variable  ",BasicLocationTrackVar
    
#*********************************************

def get_jmri_loc_track_tags():
    '''holds a combined list of JMRI locations and tracks from location roster XML'''
    try:
        global JmriLocationTrackVar
        return JmriLocationTrackVar
    except:
        return "unknown"

def set_jmri_loc_track_tags(var):
    global JmriLocationTrackVar
    JmriLocationTrackVar = var
    #print "From JMRIlistAll.py -- set_jmri_loc_track_tags variable  ",JmriLocationTrackVar
    
#*********************************************

def get_linked_gui():     # linked gui changes depending on which dialog is opened
    '''temp hold of current gui for a dialog'''
    try:
        global LinkGuiVar
        return LinkGuiVar
    except:
        return "unknown"

def set_linked_gui(obj):
    global LinkGuiVar
    LinkGuiVar = obj
    #print "set_linked_gui variable  ",LinkGuiVar
    
#*********************************************

def get_rfid_eng_assign():
    '''holds engines from RFIDconfig.XML-- used by engine menu add/drop car'''
    try:
        global EngAssignmentVar
        return EngAssignmentVar
    except:
        return ["unassigned", "unassigned", "unassigned"] # engine id, jmri text, reader address

def set_rfid_eng_assign(var):
    global EngAssignmentVar
    EngAssignmentVar = var
    print "set_rfid engine assignment variable  ",EngAssignmentVar            
    
#*********************************************

def get_active_reader():
    '''used mostly for engine menu add / drop car -- updates Desktop and dialog displays'''
    try:
        global ReaderVar
        return ReaderVar
    except:
        return "A" 

def set_active_reader(var):
    global ReaderVar
    ReaderVar = var
    gui = get_desktop_gui()
    AR = "Active reader is " + ReaderVar
    gui.readerText.text = AR
    #print "set the current reader variable  ",ReaderVar           
    
#*******************************************************

def get_send_car_to_reader():
    '''get send car to reader variable'''
    try:
        global SendcarVar
        return SendcarVar
    except:
        return "unknown" 

def set_send_car_to_reader(var):
    global SendcarVar
    SendcarVar = var
    #print "set send car to reader variable  ",SendcarVar          
    
#*******************************************************

def get_comm_hold():
    ''''Comm respondes will vary in length (thus time neeeded)  this variable  resets the compare time each time Method rec_data gets a heathly reply
     and gives more time for the next \n marking another complete piece of data was recieved.'''
    try:
        global CommHoldVar
        return CommHoldVar
    except:

        return 0 

def set_comm_hold():    # reset comparator timer
    global CommHoldVar                   
    CommHoldVar = int(round(time.time()*1000)) 
    #print "set Comm hold comparator variable  ",CommHoldVar    
    
#*******************************************************    
def get_reply_from_reader():
    '''get data back from a reader'''
    try:
        global ReaderDataVar
        return ReaderDataVar
    except:
        return "unknown" 

def set_reply_from_reader(var):
    global ReaderDataVar
    ReaderDataVar = var
    print "got some data from a reader",ReaderDataVar          
 
#*******************************************


#*******************************************************

if __name__ == "__main__":
    print "running variables.py"
   