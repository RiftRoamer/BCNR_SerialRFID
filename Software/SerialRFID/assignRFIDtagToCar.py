from  javax.swing import *
from  java.awt import *
from  java.awt.event import *
from variables import *
from javax.swing.table import DefaultTableModel
from swingutils.events import *
from javax.swing.event import *
from javax.swing.BorderFactory import *
from configRFID import *
import sys
import time
from swingutils.dialogs.basic import showMessageDialog
from JMRIlistAll import *
from importFiles import *
        
class AssignRFIDtagToCar(JDialog):
    def __init__(self):
        global changes
        changes = []
        #gui = get_desktop_gui()    # add to init (replace None) to link dialog with desktop
        JDialog.__init__(self, None, 'Assign RFID Tag', False)
        #self.setDefaultCloseOperation(DO_NOTHING_ON_CLOSE)
        self.setSize(925,330)
        self.setLayout(BorderLayout())
        self.setLocation(100,100)
        self.preferredSize = (Dimension(1100,330))
        self.setBackground(Color.LIGHT_GRAY)
        
        self.northPanel = JPanel()
        #northPanel.setLayout(BorderLayout())
        self.noteText = JLabel('   Assign RFID Tag to Car   ')
        self.noteText.setForeground(Color.decode("#000dff"))
        self.noteText.setBackground(Color.decode("#000000"))
        self.noteText.setFont(Font("Serif", Font.PLAIN, 24))
        self.northPanel.add(self.noteText)
        self.add(self.northPanel,BorderLayout.NORTH)
        
        self.southPanel = JPanel()
        self.titleText = JLabel('   Click on a "row" to select the car to be assigned - then Assign Tag  ')
        self.titleText.setForeground(Color.decode("#000dff"))
        self.titleText.setBackground(Color.decode("#000000"))
        self.titleText.setFont(Font("Serif", Font.PLAIN, 20))
        self.southPanel.add(self.titleText)
        self.add(self.southPanel,BorderLayout.SOUTH)   

        self.westPanel = JPanel()
        self.westPanel.setPreferredSize(Dimension(315,330))
        self.westPanel.setLayout(BoxLayout(self.westPanel, BoxLayout.X_AXIS))
        self.westPanel.add(Box.createVerticalGlue())
        self.explain = (" \nThis is a list of Cars/ Engines extracted from JMRI Operations 'Car' and 'Engine' rosters that have no "
        "RFID tag assigned to them.\n\nTwo operations are performed here:\n1> The RFID tag sitting on Reader A is captured "
        " and recorded in the proper JMRI Car/Engine roster.\n2> The Car/Engine information displayed (plus a bit more) "
        "is recorded on the RFID chip located at reader A\n\nTable Row --\n Selects the car to be processed\n\n " 
        "Assign Tag button --\nPerforms the assignment and updates the table, then waits for the next assignment.\n\n"
        "Cancel button -- Exit without making an assignment\n\n")
        self.westPanel.add(Box.createRigidArea(Dimension(15, 0)))
        self.westExplian = (JTextArea(text = self.explain,
                editable = False,
                wrapStyleWord = True,
                lineWrap = True,
                alignmentX = Component.LEFT_ALIGNMENT,
                size = (300, 125)
        ))
        self.westPane = JScrollPane()
        self.westPane.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_ALWAYS)
        self.westPane.setPreferredSize(Dimension(315,125))
        self.westPane.getViewport().setView(self.westExplian)
        self.westPanel.add(self.westPane)    
        self.add(self.westPanel,BorderLayout.WEST)
        
        self.centerPanel = JPanel()
        self.centerPanel.setLayout(BoxLayout(self.centerPanel, BoxLayout.Y_AXIS))
        self.centerPanel.setPreferredSize(Dimension(600,330))
        self.tablePanel = JPanel()
        self.tablePanel.setLayout(BoxLayout(self.tablePanel, BoxLayout.X_AXIS))
        self.tablePanel.setPreferredSize(Dimension(550,330))
        self.tablePanel.add(self.add_sa_table())
        self.centerPanel.add(self.tablePanel)
        self.enterPanel = JPanel()
        self.enterPanel.setSize(350,100)
        self.enterPanel.preferredSize = (Dimension(350,100))
        self.enterPanel.setLayout(BoxLayout(self.enterPanel, BoxLayout.Y_AXIS))
        self.inputPanel = JPanel()
        self.inputPanel.setSize(350,75)
        self.inputPanel.preferredSize = (Dimension(350,75))
        self.inputPanel.setLayout(BoxLayout(self.inputPanel, BoxLayout.X_AXIS))
        global newName
        self.noSelection = JLabel("Be sure to place car on reader A")
        self.inputPanel.add(Box.createRigidArea(Dimension(130, 0)))
        self.inputPanel.add(self.noSelection)
        self.inputPanel.add(Box.createRigidArea(Dimension(130, 0)))
        self.enterPanel.add(self.inputPanel)
        self.buttonPanel = JPanel()
        self.buttonPanel.setSize(400,100)
        self.buttonPanel.preferredSize = (Dimension(400,100))
        self.buttonPanel.setLayout(BoxLayout(self.buttonPanel, BoxLayout.X_AXIS))
        self.buttonPanel.add(Box.createRigidArea(Dimension(130, 0)))
        #change = JButton('Enter Change', actionPerformed = self.new_data)
        #buttonPanel.add(change)
        self.enterPanel.add(self.buttonPanel)
        self.centerPanel.add(self.enterPanel)
        self.add(self.centerPanel,BorderLayout.CENTER)
        
        self.eastPanel = JPanel()
        self.eastPanel.setLayout(BoxLayout(self.eastPanel, BoxLayout.Y_AXIS))
        self.eastPanel.preferredSize = (Dimension(150,1))
        self.saveName = JButton('Assign tag', actionPerformed = self.save_data)
        self.cancel = JButton('Cancel', actionPerformed = self.cancel_data)
        self.eastPanel.add(Box.createRigidArea(Dimension(25, 25)))
        self.eastPanel.add(self.saveName)
        self.eastPanel.add(Box.createRigidArea(Dimension(25, 25)))
        self.eastPanel.add(self.cancel)
        self.add(self.eastPanel,BorderLayout.EAST)
        
        
        self.setVisible(True)
        set_linked_gui(self)
        
    def add_sa_table(self):
            
            self.colNames = ('Type',"Color/Model","Road Name", "Road Number")
            self.dataModel = DefaultTableModel(self.sort_sa_data(), self.colNames)
            self.table = JTable(self.dataModel)
            self.table.getTableHeader().setReorderingAllowed(0)
            self.table.setSelectionMode(0)
            self.scrollPane = JScrollPane()
            self.scrollPane.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_ALWAYS)
            self.scrollPane.setPreferredSize(Dimension(330,125))
            self.scrollPane.getViewport().setView(self.table)
            self.panel = JPanel()
            self.panel.preferredSize = (Dimension(330,200))
            self.panel.add(self.scrollPane)
            return self.panel

    def save_data(self, event):
        try:
            a = 0
            #print "got to save data"
            row = self.table.getSelectedRow()
            if row < 0:
                showMessageDialog('Please select a row with a car or an engine.\n',"Car ID Required")
                return
            else:
                print "selected row = ",row
                global carCount
                global  allEngines
                print "size of allEngines = ", len(allEngines)
                print "car count = ", carCount
                if row  >= carCount:                                      # check if an engine has been selected
                    a = row - carCount
                    print "selected engine = ", allEngines[a]
                    tagCar = allEngines[a]
                    tagID = tagCar[6]
                    saveWhat = "engine"
                else:                                                                     # processing a car
                    tagCar = allCars[row]
                    tagID = tagCar[6]
                    saveWhat = "car"
                    #print "selected car = ", allCars[row]
                #print "selected tagID = ", tagID
                #print "selected tagCar = ", tagCar
                #print "saveWhat = ", saveWhat
                self.ready_command(tagCar,tagID,saveWhat)   # go send the command

        except:
            print "assignRFIDtagToCar.py -- save_data failed"
            print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]

    
    def ready_command(self, sendCar, id, save):
        #set_polling(False)
        tagCar = sendCar
        passCar = []
        set_send_car_to_reader(passCar)  # remove last car sent
        trimCar = []                             # drop stuff not sent to tag
        trimCar.append(tagCar[1])      # type
        trimCar.append(tagCar[2])      # color = model for engine
        trimCar.append(tagCar[3])      # roadName
        trimCar.append(tagCar[4])      # roadNumber
        trimCar.append(tagCar[5])      # owner
        trimCar.append(tagCar[6])      # id
        
        for item in trimCar:
            a = (item[0:16])
            b = len(a)
            if b == 0:
                a = "################"
            if b < 16:
                c = a
                a = c.ljust(16," ")
            passCar.append(a)
        #print passCar
        command = ['*A04']
        set_xmit_cmd(command)
        
        timeOut = True
        set_reply_from_reader("")
        delayTime = 1000
        set_comm_hold()
        holdTime = get_comm_hold() 
        delta = 0 
        while delta < delayTime:               
              loopTime =  int(round(time.time()*1000))
              holdTime = get_comm_hold()
              delta = loopTime - holdTime 
              tag = ""
              tag = get_reply_from_reader() #variable
              if len(tag) > 0:
                  delta = delayTime + 500
                  timeOut = False
        if timeOut:
            self.rec_tag_error()
            print "reply from read RFID tag timer timed out"
        #print "got a good tag = ", tag
        if tag > 0:
            if save == "car":
                stripTag = tag[5:]
                update_car_rfid_tags(id, stripTag)                                             # update JMRI ops car file via JMRIlistAll.py
                save_car_xml_file()
                basic_update_car_rfid_tags(id, stripTag)
                save_basic_import_data_file()                                                   # update JMRIimport.xml file via basicImportData.py
            else:
                stripTag = tag[5:]
                update_engine_rfid_tags(id, stripTag)                                             # update JMRI ops engine file via JMRIlistAll.py
                save_engine_xml_file()
                basic_update_car_rfid_tags(id, stripTag)
                save_basic_import_data_file()                                                   # update JMRIimport.xml file via basicImportData.py
        else:
            rec_tag_error()
            return
        set_send_car_to_reader(passCar)
        command = ['*A09']
        set_xmit_cmd(command)                       # master wants to write car data to RFID chip on the car

        timeOut = True
        set_reply_from_reader("")
        delayTime = 3500
        set_comm_hold()
        holdTime = get_comm_hold() 
        delta = 0 
        while delta < delayTime:               
              loopTime =  int(round(time.time()*1000))
              holdTime = get_comm_hold()
              delta = loopTime - holdTime 
              write = get_reply_from_reader() #variable
              if len(write) > 0:
                  delta = delayTime + 500
                  timeOut = False
        if timeOut:
            self.rec_write_error()
            return
            print "reply from write RFID timer timed out"
        print "got a good write= ", write
        self.update_display()
                      
    def rec_write_error(self):
        '''bad reply from reader'''
        showMessageDialog('The requested car RFID update failed to write.\n'
        'Please check that you have positioned the car correctly\n AND\nthat you are using Reader A',"Car write Error")                      
                      
                   
    def rec_tag_error(self):
        '''bad reply from reader'''
        showMessageDialog('The requested RFID tag failed to read.\n'
        'Please check that you have positioned the car correctly\n AND\nthat you are using Reader A',"Tag read Error")
         
    def cancel_data(self, event):
        #print "got to cancel data"
        global changes
        changes = []
        #print changes
        self.dispose()
        
        
    def sort_sa_data(self):
         '''Sort installed readers list for table display'''
         print "got to sort sa data"
         try:
             global allCars
             global  allEngines
             allCars = get_jmri_cars()
             allEngines = get_jmri_engines()
             temp = []
             tableData = []
             global carCount
             carCount = 0
             for shrink in allCars:
                 test = shrink[0]
                 if test == "111111" or test == "None":
                     temp = []
                     temp.append(shrink[1])
                     temp.append(shrink[2])
                     temp.append(shrink[3])
                     temp.append(shrink[4])
                     tableData.append(temp)
                     carCount = carCount + 1
             temp = []
             for shrink in allEngines:
                 test = shrink[0]
                 if test == "111111" or test == "None":
                     temp = []
                     temp.append(shrink[1])
                     temp.append(shrink[2])
                     temp.append(shrink[3])
                     temp.append(shrink[4])
                     tableData.append(temp)   
             return tableData
         except:
             print "something wrong with sort_data"
             print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]

    def update_display(self):
            self.centerPanel.remove(self.tablePanel)
            self.revalidate()
            self.tablePanel = JPanel()
            self.tablePanel.setLayout(BoxLayout(self.tablePanel, BoxLayout.X_AXIS))
            self.tablePanel.setPreferredSize(Dimension(550,330))
            self.tablePanel.add(self.add_sa_table())
            self.centerPanel.add(self.tablePanel)
            self.revalidate()
            self.repaint()    

if __name__ == "__main__":
    print "Running readerGUI.py"
        