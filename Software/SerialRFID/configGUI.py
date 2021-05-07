from java import awt
from javax.swing import *
from java import awt
from switcher import *
from mycommport import *
from variables import *
from configRFID import *
from swingutils.dialogs.basic import showMessageDialog 
from swingutils.dialogs.filechooser import *

def get_jmri_engines_path(JFileChooser):
    '''get path and file name for JMRI operations "Engine roster" XMLfile'''
    global engineFile
    showMessageDialog('Please select the path & file name for the JMRI\nOperationsEngineRoster.XML\nfile', 'Engines XML File')
    #prefs = getUserPrefs('C:\\Users') #pereerence for where to save file
    txtFilter = SimpleFileFilter('xml')
    #engineFile = showOpenDialog(txtFilter, prefs=None, prefkey=None, multiselect=False)
    engineFile = showOpenDialog(txtFilter, prefs=None, prefkey=None, multiselect=False)
    if engineFile == None:
        print "got none from engine path picker"
    else:
        global oldEngineLabel
        oldEngineLabel.text = str(engineFile) + "    "
        global newConfigEngine
        newConfigEngine = engineFile
        global engineChange
        engineChange = True
        #print engineChange
        #print newConfigEngine
 

def get_jmri_cars_path(JFileChooser):
    '''get path and file name for JMRI operations "Car roster" XMLfile'''
    global carPath
    showMessageDialog('Please select the path & file name for the JMRI\nOperationsCarRoster.XML\nfile', 'Car XML File')
    txtFilter = SimpleFileFilter('.xml')
    carPath = showOpenDialog(txtFilter, prefs=None, prefkey=None, multiselect=False)
    if carPath == None:
        print "got none from car path picker"
    else:
        global oldCarLabel
        oldCarLabel.text = str(carPath) + "    "
        global newConfigCar
        newConfigCar = carPath
        global carChange
        carChange = True
        #print carChange
        #print newConfigCar

def get_jmri_locations_path(JFileChooser):
    '''get path and file name for JMRI operations "location roster" XMLfile'''
    global opsFile
    showMessageDialog('Please select the path & file name for the JMRI\nOperationsLocationRoster.XML\nfile', 'Locations XML File')
    txtFilter = SimpleFileFilter('.xml')
    opsFile = showOpenDialog(txtFilter, prefs=None, prefkey=None, multiselect=False)
    if opsFile == None:
        print "got none from location picker"
    else:
        #print "opsFile = ", opsFile
        global oldLocationLabel
        oldLocationLabel.text = str(opsFile) + "    "
        global newConfigLocation
        newConfigLocation = opsFile
        #print "new file = ", newConfigLocation
        global locationChange
        locationChange = True

        

    
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
        return comList
    except:
        print "Can't list available ports"

def save_changes(event):
    #print "save changes"
    global panelName  # holds object name so it can be closed
    global portChange
    global engineChange
    global locationChange
    global carChange
    global newConfigPort
    global newConfigEngine
    global newConfigLocation
    global newConfigCar
    
    if portChange == True:
        #print "port change is true"
        c_set_comm_port(newConfigPort)
    if engineChange == True:
        #print "engine change is true"
        c_set_jmri_engine_roster_path(newConfigEngine)
    if carChange == True:
        #print"car change is true"
        c_set_jmri_car_roster_path(newConfigCar)
    if locationChange == True:
        #print "location change is true"
        c_set_jmri_location_roster_path(newConfigLocation)
    if locationChange or carChange or engineChange or portChange:
        save_config_file()
        showMessageDialog('Saving all changes to the configuration file.','Saving Changes')
        panelName.dispose()
        global portChange
        portChange = False
        global engineChange
        engineChange = False
        global locationChange
        locationChange = False
        global carChange
        carChange = False
    
def cancel_changes( event):
    global panelName  # holds object name so it can be closed
    global portChange
    portChange = False
    global engineChange
    engineChange = False
    global locationChange
    locationChange = False
    global carChange
    carChange = False
    panelName.dispose()
          
class ComboAction(awt.event.ActionListener):
    def actionPerformed(self,event):
            if event.getActionCommand() == "Spam":
                print 'Spam and eggs!'
            else:
                global cb
                global newConfigPort
                newConfigPort = cb.getSelectedItem()
                global oldCommLabel
                oldCommLabel.text = newConfigPort
                global portChange
                portChange = True
                
class ProgramConfig(JFrame):    
    global engineChange
    engineChange = False
    global carChange
    carChange = False
    global locationChange
    locationChange = False
    global portChange
    portChange = False
    
    def __init__(self):
        
        JFrame.__init__(self,
                         'Serial RFID Configuration',
                         size=(1000,240),
                         defaultCloseOperation=JFrame.DISPOSE_ON_CLOSE)
        self.setLayout(BorderLayout())
        self.setLocation(100,100)
        self.preferredSize = 1000,240
        self.setBackground(Color.LIGHT_GRAY)
        northPanel = JPanel()
        northPanel.setLayout(BorderLayout())
        noteText = JLabel('   NOTE: Serial RFID must be restarted before changes will take affect   ')
        noteText.setForeground(Color.decode("#000dff"))
        noteText.setBackground(Color.decode("#000000"))
        noteText.setFont(Font("Serif", Font.PLAIN, 20))
        northPanel.add(noteText)
        self.add(northPanel,BorderLayout.NORTH)

        westPanel = JPanel()
        #westPanel.add(Box.createHorizontalGlue())
        westPanel.setLayout(BoxLayout(westPanel, BoxLayout.Y_AXIS))
        westPanel.setBackground(Color.LIGHT_GRAY)
        data = SelectComPort()
        #print data
        global cb
        cb = JComboBox(data)
        cb.addActionListener(ComboAction())
        westPanel.add(cb)
        westPanel.add(Box.createRigidArea(Dimension(25, 5)))
        b3 = JButton("Location",actionPerformed = get_jmri_locations_path)
        westPanel.add(Box.createRigidArea(Dimension(25, 10)))
        westPanel.add(b3)
        b4 = JButton("Car",actionPerformed = get_jmri_cars_path)
        westPanel.add(Box.createRigidArea(Dimension(25, 10)))
        westPanel.add(b4)
        westPanel.add(Box.createRigidArea(Dimension(25, 10)))
        b5 = JButton("Engine",actionPerformed = get_jmri_engines_path)
        westPanel.add(b5)
        westPanel.add(Box.createRigidArea(Dimension(25, 22)))
        self.add(westPanel,BorderLayout.WEST)
        
        
        centerPanel = JPanel()
        centerPanel.setLayout(BoxLayout(centerPanel, BoxLayout.Y_AXIS))
        centerPanel.setBackground(Color.LIGHT_GRAY)
        global label
        label = JLabel('Selext a comm port from the dropdown list ')
        centerPanel.add(Box.createRigidArea(Dimension(25,5)))
        centerPanel.add(label)
        centerPanel.add(Box.createRigidArea(Dimension(25,22)))
        global locationLabel
        locationLabel = JLabel('JMRI OperationsLocationRoster.XML =  ') 
        centerPanel.add(locationLabel)
        centerPanel.add(Box.createRigidArea(Dimension(25, 22)))
        global CarLabel
        CarLabel = JLabel('JMRI OperationsCarRoster.XML =  ')
        global EngineLabel
        centerPanel.add(CarLabel)
        centerPanel.add(Box.createRigidArea(Dimension(25, 22)))
        EngineLabel = JLabel('JMRI OperationsEngineRoster.XML =  ')
        centerPanel.add(EngineLabel)
        centerPanel.add(Box.createRigidArea(Dimension(25, 22)))
        self.add(centerPanel,BorderLayout.CENTER)
        
        spacebar = "    "
        global configPort
        configPort = get_my_port_var() + spacebar
        #print "kelly = ",configPort
        global configLocation
        configLocation = get_jmri_location_roster_path() + spacebar
        global configCar
        configCar = get_jmri_car_roster_path() + spacebar
        global configEngine
        configEngine = get_jmri_engine_roster_path() + spacebar
        
        
        eastPanel = JPanel()
        eastPanel.setLayout(BoxLayout(eastPanel, BoxLayout.Y_AXIS))
        eastPanel.setBackground(Color.LIGHT_GRAY)
        global oldCommLabel
        #eastPanel.add(Box.createRigidArea(Dimension(25,5)))
        oldCommLabel = JLabel(configPort)
        eastPanel.add(Box.createRigidArea(Dimension(25,5)))
        eastPanel.add(oldCommLabel)
        eastPanel.add(Box.createRigidArea(Dimension(25,22)))
        global oldLocationLabel
        oldLocationLabel = JLabel(configLocation)
        #oldLocationLabel = JLabel("C:\Users\jwkel\Documents\NetBeansProjects\JythonProject\src\OperationsLocationRoster.xml    ")
        eastPanel.add(oldLocationLabel)
        eastPanel.add(Box.createRigidArea(Dimension(25, 22)))
        global oldCarLabel
        oldCarLabel = JLabel(configCar)
        eastPanel.add(oldCarLabel)
        eastPanel.add(Box.createRigidArea(Dimension(25, 22)))
        global oldEngineLabel     
        oldEngineLabel = JLabel(configEngine)
        eastPanel.add(oldEngineLabel)
        eastPanel.add(Box.createRigidArea(Dimension(25, 22)))
        self.add(eastPanel,BorderLayout.EAST)
        
        southPanel = JPanel()
        southPanel.setLayout(BoxLayout(southPanel, BoxLayout.X_AXIS))
        southPanel.setBackground(Color.LIGHT_GRAY)
        southPanel.add(Box.createRigidArea(Dimension(25, 5)))
        b3 = JButton("Save",actionPerformed = save_changes)
        southPanel.add(Box.createRigidArea(Dimension(25, 10)))
        southPanel.add(b3)
        global panelName  #holds object name for close and save methods so they can close frame
        panelName = self
        b4 = JButton("Cancel",actionPerformed = cancel_changes)
        southPanel.add(Box.createRigidArea(Dimension(25, 10)))
        southPanel.add(b4)
        southPanel.add(Box.createRigidArea(Dimension(25, 22)))
        self.add(southPanel,BorderLayout.SOUTH)

        self.pack()
    def cancel_close(self):
        #print "got to close"
        self.dispose()
        
if __name__ == '__main__':
    global demo
    demo = ProgramConfig()
    demo.setLocation(30, 30)
    demo.show()
        
