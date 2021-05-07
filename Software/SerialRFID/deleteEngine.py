from  javax.swing import *
from  java.awt import *
from  java.awt.event import *
from variables import *
from basicImportedData import *
import sys

class DeleteEngine(JDialog):
    
    def __init__(self):
        global noRadioButton
        noRadioButton = True
        global engineClick
        engineClick = ""

        JDialog.__init__(self, None, 'Delete an engine from the system', True)
        self.setSize(600,375)
        self.setLayout(BorderLayout())
        self.setLocation(100,100)
        self.preferredSize = 600,375
        self.setBackground(Color.LIGHT_GRAY)
        
        self.northPanel = JPanel()
        noteText = JLabel('Available Engines')
        noteText.setForeground(Color.decode("#000dff"))
        noteText.setBackground(Color.decode("#000000"))
        noteText.setFont(Font("Serif", Font.PLAIN, 24))
        self.northPanel.add(noteText)
        self.add(self.northPanel,BorderLayout.NORTH)
        
        self.centerPanel = JPanel()
        self.centerPanel.add(self.get_engine_list())
        self.add(self.centerPanel,BorderLayout.CENTER) 
        
        self.eastPanel = JPanel()
        self.eastPanel.preferredSize = (Dimension(250,100))
        self.cancel = JButton('Cancel', actionPerformed = self.cancel_dialog)
        self.assign = JButton(' Delete ', actionPerformed = self.link_box)
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
        newText = 'Select an engine to delete from the system'
        self.assignText = JLabel(newText, SwingConstants.CENTER)
        self.assignText.setForeground(Color.decode("#000dff"))
        self.assignText.setBackground(Color.decode("#000000"))
        self.assignText.setFont(Font("Serif", Font.PLAIN, 24))
        self.textPanel = JPanel()
        self.textPanel.setLayout(BoxLayout(self.textPanel, BoxLayout.X_AXIS))
        self.textPanel.preferredSize = (Dimension(420,50))
        self.textPanel.add(self.assignText)
        
        self.southPanel.add(self.textPanel)
        self.add(self.southPanel,BorderLayout.SOUTH)
        
        self.setVisible(True)
       

    def on_click2(self, event):    # engine
            global engineClick
            global noRadioButton
            label2 = event.getActionCommand()
            a2 = label2.split(".")
            engineClick = a2[0].strip()  # engine id
            if engineClick == "PERM1":
                showMessageDialog('Do not delete\nThis is an internal engine that cannot be deleted.\n ',"Deletion Error")
                noRadioButton = True
                #print "************    engine = ", engineClick
            else:
                noRadioButton = False
                #print "************    engine = ", engineClick
            

    def get_engine_list(self):
         '''make a radio button for every engine '''
         engineList = basic_get_list_of_engines()    # variables
         print "enginelist = ", engineList
         self.boxPanel2 = JPanel()
         self.boxPanel2.setLayout(BoxLayout(self.boxPanel2, BoxLayout.Y_AXIS))
         self.boxPanel2.preferredSize = (Dimension(250,300))
         try: 
             self.group2 = ButtonGroup()
             for engine in engineList:                                                       
                     text = engine[6] + ".   " + engine[2] + "   " + engine[1] + " " + engine[5]      
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
             print "deleteEngine.py --  something wrong with get_engine_list"
             print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]
         

    def link_box(self, event):    
            global engineClick  # engine id
            print "engine ID = ", engineClick
            global noRadioButton
            if noRadioButton:
                showMessageDialog('An Engine \n'
                    'must be selected before a deletion can be performed.\n ',"Deletion Error")
                return 
            basic_delete_engine(engineClick)
            noRadioButton = True
            self.dispose()
        
    def cancel_dialog(self, event):
            self.dispose()