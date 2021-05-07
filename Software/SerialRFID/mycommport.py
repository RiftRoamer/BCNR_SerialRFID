import gnu.io
import gnu.io.RXTXPort as RXTX
import time
from  javax.swing import JOptionPane
from javax.swing import *
from  java.awt import *
import sys
from SerialRFID import *      
from basicImportedData import *

# ----------------------------------------------------------------------------------------------------------------
def SelectComPort():
    '''open dialog and get comm port'''
    comList = []
    try:
        thePorts = gnu.io.CommPortIdentifier.getPortIdentifiers()
        while thePorts.hasMoreElements():
              com =  thePorts.nextElement()
              portType = com.getPortType()
              if portType == gnu.io.CommPortIdentifier.PORT_SERIAL:
                   comList.append(com.getName())
        global choice
        choice = JOptionPane.showInputDialog(None, "Select a Com Port...", "Serial RFID COM Port",  JOptionPane.INFORMATION_MESSAGE, None, comList, comList[1])
        if choice == None:
            print "no change"
            return choice
        else:
            #print choice
            return choice
    except:
        print "Can't list available ports"

# --------------------------------------------------------------------------------------------------------------------------------
def rec_data_error():
    '''no reply from comm port'''
    #print "show dialog"
    global a
    showMessageDialog('The selected Comm port is not receiving a reply from the field device.\n'
    'Please check that you have selected the correct port\n OR\nconnections to field devices',"Comm Port Error")
    #set_polling(False)
    return False
    
# --------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------
class MyCommPort():
           #serialPort =''
           def __init__(self):
                       ''' dummy attributes to do nothing but assign the class to an object'''
                       _true = 12
                       _false = 13

# ----------------------------------------------------------------------------------------------------------    
           def set_port(self, port):
                       '''Use picked port and configure it'''
                       _port = str(port)
                        #Open COM port
                       try:
                                  portId=gnu.io.CommPortIdentifier.getPortIdentifier(_port)
                                  global serialPort
                                  serialPort=portId.open("Serial RFID",5000)        #(Name,delay)
                       except gnu.io.PortInUseException:
                                  print "port in use"
                                  return
                       except gnu.io.NoSuchPortException:
                                  print "no such port"
                       except gnu.io.IOException:
                                  print "IO error"
                                  #Set port parameters
                       try:
                                  serialPort.setSerialPortParams(9600,RXTX.DATABITS_8,RXTX.STOPBITS_1,RXTX.PARITY_NONE)
                                  serialPort.setFlowControlMode(serialPort.FLOWCONTROL_NONE)
                                  serialPort.setOutputBufferSize(1024)
                                  #print "buffer size = ", serialPort.getOutputBufferSize()
                                  #print "set port"
                       except gnu.io.UnsupportedCommOperationException: 
                                  print "Port parameter error"
                                  return
                       #Open input & output streams
                       self.outStream=serialPort.getOutputStream()
                       self.inStream=serialPort.getInputStream()
                       time.sleep(0.1)

# ----------------------------------------------------------------------------------------------
           def close_port(self):
                       '''Close inStream, outStream before closing the port itself'''
                       self.outStream.close()
                       self.inStream.close()
                       global serialPort
                       serialPort.close()
                       #print "Port has been closed"

# ----------------------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------------------
class Polling(SwingWorker, object):
   ''' setup main program thread'''
   def  __init__(self, port):
               global pollPort
               pollPort = port      # pass in Com port to use
               self.gui = get_desktop_gui()           # pass in desktop object for process to update
               SwingWorker.__init__(self)
               pollPort.outStream.flush()
               for char in str(pollPort.inStream.read()):
                   print "instream dump", char

# -----------------------------------------------------------------------------------------------------------------------------------------------
   def process(self, address, state, data="none"):
       ''' update state of stuff in the GUI frames'''
       try:
           self.gui.pollText.text = address   #display what address is Xmit and @ when waiting for reply
           if state == "stop":
               self.gui.disable.doClick()               # set polling menu to disable and stop polling
           #elif state == "start":
            #   self.gui.enable.doClick()               # set polling menu to disable and stop polling    
           elif state == "error":
                self.gui.rec_data_error()
           elif state == "pull":
                print "got to pull"
                basic_add_car_to_engine(data[0], data[1])
           elif state == "drop":
                print "got to drop"
                basic_drop_car_to_location(data[0], data[1])
       except:
           print "something wrong with process"
           print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]

# ----------------------------------------------------------------------------------------------------------------------------------------------------
   def done(self):
       ''' things to do when closing thread'''
       print "got to done"
       pass

# -------------------------------------------------------------------------------------------------------------------------------------------------           
   def doInBackground(self):
       '''Main loop for polling reader nodes'''
       pollRate = 300                                                  # set poll rate in mmilliseconds
       holdTime = int(round(time.time()*1000))        # remember last poll point
       loopTime =  int(round(time.time()*1000))       # measure looping time
       delta = 0                                                            # difference in time
       while True:
               try:
                   poll = get_polling()                                #test program menu has polling enabled
                   stack = poll_stack()                               # check for additions / deletions of installed readers allows dynamic changes to polling
                   if not poll:                                              # comm loop disabled
                       #defaultCmd = []                               # cancel any commands
                       #set_xmit_cmd("empty")                    # set variable
                       placeHolder = 0                                 # this IF does nothing -- future use?
                       
                   if poll and stack:                                    # must have at least one reader installed to poll
                       xmit = get_xmit_cmd()                      # needed to see if somehing else has added a command to the stack
                       commandPresent = len(xmit)
                       if commandPresent > 0:
                           print "top command present"
                           self.process_command()
                       for reader in stack:
                          holdTime = int(round(time.time()*1000)) 
                          delta = 0 
                          while delta < pollRate:               
                              loopTime =  int(round(time.time()*1000))
                              delta = loopTime - holdTime 
                          self.query =   "*" + reader + "08" + "query\n"
                          self.toOutput=  self.query 
                          self.xmit_data(self.toOutput, reader)
                          time.sleep(.03)
                          self.rec = self.recv_data()
                          print "polling got this ", self.rec
                          s = str(self.rec)
                          req = s[0]
                          print"req = ", req                                                   # type of reply
                          if req == "?":                                                         # question mark (?) means reader  is sending something
                              cmdList = []                                                      
                              cmdList.append(self.rec)                                   # place the query reply in a list
                              set_xmit_cmd(cmdList)                                     # appends command to variable list acting as a stack        
                          xmit = get_xmit_cmd()                                          # needed to see if somehing else has added a command to the stack
                          commandPresent = len(xmit)
                          if req == "X":
                               #cursor = get_linked_gui()
                               #cursor.setCursor(Cursor.getPredefinedCursor(Cursor.DEFAULT_CURSOR))
                               self.process( "@", "error")
                          
                          if commandPresent > 0:                                       # break polling loop if a command needs to be processed
                              print "command detected break issued"
                              break
                          poll = get_polling()
                          if not poll:
                               break
                          holdTime = loopTime
                   else:
                           
                           while not poll:
                               poll = get_polling()
                               if not poll:
                                   mode = get_mode()
                                   if mode == 'jmri':
                                       #print "****************************************       got to no poll jmri test"
                                       self.process("Polling is Idle", "nothing")
                                       xmit = get_xmit_cmd()                      # needed to see if  JMRI mode has added a command to the stack
                                       commandPresent = len(xmit)
                                       if commandPresent > 0:
                                           print "top command present"
                                           self.process_command()
                                   else:
                                       self.process("Polling is Disabled", "nothing")
                                       time.sleep(0.3)
                                       pollPort.outStream.flush()
                                       time.sleep(1)
                                       for char in str(pollPort.inStream.read()):
                                           print "instream dump", char
               except:
                    print "something wrong with do in background"
                    print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]
                    
           #loopTime =  int(round(time.time()*1000))
    
# -------------------------------------------------------------------------------------------------------------------------    
   def process_command(self):
    try:
        print "got to process commnad"
        c = get_xmit_cmd()  # list of commands from variable
        print "c = ", c
        process = c.pop(0)  #acts as a FIFO command stack
        print "process = ", process
        command = process[0]
        print "processing = ", command
        reader = command[1]
        print "reader = ", reader
        self.part1 = command[2]
        self.part2 = command[3]
        self.cmd = self.part1 + self.part2
        print "cmd = ", self.cmd
        
# ---------------------------------------------   command 1  ---------------------------------------------------------------------------     
# ---------------------------------------- add a car to this engine  --------------------------------------------------------------------
        if self.cmd == "01":
               print "got to command 01"
               carList = []
               try:
                   self.answer = self.reply[4:]
                   #print "answer = ", self.answer
                   carList = self.answer.split('~')
                   #print "carList = ", carList
                   self.process( "#", "pull", data = carList )
               except:
                       print "something wrong with command 1"
                       print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1] 

# ----------------------------------------------   command 2  --------------------------------------------------------------------  
 # ----------------------------------- add a car to this location (reader) -------------------------------------------------------             
        elif self.cmd == "02":
               print "got to command 02"
               carList = []
               try:
                   self.answer = self.reply[4:]
                   #print "answer = ", self.answer
                   carList = self.answer.split('~')
                   #print "carList = ", carList
                   self.process( "#", "drop", data = carList )
               except:
                       print "something wrong with command 2"
                       print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1] 
             
# ----------------------------------------------------   command 4  ----------------------------------------------------------------------------     
# ------------------------------------ get RFID tag for current car on reader  --------------------------------------------------------------
        elif self.cmd == "04":
             print "command 04"
             cursor = get_linked_gui()
             cursor.setCursor(Cursor.getPredefinedCursor(Cursor.WAIT_CURSOR))
             x = command.rstrip()
             fullCommand = x + "getTag\n"  # get RFID tag for current car on reader
             #print "full command = ", fullCommand
             self.xmit_data(fullCommand, reader)
             time.sleep(.100)
             answer = self.recv_data()
             #print "answer = ", answer
             set_reply_from_reader(answer)
             cursor = get_linked_gui()
             cursor.setCursor(Cursor.getPredefinedCursor(Cursor.DEFAULT_CURSOR))           
  
        # ---------------------------------------------   command 9  ---------------------------------------------------------------------------   
        # -----------------------------------  write dat to this car's RFID chip   -------------------------------------------------------------
        elif self.cmd == "09":
             #''' Write car data to RFID chip'''
            try:
                   print "command 09"
                   cursor = get_linked_gui()
                   cursor.setCursor(Cursor.getPredefinedCursor(Cursor.WAIT_CURSOR))
                   fullCommand  = ""
                   data = get_send_car_to_reader()
                   build = ""
                   for item in data:
                       build = build + item + "~"
                   a = (build[0:-1])   # strip off last tilde
                   fullCommand = command + a  + "\n" 
                   self.xmit_data(fullCommand, reader)
                   time.sleep(1)
                   self.answer = self.recv_data()
                   set_reply_from_reader(self.answer)
                   cursor = get_linked_gui()
                   cursor.setCursor(Cursor.getPredefinedCursor(Cursor.DEFAULT_CURSOR))
            except:
                           print "something wrong with command 9"
                           print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1] 
                           return    
             
        print "got to proeccess command return"
        return
    except:
        print "something wrong with process command"
        print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]            

# -----------------------------------------------------------------------------------------------------------------
   def xmit_data(self,sendThis, reader):
               '''commands and data sent to readers'''
               print 'xmit send this ',sendThis
               polling = "Polling " + reader
               self.process(polling,"start")
               global pollPort
               try:
                          pollPort.outStream.write(sendThis)
               except:
                          print "bad xmit" 
                          print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]
               time.sleep(0.2)    # allow GUI to toggle polling symbol

# -----------------------------------------------------------------------------------------------------------------               
   def recv_data(self):
               '''replies and requests from readers'''
               attemps = 0
               count = 0
               self.process("Polling @", "start")     # toggle label on main GUI
               self.char =''                                        # holds a characcter from buffer
               self.reply = ''                                      # complete reply from reader
               while count <  50:                              # 2.1 seconds -- Ardunio tests card reader every 2 
                   try:
                       present = pollPort.inStream.available()
                       #print "***************     present = ", present
                       if present > 0:
                           #while pollPort.inStream.available:
                           self.char =pollPort.inStream.read()
                           if self.char == 10:               # test for new line \n end of message
                                    print "recv got this ", self.reply
                                    set_comm_hold()     # good read reset timeout comparator
                                    return self.reply
                           else:
                                     self.reply = self.reply + chr(self.char)
                       else: 
                           count = count + 1
                           print "count = ", count
                           time.sleep(.07)
                   except:
                       attemps = attemps + 1
                       if attemps < 6:
                           print "attemping another read"
                           print "char = ",self.char
                           time.sleep(.2)
                           continue
                       else:
                           print "something wrong with recieved data"
                           print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]
                           #rec_data_error()
                           return "X"
               return "X"
    
# ----------------------------------------------------------------------------------------------------------------------------           
   '''def rec_data_errorX(self):
        #no reply from comm port
        #print "show dialog"
        showMessageDialog('The selected Comm port is not receiving a reply from the field device.\n'
        'Please check that you have selected the correct port\n OR\nconnections to field devices',"Comm Port Error")
        #set_polling(False)'''
   
# -----------------------------------------------------------------------------------------------------------------------------    
def poll_stack():
     '''Sort variable installed readers list of dictionaries and extract polling addresses'''
     try:
         pollList = []
         dictList = get_installed_readers()
         for dictionary in dictList:
             address = dictionary.get('address') # ignores / drops the reader's name
             pollList.append(address)
         if len(pollList) > 0:  # must have at least one reader
                 return pollList
         else:
                 return False
     except:
         print "something wrong with poll_stack"
         print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]

# ------------------------------------------------------------------------------------------------------------------------------
   
if __name__ == '__main__':
   print "running mycommport.py"