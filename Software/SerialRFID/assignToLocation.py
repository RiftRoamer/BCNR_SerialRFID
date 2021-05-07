from  javax.swing import *
from  java.awt import *
from  java.awt.event import *
from variables import *
from basicImportedData import *
import sys

class AssignToLocation(JDialog):
    
    def __init__(self):
        global noRadioButton
        noRadioButton = True
        global noRadioButton2
        noRadioButton2 = True
        showAssignment = get_rfid_eng_assign()
        global engineClick
        engineClick = showAssignment[0]     # engine id
        global assignmentClick
        assignmentClick = showAssignment[1]  #JMRI text
        global assignmentClick2
        assignmentClick2 = showAssignment[2] # reader number
        JDialog.__init__(self, None, 'Assign an engine to a location', True)
        #self.setDefaultCloseOperation(DO_NOTHING_ON_CLOSE)
        self.setSize(900,375)
        self.setLayout(BorderLayout())
        self.setLocation(100,100)
        self.preferredSize = 900,375
        self.setBackground(Color.LIGHT_GRAY)
        
        self.northPanel = JPanel()
        noteText = JLabel('Engine                               Location / Reader                                       ')
        noteText.setForeground(Color.decode("#000dff"))
        noteText.setBackground(Color.decode("#000000"))
        noteText.setFont(Font("Serif", Font.PLAIN, 24))
        self.northPanel.add(noteText)
        self.add(self.northPanel,BorderLayout.NORTH)
        
        self.westPanel = JPanel()
        self.westPanel.add(self.sort_rfid_engine())
        self.add(self.westPanel,BorderLayout.WEST) 
        global displayMode 
        displayMode = get_mode()
        
        self.centerPanel = JPanel()
        if displayMode == "stand alone":
            self.centerPanel.add(self.sort_alone_assignment())
        else:
             self.centerPanel.add(self.sort_jmri_assignment())
        self.add(self.centerPanel,BorderLayout.CENTER) 
        
        self.eastPanel = JPanel()
        self.eastPanel.preferredSize = (Dimension(250,100))
        self.cancel = JButton('Cancel', actionPerformed = self.cancel_dialog)
        self.assign = JButton(' Assign ', actionPerformed = self.link_box)
        self.eastPanel.add(Box.createRigidArea(Dimension(25, 10)))
        self.comboPanel = JPanel()
        self.comboPanel.setLayout(BoxLayout(self.comboPanel, BoxLayout.Y_AXIS))
        self.comboPanel.preferredSize = (Dimension(200,100))
        self.comboPanel.add(self.assign)
        self.comboPanel.add(Box.createRigidArea(Dimension(25, 10)))
        self.comboPanel.add(self.cancel)
        self.eastPanel.add(self.comboPanel)
        self.add(self.eastPanel,BorderLayout.EAST)
        
        self.southPanel = JPanel()
        global engineClick
        global assignmentClick
        global assignmentClick2
        newText = "Currently engine " + engineClick + " is assigned to " + assignmentClick + "   reader " + assignmentClick2
        self.assignText = JLabel(newText, SwingConstants.CENTER)
        self.assignText.setForeground(Color.decode("#000dff"))
        self.assignText.setBackground(Color.decode("#000000"))
        self.assignText.setFont(Font("Serif", Font.PLAIN, 24))
        self.textPanel = JPanel()
        self.textPanel.setLayout(BoxLayout(self.textPanel, BoxLayout.X_AXIS))
        self.textPanel.preferredSize = (Dimension(850,50))
        self.textPanel.add(self.assignText)
        
        self.southPanel.add(self.textPanel)
        self.add(self.southPanel,BorderLayout.SOUTH)
        
        self.setVisible(True)
        self.sort_rfid_engine()

    def on_click(self, event):    
            global  assignmentClick    # location / reader
            global  assignmentClick2
            label = event.getActionCommand()
            a = label.split(".")                  # use decimal to split text line - 3 parts
            assignmentClick = a[0].strip() # JMRI English text
            assignmentClick2 = a[2].strip() # reader address A/B/C etc
            global noRadioButton
            noRadioButton = False
            
    def on_click2(self, event):    # engine
            global engineClick
            label2 = event.getActionCommand()
            a2 = label2.split(".")
            engineClick = a2[0].strip()  # engine id
            global noRadioButton2
            noRadioButton2 = False
            
    def sort_alone_assignment(self):
         '''make a radio button for every stand alone mode location'''
         locationList = get_installed_readers()    # variables  
         print "installed readers = ", get_installed_readers()
         self.boxPanel = JPanel()
         self.boxPanel.setLayout(BoxLayout(self.boxPanel, BoxLayout.Y_AXIS))
         self.boxPanel.preferredSize = (Dimension(250,300))
         try: 
             self.group = ButtonGroup()
             for location in locationList:                                                       
                     text = location['name'] + ".        " + "Reader - ." + location['address']      #add period to act as seperator
                     padText = text.ljust(90," ")
                     self.cb = JRadioButton(padText, actionPerformed = self.on_click) 
                     self.group.add(self.cb)
                     self.locPanel = JPanel()
                     self.locPanel.setLayout(BoxLayout(self.locPanel, BoxLayout.X_AXIS))
                     self.locPanel.preferredSize = (Dimension(250,50))
                     self.locPanel.add(self.cb)
                     self.boxPanel.add(self.locPanel)
             
             locationList = get_basic_reader_assignments()    # variables
             print "location list 2 = ", locationList
             for location in locationList:                                                       
                     text = location[2] + ".        " + "Reader - ." + location[0]      
                     padText = text.ljust(90," ")
                     self.cb = JRadioButton(padText, actionPerformed = self.on_click) 
                     self.group.add(self.cb)
                     self.locPanel = JPanel()
                     self.locPanel.setLayout(BoxLayout(self.locPanel, BoxLayout.X_AXIS))
                     self.locPanel.preferredSize = (Dimension(250,50))
                     self.locPanel.add(self.cb)
                     self.boxPanel.add(self.locPanel)
                     
             self.scrollPane = JScrollPane(self.boxPanel)
             self.scrollPane.setPreferredSize(Dimension(250,225))
             self.panel = JPanel()
             self.panel.add(self.scrollPane)
             self.pack()
             return self.panel   
         except:
             print "something wrong with sort_rfid_assignment"
             print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]
     
    def sort_jmri_assignment(self):
         '''make a checkbox for every JMRI Operations location'''
         print "got to assignments"
         locationList = get_basic_reader_assignments()    # variables
         print "location list = ", locationList
         self.boxPanel = JPanel()
         self.boxPanel.setLayout(BoxLayout(self.boxPanel, BoxLayout.Y_AXIS))
         self.boxPanel.preferredSize = (Dimension(250,300))
         try: 
             self.group = ButtonGroup()
             for location in locationList:                                                       
                     text = location[2] + ".        " + "Reader - ." + location[0]      
                     padText = text.ljust(90," ")
                     self.cb = JRadioButton(padText, actionPerformed = self.on_click) 
                     self.group.add(self.cb)
                     self.locPanel = JPanel()
                     self.locPanel.setLayout(BoxLayout(self.locPanel, BoxLayout.X_AXIS))
                     self.locPanel.preferredSize = (Dimension(250,50))
                     self.locPanel.add(self.cb)
                     
                     
                     self.boxPanel.add(self.locPanel)
             self.scrollPane = JScrollPane(self.boxPanel)
             self.scrollPane.setPreferredSize(Dimension(250,225))
             self.panel = JPanel()
             self.panel.add(self.scrollPane)
             self.pack()
             return self.panel   
         except:
             print "something wrong with sort_data"
             print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]
             
    def sort_rfid_engine(self):
         '''make a checkbox for every JMRI Operations location'''
         engineList = basic_get_list_of_engines()    # variables
         self.boxPanel2 = JPanel()
         self.boxPanel2.setLayout(BoxLayout(self.boxPanel2, BoxLayout.Y_AXIS))
         self.boxPanel2.preferredSize = (Dimension(250,300))
         try: 
             self.group2 = ButtonGroup()
             for engine in engineList:                                                       
                     text = engine[6] + ".   " + engine[2] + "   " + engine[3] + " " + engine[4]      
                     padText = text.ljust(90," ")
                     self.cb = JRadioButton(padText, actionPerformed = self.on_click2) 
                     self.group2.add(self.cb)
                     self.locPanel2 = JPanel()
                     self.locPanel2.setLayout(BoxLayout(self.locPanel2, BoxLayout.X_AXIS))
                     self.locPanel2.preferredSize = (Dimension(250,50))
                     self.locPanel2.add(self.cb)
                     self.boxPanel2.add(self.locPanel2)
             self.scrollPane2 = JScrollPane(self.boxPanel2)
             self.scrollPane2.setPreferredSize(Dimension(250,225))
             self.panel2 = JPanel()
             self.panel2.add(self.scrollPane2)
             self.pack()
             return self.panel2   
         except:
             print "something wrong with sort_rfid_engine"
             print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]
         
    def link_box(self, event):    
            global engineClick  # engine id
            print "engine ID = ", engineClick
            global assignmentClick # Stand alone text - name stored in readers RFIDconfig.XML
            global assignmentClick2 # reader address A/B/C etc
            global noRadioButton
            global noRadioButton2
            if noRadioButton or noRadioButton2:
                showMessageDialog('An Engine and a location\n'
                    'must be selected before an assignment can be made.\n ',"Assignment Error")
                return 
            #print "radio buttons were set"
            newText = "Currently engine " + engineClick + " is assigned to " + assignmentClick + "   reader " + assignmentClick2
            self.assignText.text = newText
            set_rfid_eng_assign([engineClick, assignmentClick, assignmentClick2])
            self.gui = get_desktop_gui() 
            self.gui.asignText.text =  newText
            noRadioButton = True
            noRadioButton2 = True
            self.dispose()
        
    def cancel_dialog(self, event):
            self.dispose()