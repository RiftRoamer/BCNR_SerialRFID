from  javax.swing import *
from  java.awt import *
from  java.awt.event import *
from variables import *
from configRFID import *
from java.awt import BorderLayout;
from java.awt import Color;
from swingutils.dialogs.basic import showMessageDialog
#global wholeList
#wholeList = []
global cbList
cbList =[]
global noRadioButton
noRadioButton = True
global toCar
toCar = 'yes'  # by default write the data to a RFID tag on reader A

class StandAloneProgramming(JDialog):
    def __init__(self):
        JDialog.__init__(self, None, 'Stand Alone Mode Car Programming', True)
        self.setSize(1200,500)
        self.setLayout(BorderLayout())
        self.setLocation(100,100)
        self.preferredSize = 1000,500
        self.setBackground(Color.LIGHT_GRAY)
        
        self.northPanel = JPanel()
        self.noteText = JLabel('                  Create Car        ')
        self.noteText.setForeground(Color.decode("#000dff"))
        self.noteText.setBackground(Color.decode("#000000"))
        self.noteText.setFont(Font("Serif", Font.PLAIN, 24))
        self.northPanel.add(self.noteText)
        self.add(self.northPanel,BorderLayout.NORTH)
        
        self.southPanel = JPanel()
        self.titleText = JLabel("   Create Stand Alone Mode Car   ")
        self.titleText.setForeground(Color.decode("#000dff"))
        self.titleText.setBackground(Color.decode("#000000"))
        self.titleText.setFont(Font("Serif", Font.PLAIN, 20))
        self.southPanel.add(self.titleText)
        self.add(self.southPanel,BorderLayout.SOUTH)
        
        self.eastPanel = JPanel()
        self.eastPanel.setLayout(BoxLayout(self.eastPanel, BoxLayout.Y_AXIS))
        self.eastPanel.preferredSize = (Dimension(250,100))

        self.cancel = JButton('Cancel', actionPerformed = self.cancel_data)
        self.create    = JButton(' Create ', actionPerformed = self.save_data)
        self.eastPanel.add(Box.createRigidArea(Dimension(50, 10)))
        self.comboPanel = JPanel()
        self.comboPanel.setLayout(BoxLayout(self.comboPanel, BoxLayout.X_AXIS))
        self.comboPanel.preferredSize = (Dimension(25,25))

        self.eastPanel.add(self.comboPanel)
        self.eastPanel.add(self.create)
        self.eastPanel.add(Box.createRigidArea(Dimension(25, 10)))
        self.eastPanel.add(self.cancel)
        self.add(self.eastPanel,BorderLayout.EAST)
        
        self.bPanel = JPanel()
        self.bPanel.setLayout(BoxLayout(self.bPanel, BoxLayout.Y_AXIS))
        self.bPanel.preferredSize = (Dimension(100,100))
        self.internal = JRadioButton('Add for internal use only', actionPerformed=self.record)
        self.tag = JRadioButton('Add & write data to RFID tag', actionPerformed=self.record)
        self.bGroup = ButtonGroup()
        self.bGroup.add(self.internal)
        self.bGroup.add(self.tag)
        self.tag.selected = 1
        self.bPanel.add(Box.createRigidArea(Dimension(25, 50)))
        self.bPanel.add(self.internal)
        self.bPanel.add(Box.createRigidArea(Dimension(25, 10)))
        self. bPanel.add(self.tag)
        self.eastPanel.add(self.bPanel)
        
        self.add(self.eastPanel,BorderLayout.EAST)
        
        
        
        
        
        
        
        
        self.westPanel = JPanel()
        self.westPanel.setLayout(BoxLayout(self.westPanel, BoxLayout.X_AXIS))
        self.westPanel.add(Box.createRigidArea(Dimension(10, 25)))
        self.westPanel.preferredSize = (Dimension(350,350))
        self.helpText = self.help_column()
        self.westPanel.add(Box.createRigidArea(Dimension(10, 25)))
        self.westPanel.add(self.helpText)
        self.add(self.westPanel,BorderLayout.WEST)
        
        self.centerPanel = JPanel()
        self.centerPanel.setLayout(BoxLayout(self.centerPanel, BoxLayout.Y_AXIS))
        self.centerPanel.preferredSize = (Dimension(125,1))
        self.checkPanel = JPanel()
        self.checkPanel.setLayout(BoxLayout(self.checkPanel, BoxLayout.X_AXIS))
        self.checkPanel.setPreferredSize(Dimension(350,300))
        self.checkPanel.add(self.make_text_fields())
        self.centerPanel.add(self.checkPanel)    
        self.add(self.centerPanel,BorderLayout.CENTER)
        self.pack()
        self.setVisible(True)
        set_linked_gui(self)   #add to variable
        
    def help_column(self):
       ''' Put 'how to' text into west panel'''
       self.text = ("'Creating a Car:\n\n"
            "Stand Alone Mode Car Programming -- \nNo connection to JMRI is supported in this mode. The user is presented with input boxes to provide "
            "the needed data (Road name, road number, etc) and Serial RFID performs only a single WRITE operation to record the supplied data to the rfid "
            "tag placed on reader 'A'. Now this piece of rolling stock has all the information that a Serial RFID reader needs for a proper display.\n"
            "\n\nCreate: -- Initiates the write to the car sitting on reader A\n\n Cancel: -- closes the window and discards all data"
            )
       self.mainText = JTextArea()
       self.mainText.text = self.text
       self.mainText.lineWrap = True
       self.mainText.wrapStyleWord = True
       self.mainText.setSize(300, 350)
       self.mainText.setBackground(Color.LIGHT_GRAY)
       self.mainText.setCaretPosition(0);
       self.mainScroll = JScrollPane(self.mainText)
       self.mainScroll.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_ALWAYS)
       self.mainScroll.setPreferredSize(Dimension(325, 350))
       self.mainScroll.getViewport().setView((self.mainText))
       self.mainPanel = JPanel()
       self.mainPanel.setBackground(Color.LIGHT_GRAY)
       self.mainPanel.add(self.mainScroll)
       return self.mainPanel  
        
    def update_display(self):
        self.centerPanel.remove(self.checkPanel)
        self.revalidate()
        self.checkPanel = JPanel()
        self.checkPanel.setLayout(BoxLayout(self.checkPanel, BoxLayout.X_AXIS))
        self.checkPanel.setPreferredSize(Dimension(350,300))
        self.checkPanel.add(self.make_text_fields())
        self.centerPanel.add(self.checkPanel)
        self.revalidate()
        self.repaint()

    def cancel_data(self, event):
        self.dispose()
     
    def record(self, event):
        print "got to record event"
        if self.internal.isSelected():
              print "*********  internal selected"
              global toCar
              toCar = 'no'
        else:
              print "*********  TAG selected"
              global toCar
              toCar = 'yes'     
        
    def save_data(self, event):
        if len(self.ids.text) == 0:
            showMessageDialog('Please enter a Car ID to allow the program to track this car.\n'
            'this is usually a mix of the Road Name and Road number; such as MILW123',"Car ID Required")
            return
    #set_polling(False)
        passCar = []
        trimCar = []
        global toCar
        if toCar == 'yes':
            tag = self.get_car_rfid_tag()         #[0] returned RFID tag
            #print "to car tag = ", tag
            if tag != "none":
                stripTag = tag[5:]
                passCar.append(stripTag)               # [0] rfid
                passCar.append(self.types.text)      # [1] type
                passCar.append(self.color.text)     # [2] model
                passCar.append(self.names.text)    # [3] road name
                passCar.append(self.number.text)  # [4] road number
                passCar.append(self.owners.text)   # [5] owner
                passCar.append(self.ids.text)          # [6] id
                tag2  = self.write_data_to_car_rfid_tag(passCar)
        else:
            tag2 = "pass"
            trimCar.append(self.types.text)
            trimCar.append(self.color.text)
            trimCar.append(self.names.text)
            trimCar.append(self.number.text)
            trimCar.append(self.owners.text)
            trimCar.append(self.ids.text)

            for item in trimCar:
                a = (item[0:16])
                b = len(a)
                if b == 0:
                    a = "################"
                passCar.append(a)
        
        print passCar
        if tag2 != "none":
            basic_create_car_tags(passCar)
            self.update_display()   # empty all fields

    def get_car_rfid_tag(self):
        command = ['*A04']
        set_xmit_cmd(command)
        time.sleep(.03)
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
            tag = "none"
            print "standAloneProgramming.py -- reply from get_car_rfid_tag timer timed out"
        return tag
            
    def make_text_fields(self):
     '''make a textarea for every data point '''
     self.tag = JTextField('fixed in tag',16)
     self.tag.setEditable(False)
     self.types = JTextField(16)
     self.color = JTextField(16)
     self.names = JTextField(16)
     self.number = JTextField(16)
     self.owners = JTextField(16)
     self.ids = JTextField(16)
     
     self.tagLabel = JLabel("RFID")
     self.typesLabel = JLabel("Type")
     self.colorLabel = JLabel("Color")
     self.nameLabel = JLabel("Road Name")
     self.numberLabel = JLabel("Road Number")
     self.ownerLabel = JLabel("Owner")
     self.idLabel = JLabel("Car ID")
     self.limit = JLabel("All entries are trimmed to 16 characters")
     self.hashTag = JLabel("Empty fields will be padded with #################")
     self.fixedTag = JLabel("Car programming is limited to reader A")
     
     self.panel = JPanel()
     self.panel.setLayout(BoxLayout(self.panel, BoxLayout.Y_AXIS))
     self.panel.setPreferredSize(Dimension(350,300))
     
     self.panel0 = JPanel()
     self.panel0.setLayout(BoxLayout(self.panel0, BoxLayout.X_AXIS))
     self.panel0.setPreferredSize(Dimension(20,10))
     self.panel0.add(Box.createRigidArea(Dimension(50, 10)))
     self.panel0.add(self.tagLabel)
     self.panel0.add(Box.createRigidArea(Dimension(10, 10)))
     self.panel0.add(self.tag)
     self.panel0.add(Box.createRigidArea(Dimension(50, 10)))
     self.panel.add(self.panel0)
     
     self.panel1 = JPanel()
     self.panel1.setLayout(BoxLayout(self.panel1, BoxLayout.X_AXIS))
     self.panel1.setPreferredSize(Dimension(20,10))
     self.panel1.add(Box.createRigidArea(Dimension(50, 10)))
     self.panel1.add(self.typesLabel)
     self.panel1.add(Box.createRigidArea(Dimension(10, 10)))
     self.panel1.add(self.types)
     self.panel1.add(Box.createRigidArea(Dimension(50, 10)))
     self.panel.add(self.panel1)
     
     self.panel2 = JPanel()
     self.panel2.setLayout(BoxLayout(self.panel2, BoxLayout.X_AXIS))
     self.panel2.setPreferredSize(Dimension(20,10))
     self.panel2.add(Box.createRigidArea(Dimension(50, 10)))
     self.panel2.add(self.colorLabel)
     self.panel2.add(Box.createRigidArea(Dimension(10, 10)))
     self.panel2.add(self.color)
     self.panel2.add(Box.createRigidArea(Dimension(50, 10)))
     self.panel.add(self.panel2)
     
     self.panel3 = JPanel()
     self.panel3.setLayout(BoxLayout(self.panel3, BoxLayout.X_AXIS))
     self.panel3.setPreferredSize(Dimension(20,10))
     self.panel3.add(Box.createRigidArea(Dimension(50, 10)))
     self.panel3.add(self.nameLabel)
     self.panel3.add(Box.createRigidArea(Dimension(10, 10)))
     self.panel3.add(self.names)
     self.panel3.add(Box.createRigidArea(Dimension(50, 10)))
     self.panel.add(self.panel3)
     
     self.panel4 = JPanel()
     self.panel4.setLayout(BoxLayout(self.panel4, BoxLayout.X_AXIS))
     self.panel4.setPreferredSize(Dimension(20,10))
     self.panel4.add(Box.createRigidArea(Dimension(50, 10)))
     self.panel4.add(self.numberLabel)
     self.panel4.add(Box.createRigidArea(Dimension(10, 10)))
     self.panel4.add(self.number)
     self.panel4.add(Box.createRigidArea(Dimension(50, 10)))
     self.panel.add(self.panel4)
     
     self.panel5 = JPanel()
     self.panel5.setLayout(BoxLayout(self.panel5, BoxLayout.X_AXIS))
     self.panel5.setPreferredSize(Dimension(20,10))
     self.panel5.add(Box.createRigidArea(Dimension(50, 10)))
     self.panel5.add(self.ownerLabel)
     self.panel5.add(Box.createRigidArea(Dimension(10, 10)))
     self.panel5.add(self.owners)
     self.panel5.add(Box.createRigidArea(Dimension(50, 10)))
     self.panel.add(self.panel5)
     
     self.panel6 = JPanel()
     self.panel6.setLayout(BoxLayout(self.panel6, BoxLayout.X_AXIS))
     self.panel6.setPreferredSize(Dimension(20,10))
     self.panel6.add(Box.createRigidArea(Dimension(50, 10)))
     self.panel6.add(self.idLabel)
     self.panel6.add(Box.createRigidArea(Dimension(10, 10)))
     self.panel6.add(self.ids)
     self.panel6.add(Box.createRigidArea(Dimension(50, 10)))
     self.panel.add(self.panel6)
     self.panel.add(Box.createRigidArea(Dimension(10, 50)))
     
     self.panelL = JPanel()
     self.panelL.setLayout(BoxLayout(self.panelL, BoxLayout.X_AXIS))
     self.panelL.setPreferredSize(Dimension(20,10))
     self.panelL.add(self.limit)
     
     self.panelH = JPanel()
     self.panelH.setLayout(BoxLayout(self.panelH, BoxLayout.X_AXIS))
     self.panelH.setPreferredSize(Dimension(20,20))
     self.panelH.add(self.hashTag)
     
     self.panelF = JPanel()
     self.panelF.setLayout(BoxLayout(self.panelF, BoxLayout.X_AXIS))
     self.panelF.setPreferredSize(Dimension(20,20))
     self.panelF.add(self.fixedTag)
     
     self.panel.add(self.panelL)
     self.panel.add(Box.createRigidArea(Dimension(10, 10)))
     self.panel.add(self.panelH)
     self.panel.add(Box.createRigidArea(Dimension(10, 10)))
     self.panel.add(self.panelF)
     self.panel.add(Box.createRigidArea(Dimension(10, 120)))
     
     return self.panel

    def write_data_to_car_rfid_tag(self, sendCar):
        tagCar = sendCar
        passCar = []
        set_send_car_to_reader(passCar)  # remove last car sent
        trimCar = []                             # tagCar[0] drop rfid not sent to tag
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
            write = "none"
            print "standAloneProgramming.py -- reply from write_data_to_car_rfid_tag timer timed out"
        return write

    def rec_write_error(self):
        '''bad reply from reader'''
        showMessageDialog('The requested WRITE to failed .\n'
        'Please check that you have positioned the car correctly\n AND\nthat you are using Reader A',"Car write Error")      

if __name__ == "__main__":
    print "Running engineJmriGUI.py"
