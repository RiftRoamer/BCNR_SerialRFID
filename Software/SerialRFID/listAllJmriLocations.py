from  javax.swing import *
from  java.awt import *
from  java.awt.event import *
from variables import *
from javax.swing.table import DefaultTableModel
import sys
from importFiles import *
from JMRIlistAll import *

class ListAllJmriLocations(JDialog):
    def __init__(self):
        JDialog.__init__(self, None, 'All JMRI Locations', True)
        #self.setDefaultCloseOperation(DO_NOTHING_ON_CLOSE)
        self.setSize(900,250)
        self.setLayout(BorderLayout())
        self.setLocation(100,100)
        self.preferredSize = 900,250
        self.setBackground(Color.LIGHT_GRAY)
        self.add(self.add_jmri_table(),BorderLayout.CENTER)
        self.setVisible(True)
       
    def add_jmri_table(self):
            
            southPanel = JPanel()
            #northPanel.setLayout(BorderLayout())
            titleText = JLabel('   This is a read-only list of all JMRI Operations locations.   ')
            titleText.setForeground(Color.decode("#000dff"))
            titleText.setBackground(Color.decode("#000000"))
            titleText.setFont(Font("Serif", Font.PLAIN, 20))
            southPanel.add(titleText)
            self.add(southPanel,BorderLayout.SOUTH)
            
            northPanel = JPanel()
            #northPanel.setLayout(BorderLayout())
            noteText = JLabel('   JMRI Operations Locations   ')
            noteText.setForeground(Color.decode("#000dff"))
            noteText.setBackground(Color.decode("#000000"))
            noteText.setFont(Font("Serif", Font.PLAIN, 24))
            northPanel.add(noteText)
            self.add(northPanel,BorderLayout.NORTH)
            
            eastPanel = JPanel()
            eastPanel.setLayout(BoxLayout(eastPanel, BoxLayout.Y_AXIS))
            eastPanel.preferredSize = (Dimension(150,1))
            cancel = JButton('Cancel', actionPerformed = self.cancel_data)
            eastPanel.add(Box.createRigidArea(Dimension(25, 25)))
            eastPanel.add(Box.createRigidArea(Dimension(25, 25)))
            eastPanel.add(cancel)
            self.add(eastPanel,BorderLayout.EAST)
 
            westPanel = JPanel()
            westPanel.setLayout(BoxLayout(westPanel, BoxLayout.Y_AXIS))
            westPanel.preferredSize = (Dimension(150,1))
            westPanel.add(Box.createRigidArea(Dimension(25, 25)))
            westPanel.add(Box.createRigidArea(Dimension(25, 25)))
            self.add(westPanel,BorderLayout.WEST)
            
            
            panel = JPanel()
            panel.setLayout(BoxLayout(panel, BoxLayout.Y_AXIS))
            panel.preferredSize = (Dimension(125,1))
            colNames = ('Location','Tracks')
            dataModel = DefaultTableModel(self.sort_jmri_data(), colNames)
            
            self.table = JTable(dataModel)
            self.table.getTableHeader().setReorderingAllowed(0)

            scrollPane = JScrollPane()
            scrollPane.setPreferredSize(Dimension(300,100))
            scrollPane.getViewport().setView((self.table))
            panel.add(scrollPane)
            return panel
       
    def cancel_data(self, event):
        #print "got to cancel data"
        global changes
        changes = []
        #print changes
        self.dispose()   
        
    def sort_jmri_data(self):
         '''Sort list of locations from Operations XML file for table display'''
         try:
             #JMRI = Locations()  #locationXML
             wholeList = get_jmri_loc_track_tags()
             self.temp = []
             self.tableData = []
             for loc in wholeList:
                 for item in loc:
                     location = isinstance(item, dict)
                     if location :
                         self.temp.append(item.get('name'))
                         self.temp.append("   ")
                         self.tableData.append(self.temp)
                         self.temp = []
                     track = isinstance(item, list)
                     if track :
                         for tracks in item:
                             self.temp.append("    ")
                             self.temp.append(tracks.get('name'))
                             self.tableData.append(self.temp)
                             self.temp = []    
             return self.tableData
         except:
             print "something wrong with sort_data"
             print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]
         
        
if __name__ == "__main__":
    print "Running locationJmriGUI.py"
    me = LocationJmriGUI()