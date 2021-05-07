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

        
class ListAllJmriEngines(JDialog):
    def __init__(self):
        global changes
        changes = []
        JDialog.__init__(self, None, 'List of Engines from JMRI Operations rosters', True)
        #self.setDefaultCloseOperation(DO_NOTHING_ON_CLOSE)
        self.setSize(1100,330)
        self.setLayout(BorderLayout())
        self.setLocation(100,100)
        self.preferredSize = (Dimension(1100,330))
        self.setBackground(Color.LIGHT_GRAY)
        
        northPanel = JPanel()
        titleText = JLabel('                                      Engines                                     ')
        titleText.setForeground(Color.decode("#000dff"))
        titleText.setBackground(Color.decode("#000000"))
        titleText.setFont(Font("Serif", Font.PLAIN, 24))
        northPanel.add(titleText)
        self.add(northPanel,BorderLayout.NORTH)
        
        southPanel = JPanel()
        noteText = JLabel('   This is a read-only display of all JMRI engines ')
        noteText.setForeground(Color.decode("#000dff"))
        noteText.setBackground(Color.decode("#000000"))
        noteText.setFont(Font("Serif", Font.PLAIN, 20))
        southPanel.add(noteText)
        self.add(southPanel,BorderLayout.SOUTH)   

        westPanel = JPanel()
        westPanel.setPreferredSize(Dimension(25,25))
        westPanel.setLayout(BoxLayout(westPanel, BoxLayout.X_AXIS))
        westPanel.add(Box.createVerticalGlue())
        westPanel.add(Box.createRigidArea(Dimension(25, 25)))
        self.add(westPanel,BorderLayout.WEST)
        
        eastPanel = JPanel()
        eastPanel.setLayout(BoxLayout(eastPanel, BoxLayout.Y_AXIS))
        eastPanel.preferredSize = (Dimension(25,25))
        eastPanel.add(Box.createRigidArea(Dimension(25, 25)))
        self.add(eastPanel,BorderLayout.EAST)
        
        centerPanel = JPanel()
        centerPanel.setLayout(BoxLayout(centerPanel, BoxLayout.Y_AXIS))
        centerPanel.setPreferredSize(Dimension(900,330))
        
        combinedPanel = JPanel()
        combinedPanel.setLayout(BoxLayout(combinedPanel, BoxLayout.X_AXIS))
        combinedPanel.setPreferredSize(Dimension(600,330))
        
        enginePanel = JPanel()
        enginePanel.setLayout(BoxLayout(enginePanel, BoxLayout.Y_AXIS))
        enginePanel.setPreferredSize(Dimension(850,330))
        enginePanel.add(self.add_engine_table())
        combinedPanel.add(enginePanel)
        '''
        carPanel = JPanel()
        carPanel.setLayout(BoxLayout(carPanel, BoxLayout.Y_AXIS))
        carPanel.setPreferredSize(Dimension(550,330))
        carPanel.add(self.add_car_table())
        combinedPanel.add(carPanel)
        '''
        centerPanel.add(combinedPanel)
        cancel = JButton('Close', actionPerformed = self.cancel_data)
        centerPanel.add(cancel)
        centerPanel.add(Box.createRigidArea(Dimension(25, 25)))
        self.add(centerPanel,BorderLayout.CENTER)
        self.setVisible(True)
    '''    
    def add_car_table(self):
            colNames = ('Type',"Color","Road Name", "Road Number")
            dataModel = DefaultTableModel(sort_car_data(), colNames)
            self.table = JTable(dataModel)
            self.table.getTableHeader().setReorderingAllowed(0)
            self.table.setSelectionMode(0)
            scrollPane = JScrollPane()
            scrollPane.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_ALWAYS)
            scrollPane.setPreferredSize(Dimension(330,125))
            scrollPane.getViewport().setView(self.table)
            panel = JPanel()
            panel.preferredSize = (Dimension(330,200))
            panel.add(scrollPane)
            return panel
     '''   
    def add_engine_table(self):
            colNames = ('Type',"Model","Road Name", "Road Number")
            dataModel = DefaultTableModel(sort_engine_data(), colNames)
            self.table = JTable(dataModel)
            self.table.getTableHeader().setReorderingAllowed(0)
            self.table.setSelectionMode(0)
            scrollPane = JScrollPane()
            scrollPane.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_ALWAYS)
            scrollPane.setPreferredSize(Dimension(850,125))
            scrollPane.getViewport().setView(self.table)
            panel = JPanel()
            panel.preferredSize = (Dimension(900,200))
            panel.add(scrollPane)
            return panel
        
    def cancel_data(self, event):
        self.dispose()
'''        
def sort_car_data():
    Sort installed readers list for table display
     print "got to sort sa data"
     try:
         allCars = get_jmri_cars()
         temp = []
         carData = []
         for shrink in allCars:
             temp = []
             temp.append(shrink[1])
             temp.append(shrink[2])
             temp.append(shrink[3])
             temp.append(shrink[4])
             carData.append(temp)
         return carData
     except:
         print "something wrong with sort_car_data"
         print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]
'''
def sort_engine_data():
     '''Sort installed readers list for table display'''
     print "got to sort sa data"
     try:
         allEngines = get_jmri_engines()
         temp = []
         engineData = []
         for shrink in allEngines:
             temp = []
             temp.append(shrink[1])
             temp.append(shrink[2])
             temp.append(shrink[3])
             temp.append(shrink[4])
             engineData.append(temp)
         return engineData
     except:
         print "something wrong with sort_engine_data"
         print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]

        
if __name__ == "__main__":
    print "Running readerGUI.py"
        