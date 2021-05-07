from javax.swing import *
from javax import imageio
from java import io
import time
from switcher import *
from mycommport import *
from java.lang import Runnable
from variables import *
from configRFID import *

class DesktopFrame(JFrame):
           """    Base GUI code     By: Jim Kelly 12-6-20           """

           def __init__(self):
            """
            Creates the Main program frame
            """
            JFrame.__init__(self,
                            'Serial RFID Layout Monitor',
                            size=(900,500),
                            defaultCloseOperation=JFrame.EXIT_ON_CLOSE)

            self.setLayout(BorderLayout())
            self.preferredSize = 900,500
            self.getContentPane().setBackground( Color.LIGHT_GRAY )
            self.create_menus()
            self.image("rfid_pic.jpg")
            self.text = ("\nFundamentally SerialRFID provides the user with an easy to use Liduid Crystal Display (LCD)) showing the road markings of your rolling stock. "
            "To accomplish this each piece of stock must have a Radio Frequency Identification (RFID) tag. The local LCD display will show 1- Type (boxcar), "
            "2- Color (Green), 3- Road name/number (Milw123) and 4-Owner (John Doe.) Items 1-3 were selected because of the ease they create while working "
            "a yard; say during an operations session. Item 4 can help clubs and OPS hosts indentify who owns that piece of stock when there is duplicate stock "
            "with identical markings.\n\nSerialRFID is not integrated with JMRI but it does haave a 'hook' into its XML files so that if you have entered your "
            "engines, cars and locations that information can be pulled into SerialRFID and even send that information to a RFID chip without having to "
            "manually reenter all that data. Details are explained in the manual.\n" )
            self.main_pane(self.text)
            self.mode_panel()
            
            self.southPanel = JPanel()
            self.southPanel.setLayout(BorderLayout())
            self.southPanel.setBackground(Color.LIGHT_GRAY)
            self.southPanel.setLayout(BoxLayout(self.southPanel, BoxLayout.X_AXIS))
            self.southPanel.add(Box.createRigidArea(Dimension(25, 25)))
            self.add(self.southPanel, BorderLayout.SOUTH)
            
            self.centerPanel = JPanel()
            self.centerPanel.setLayout(BorderLayout())
            self.centerPanel.setBackground(Color.LIGHT_GRAY)
            self.centerPanel.setLayout(BoxLayout(self.centerPanel, BoxLayout.X_AXIS))
            #self.centerPanel.setSize(25, 25)
            self.centerPanel.setPreferredSize(Dimension(25, 25))
            self.centerPanel.add(Box.createRigidArea(Dimension(25, 25)))
            #self.centerPanel = JLabel("Polling Reader - ?")
            self.add(self.centerPanel, BorderLayout.CENTER)
            
            self.pack()
            self.visible = True
            comm = get_my_port_var()   # from variables
            #print "comm = ",get_my_port_var() 
            global comPort
            comPort = MyCommPort()                       #mycommport
            set_desktop_gui(self)
            set_active_reader('A')                                #variable
            comPort.set_port(comm)                           #mycommport
            self.startPolling = Polling(comPort)          #mycommport
            self.startPolling.execute()                          #mycommport
            #set_swing_worker (self.startPolling)
            currentMode = get_mode()
            if currentMode == "stand alone":
                    self.alone.doClick()
            else:
                    self.jmri.doClick()

           def menu_pick(self, event):  
                       '''Capture which menu item was selected'''
                       c=event.getActionCommand()
                       if c == "Stand Alone":
                                  self.menu0.visible = 1
                                  self.menu00.visible = 0
                                  self.menu2.visible=0 
                                  self.menu2a.visible=1
                                  self.menu3.visible=0
                                  self.menu3a.visible=1
                                  self.menu4.visible=1 
                                  self.menu5.visible=0 
                                  self.menu5a.visible=1 
                                  self.modeText.text="Current Mode Setting: Stand Alone"

                       if c =="JMRI":
                                  self.menu0.visible = 0
                                  self.menu00.visible = 1
                                  self.menu2.visible=1 
                                  self.menu2a.visible=0
                                  self.menu3.visible=1
                                  self.menu3a.visible=0
                                  self.menu4.visible=0 
                                  self.menu5.visible=1
                                  self.menu5a.visible=0
                                  self.modeText.text="Current Mode Setting: JMRI"
            
                       d = c.replace(" ","_")
                       e = d.lower()
                       a=Switcher()
                       a.get_selection(e)

           def image(self, fileName):
                       '''Put picture on the Introduction panels'''
                       self.tPanel = JPanel()
                       self.tPanel.setLayout(BorderLayout())
                       self.tPanel.setBackground(Color.LIGHT_GRAY)
                       self.tPanel.setLayout(BoxLayout(self.tPanel, BoxLayout.Y_AXIS))
                       self.tPanel.setPreferredSize(Dimension(465, 250))
                       self.tPanel.add(Box.createRigidArea(Dimension(25, 25)))
                       self.panel = JPanel()
                       self.panel.setLayout(BorderLayout())
                       self.panel.setBackground(Color.LIGHT_GRAY)
                       self.panel.setPreferredSize(Dimension(465, 250))
                       self.panel.setLayout(BoxLayout(self.panel, BoxLayout.X_AXIS))
                       self.panel.add(Box.createRigidArea(Dimension(25, 25)))
                       _image_filename = fileName
                       self.showImage = imageio.ImageIO.read(io.File(_image_filename))
                       self.panel.add(JLabel(ImageIcon(self.showImage)))
                       #self.panel.add(Box.createRigidArea(Dimension(25, 25)))
                       self.tPanel.add(self.panel)
                       self.add(self.tPanel, BorderLayout.WEST)
                       self.pack()
        
           def main_pane(self, text):
                       ''' Put introduction text into mainPanel'''
                       _text = text
                       
                       self.sPanel = JPanel()
                       self.sPanel.setLayout(BoxLayout(self.sPanel, BoxLayout.Y_AXIS))
                       self.sPanel.add(Box.createRigidArea(Dimension(50, 25)))
                       self.sPanel.setBackground(Color.LIGHT_GRAY)
                       self.sPanel.preferredSize = (Dimension(400,250))
                       
                       
                       self.mainText = JTextArea()
                       self.mainText.text = _text
                       self.mainText.lineWrap = True
                       self.mainText.wrapStyleWord = True
                       self.mainText.setCaretPosition(0);
                       self.mainText.preferredSize = (Dimension(400,250))
                       self.mainText.setBackground(Color.LIGHT_GRAY)
                       self.mainScroll = JScrollPane(self.mainText)
                       self.mainScroll.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_ALWAYS)
                       self.mainScroll.setPreferredSize(Dimension(400, 250))
                       self.mainScroll.getViewport().setView((self.mainText))
                       self.mainPanel = JPanel()
                       self.mainPanel.setLayout(BoxLayout(self.mainPanel, BoxLayout.X_AXIS))
                       self.mainPanel.preferredSize = (Dimension(400,250))
                       self.mainPanel.add(Box.createRigidArea(Dimension(50, 25)))
                       self.mainPanel.setBackground(Color.LIGHT_GRAY)
                       self.mainPanel.add(self.mainScroll)
                       self.mainPanel.add(Box.createRigidArea(Dimension(25, 25)))
                       self.sPanel.add(self.mainPanel)
                       self.add(self.sPanel, BorderLayout.EAST)
                       self.pack()
                       
           def mode_panel(self):
                       ''' Toggle mode display'''
                       self.pollText = JLabel("Polling Reader - ?")
                       self.pollPanel = JPanel()
                       self.pollPanel.setLayout(BoxLayout(self.pollPanel, BoxLayout.X_AXIS))
                       self.pollPanel.preferredSize = (Dimension(300,35))
                       self.pollPanel.add(Box.createRigidArea(Dimension(75, 25)))
                       self.pollPanel.add(self.pollText)
                       self.pollPanel.setBackground(Color.LIGHT_GRAY)
                       self.modeText = JLabel("Current Mode Setting : Stand Alone")
                       self.modePanel = JPanel()
                       self.modePanel.setLayout(BoxLayout(self.modePanel, BoxLayout.X_AXIS))
                       self.modePanel.preferredSize = (Dimension(300,35))
                       self.modePanel.add(Box.createRigidArea(Dimension(50, 25)))
                       self.modePanel.add(Box.createRigidArea(Dimension(50, 25)))
                       self.modePanel.add(self.modeText)
                       self.modePanel.add(Box.createRigidArea(Dimension(50, 25)))
                       self.readerText = JLabel("Active reader is A")
                       self.modePanel.add(Box.createRigidArea(Dimension(50, 25)))
                       self.modePanel.add(self.readerText)
                       self.modePanel.setBackground(Color.LIGHT_GRAY)
                       self.rightPanel = JPanel()
                       self.rightPanel.setLayout(BoxLayout(self.rightPanel, BoxLayout.X_AXIS))
                       self.rightPanel.preferredSize = (Dimension(300,35))
                       self.rightPanel.add(Box.createRigidArea(Dimension(300, 25)))
                       self.rightPanel.setBackground(Color.LIGHT_GRAY)
                       self.fillPanel = JPanel()
                       self.fillPanel.setLayout(BoxLayout(self.fillPanel, BoxLayout.X_AXIS))
                       self.fillPanel.preferredSize = (Dimension(300,35))
                       self.fillPanel.add(self.modePanel)
                       self.fillPanel.add(self.pollPanel)
                       self.fillPanel.add(self.rightPanel)
                       self.assignment = get_rfid_eng_assign()
                       self.asignText =  JLabel("Currently engine " + self.assignment[0] + " is assigned to " + self.assignment[1] + "   reader " + self.assignment[2])
                       self.asignPanel = JPanel()
                       self.asignPanel.setLayout(BoxLayout(self.asignPanel, BoxLayout.X_AXIS))
                       self.asignPanel.preferredSize = (Dimension(300,35))
                       #self.asignPanel.add(Box.createRigidArea(Dimension(50, 25)))
                       #self.asignPanel.add(Box.createRigidArea(Dimension(50, 25)))
                       self.asignPanel.add(self.asignText)
                       
                       self.combinedPanel = JPanel()
                       self.combinedPanel.setLayout(BoxLayout(self.combinedPanel, BoxLayout.Y_AXIS))
                       self.combinedPanel.preferredSize = (Dimension(300,50))
                       self.combinedPanel.add(self.fillPanel)
                       self.combinedPanel.add(self.asignPanel)
                       
                       self.add(self.combinedPanel, BorderLayout.NORTH)
                       self.pack()
    
    
           def rfid_intro(self, event):  
                       '''Basic setup instruction on Main frame'''
                       self.sPanel.visible = False
                       self.tPanel.visible = False
                       self.text = ("\nFundamentally SerialRFID provides the user with an easy to use Liduid Crystal Display (LCD)) showing the road markings of your rolling stock. "
                            "To accomplish this each piece of stock must have a Radio Frequency Identification (RFID) tag. The local LCD display will show 1- Type (boxcar), "
                            "2- Color (Green), 3- Road name/number (Milw123) and 4-Owner (John Doe.) Items 1-3 were selected because of the ease they create while working "
                            "a yard; say during an operations session. Item 4 can help clubs and OPS hosts indentify who owns that piece of stock when there is duplicate stock "
                            "with identical markings.\n\nSerialRFID is not integrated with JMRI but it does haave a 'hook' into its XML files so that if you have entered your "
                            "engines, cars and locations that information can be pulled into SerialRFID and even send that information to a RFID chip without having to "
                            "manually reenter all that data. Details are explained in the manual.\n" )
                       self.main_pane(self.text)
                       self.image("rfid_pic.jpg")
        
           def locations_intro(self, event):  
                       '''About text explains what locations are.'''
                       self.sPanel.visible = False
                       self.tPanel.visible = False
                       self.text = ("\nSerial RFID Locations:\n\n "
                            "SerialRFID requires at least reader 'A' be installed to be meaningful at all. As a result a permanent location and track "
                            " are also provided. Locationscan be as simple as a list of readers (See Readers menu) referred to by address (Or given textual "
                            "ames) or they can be a mixed with JMRI location names.\n\nJMRI Mode -- Displays a read-only list of all the locations entered "
                            "into JMRI. No assignments to readers is provided since the program does not store 'Drop' and 'Pull' information in this mode.\n\n"
                            "Stand Alone Mode -- Cars and Engines 'drops' and 'pulls' are recorded. Give names to readers and Link to JMRI locations are available features.\n")
                       self.main_pane(self.text)
                       self.image("locations_pic.jpg")  
        
           def engines_intro(self, event):  
                       '''About text explains what engines are.'''
                       self.sPanel.visible = False
                       self.tPanel.visible = False
                       self.text = ("\nSerial RFID Engines:\n\n" 
                            "SerialRFID uses the term engines to avoid conflict with JMRI Trains. Engines are used to move cars between readers so they can be dropped at a reader "
                            "(location) or pulled from a location and added to an engine.\n\nThis is normally done at a reader local control panel and they are added to the program "
                            "as more of a maintenance function.\n\nIt's probably best to look at the user of SerialRFID as a Yardmaster and engines become easy ways for the user "
                            "to move cars between readers without resorting to the five finger airlift.\n")
                       self.main_pane(self.text)
                       self.image("engine_pic.jpg")

           def readers_intro(self, event):  
                       '''About text explains what readers are.'''
                       self.sPanel.visible = False
                       self.tPanel.visible = False
                       self.text = ("\nSerial RFID Readers:\n\n"
                            "Readers are the heart and soul of the program and it's why you use the program at all, so the requirement of at least one reader should be self-explanatroy.\n"
                            "The program must have a reader 'A' and since this is the minimum amount of readers required all write operations to a RFID tag are performed"
                            "only to this reader. By default the Arduino code will assign the address 'A' to all readers to accommodate this requirement. Adding more than one reader"
                            "will require changing the reader address.\n") 
                       self.main_pane(self.text)
                       self.image("readers_pic.jpg")
    
           def cars_intro(self, event):  
                       '''About text explains what cars are.'''
                       self.sPanel.visible = False
                       self.tPanel.visible = False
                       self.text = ("\nSerial RFID Cars:\n\n"
                        "It's all about the Cars!\nCar movement is the whole purpose of an operations session. SerialRFID allows you to manually enter cars and/or import cars "
                        "from JMRI. The status of cars is remembered between sessions (attached to an engine or left at a location.)") 
                       self.main_pane(self.text)
                       self.image("cars_pic.jpg")
    
           def mode_intro(self, event):  
                       '''About text explains what modes are available.'''
                       self.sPanel.visible = False
                       self.tPanel.visible = False
                       self.text = ("'\nSerial RFID Modes:\n\n "
                        "Mode selection alters many of the Menu Bar selections depending on the selected mode. These changes are discussed under the affected menu sections. "
                        "Think of the 'Mode' as a menu filter..\n\nStand Alone -- Will enable menu options in Polling,Locations, Engines and Cars."
                        "\n\nJMRI -- Since this mode is meant to augment JMRI Operations 'Polling' and 'Readers' are disabled and Locations, Engines, Cars will display "
                        " read-only lists of entries pulled directly from the JMRI XML files. To use this mode requires that you have set the path to the JMRI files "
                        " using the 'Configure' menu option. There is one active menu selection under 'Cars', (Assign RFID tag to Car) which is detailed under that menu selection.\n")
                       self.main_pane(self.text)
                       self.image("mode_pic.jpg")
        
           def poll_intro(self, event):  
                       '''About text explains turning on & off polling.'''
                       self.sPanel.visible = False
                       self.tPanel.visible = False
                       self.text = ("\n'Serial RFID Polling:\npolling is displayed on the far right side of the status bar.\n\n JMRI mode:\nIn this mode it will "
                       "display 'Pollling is Idle' as this mode only sends commands to reader 'A' on an as needed basis.\n\nStand Alone Mode:\n"
                       "this mode displays polling as a toggle between a reader address and the ampersand sign(@). The address shows where in the repeating "
                       "cycle the program is querying. while the ambersand indicates that a reply has been received. If the user selects to disable polling the "
                       "display updates to 'Polling Disabled'. If there is a problem with the polling the program displays a popup asking the userto check the COMM"
                       " port and field connections. Then the display updtaes to show 'Polling is Disabled'.\n")
                       self.main_pane(self.text)
                       self.image("polling_pic.jpg")
           
           def create_menus(self):
                       '''Main frame menu items I filtered at the menu level to ease future feature changes per mode. Menu visibility set to
                       stand alone mode for program start.'''
                       self.menu = JMenu('File')
                       self.menu.add(JMenuItem('About Serial RFID', actionPerformed=self.rfid_intro))
                       self.menu.add(JMenuItem('Configure', actionPerformed=self.menu_pick))
                       self.menu.add(JMenuItem('Import JMRI Files', actionPerformed=self.menu_pick))
                       self.menu.add(JMenuItem('Exit', actionPerformed=self.menu_pick))
                       
                       self.menu00 = JMenu('Polling')
                       self.menu00.add(JMenuItem('About Polling', actionPerformed=self.poll_intro))
                       
                       self.menu0 = JMenu('Polling')
                       self.menu0.add(JMenuItem('About Polling', actionPerformed=self.poll_intro))
                       self.enable = JRadioButtonMenuItem('Enable Polling', actionPerformed=self.menu_pick, selected=1)
                       self.disable = JRadioButtonMenuItem('Disable Polling', actionPerformed=self.menu_pick)
                       self.b0Group = ButtonGroup()
                       self.b0Group.add(self.enable)
                       self.b0Group.add(self.disable)
                       self.menu0.add(self.enable)
                       self. menu0.add(self.disable)
                       
                       self.menu1 = JMenu('Mode')
                       self.menu1.add(JMenuItem('About modes', actionPerformed=self.mode_intro))
                       self.alone = JRadioButtonMenuItem('Stand Alone', actionPerformed=self.menu_pick)
                       self.jmri = JRadioButtonMenuItem('JMRI', actionPerformed=self.menu_pick)
                       self.bGroup = ButtonGroup()
                       self.bGroup.add(self.alone)
                       self.bGroup.add(self.jmri)
                       self.menu1.add(self.alone)
                       self. menu1.add(self.jmri)

                       self.menu2 = JMenu('Locations',visible=0)
                       self.menu2.add(JMenuItem('About RFID Locations', actionPerformed=self.locations_intro))
                       self.menu2.add(JMenuItem('List all JMRI Locations', actionPerformed=self.menu_pick))
                      

                       self.menu2a = JMenu('Locations',visible=1)
                       self.menu2a.add(JMenuItem('About RFID Locations', actionPerformed=self.locations_intro))
                       self.menu2a.add(JMenuItem('List Cars from a Reader', actionPerformed=self.menu_pick))
                       self.menu2a.add( JMenuItem('Add Text Location to a Reader', actionPerformed=self.menu_pick))
                       self.menu2a.add(JMenuItem('Link JMRI Location to a Reader', actionPerformed=self.menu_pick))

                       self.menu3 = JMenu('Engines')
                       self.menu3.add(JMenuItem('About RFID Engines', actionPerformed=self.engines_intro))
                       self.menu3.add(JMenuItem('List All JMRI Engines', actionPerformed=self.menu_pick))
                       
                       self.menu3a = JMenu('Engines')
                       self.menu3a.add(JMenuItem('About RFID Engines', actionPerformed=self.engines_intro))
                       self.menu3a.add(JMenuItem('Create Engine', actionPerformed=self.menu_pick))
                       self.menu3a.add(JMenuItem('Asign to location', actionPerformed=self.menu_pick))
                       self.menu3a.add(JMenuItem('Pick up Drop off Car', actionPerformed=self.menu_pick))
                       self.menu3a.add(JMenuItem('List Cars in Engine', actionPerformed=self.menu_pick))
                       self.menu3a.add(JMenuItem('Terminate Engine', actionPerformed=self.menu_pick))
                       self.menu3a.add(JMenuItem('Delete Engine', actionPerformed=self.menu_pick))
                     
                       self.menu4 = JMenu('Readers',visible=1)
                       self.menu4.add(JMenuItem('About RFID Readers', actionPerformed=self.readers_intro))
                       self.menu4.add(JMenuItem('Set Active Reader', actionPerformed=self.menu_pick))
                       self.menu4.add(JMenuItem('Add reader', actionPerformed=self.menu_pick))
                       self.menu4.add(JMenuItem('Delete reader', actionPerformed=self.menu_pick))
                       
                       self.menu5 = JMenu('Cars',visible=0)
                       self.menu5.add(JMenuItem('About RFID Cars', actionPerformed=self.cars_intro))
                       self.menu5.add(JMenuItem('List all JMRI Cars', actionPerformed=self.menu_pick))
                       self.menu5.add(JMenuItem('Assign RFID tag to Car', actionPerformed=self.menu_pick))
                       
                       self.menu5a = JMenu('Cars',visible=1)
                       self.menu5a.add(JMenuItem('About RFID Cars', actionPerformed=self.cars_intro))
                       self.menu5a.add(JMenuItem('Stand Alone Mode Car Programming', actionPerformed=self.menu_pick))
                       self.menu5a.add(JMenuItem('Delete Car', actionPerformed=self.menu_pick))

                       self.menubar = JMenuBar()
                       self.menubar.add(self.menu)
                       self.menubar.add(self.menu00)
                       self.menubar.add(self.menu0)
                       self.menubar.add(self.menu1)
                       self.menubar.add(self.menu2)
                       self.menubar.add(self.menu2a)
                       self.menubar.add(self.menu3)
                       self.menubar.add(self.menu3a)
                       self.menubar.add(self.menu4)
                       self.menubar.add(self.menu5)
                       self.menubar.add(self.menu5a)

                       self.setJMenuBar(self.menubar)

           def rec_data_error(self):
                    '''no reply from comm port'''
                    #print "show dialog"
                    set_polling(False)  # variable -- turn off polling so message stops popping up
                    showMessageDialog('The selected Comm port is not receiving a reply from the field device.\n'
                    'Please check that you have selected the correct port\n OR\nconnections to field devices',"Comm Port Error 2")
                    #set_polling(False)    
        
class Runnable(Runnable):
           def __init__(self, runFunction):
                       self._runFunction = runFunction

           def run(self):
                       self._runFunction()
                       
def startup():
   open_configuration()      # from configRFID.py



    
if __name__ == '__main__':
    print "running desktop"
    startup()
    time.sleep(.1)
    SwingUtilities.invokeLater(Runnable(DesktopFrame))
    '''
    demo = DesktopFrame()
    demo.setLocation(30, 30)
    demo.show()
    comm = "COM4"
    global comPort
    comPort = MyCommPort()
    comPort.set_port(comm)
    poll = Polling(comPort)
    poll.start()
    poll.join()'''
    '''