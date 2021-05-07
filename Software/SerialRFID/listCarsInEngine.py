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

        
class ListCarsInEngine(JDialog):
    def __init__(self):
        global changes
        changes = []
        JDialog.__init__(self, None, 'List of SerialRFID Engines with manifest', True)
        #self.setDefaultCloseOperation(DO_NOTHING_ON_CLOSE)
        self.setSize(925,350)
        self.setLayout(BorderLayout())
        self.setLocation(100,100)
        self.preferredSize = (Dimension(1100,350))
        self.setBackground(Color.LIGHT_GRAY)
        
        self.northPanel = JPanel()
        self.titleText = JLabel('   Select Engine                                                            Manifest       ')
        self.titleText.setForeground(Color.decode("#000dff"))
        self.titleText.setBackground(Color.decode("#000000"))
        self.titleText.setFont(Font("Serif", Font.PLAIN, 24))
        self.northPanel.add( self.titleText)
        self.add( self.northPanel,BorderLayout.NORTH)
        
        self.southPanel = JPanel()
        self.noteText = JLabel("   Select engine row, click 'Update Manifest', and car table will refresh.  ")
        self.noteText.setForeground(Color.decode("#000dff"))
        self.noteText.setBackground(Color.decode("#000000"))
        self.noteText.setFont(Font("Serif", Font.PLAIN, 20))
        self.southPanel.add( self.noteText)
        self.add( self.southPanel,BorderLayout.SOUTH)   

        self.westPanel = JPanel()
        self.westPanel.setPreferredSize(Dimension(25,25))
        self.westPanel.setLayout(BoxLayout( self.westPanel, BoxLayout.X_AXIS))
        self.westPanel.add(Box.createVerticalGlue())
        self.westPanel.add(Box.createRigidArea(Dimension(25, 25)))
        self.add( self.westPanel,BorderLayout.WEST)
        
        self.eastPanel = JPanel()
        self.eastPanel.setLayout(BoxLayout( self.eastPanel, BoxLayout.Y_AXIS))
        self.eastPanel.preferredSize = (Dimension(25,25))
        self.eastPanel.add(Box.createRigidArea(Dimension(25, 25)))
        self.add( self.eastPanel,BorderLayout.EAST)
        
        self.centerPanel = JPanel()
        self.centerPanel.setLayout(BoxLayout( self.centerPanel, BoxLayout.Y_AXIS))
        self.centerPanel.setPreferredSize(Dimension(600,375))
        
        self.combinedPanel = JPanel()
        self.combinedPanel.setLayout(BoxLayout( self.combinedPanel, BoxLayout.X_AXIS))
        self.combinedPanel.setPreferredSize(Dimension(600,330))
        
        self.enginePanel = JPanel()
        self.enginePanel.setLayout(BoxLayout( self.enginePanel, BoxLayout.Y_AXIS))
        self.enginePanel.setPreferredSize(Dimension(550,330))
        self.enginePanel.add(self.add_engine_table())
        self.combinedPanel.add( self.enginePanel)
        
        self.carPanel = JPanel()
        self.carPanel.setLayout(BoxLayout( self.carPanel, BoxLayout.Y_AXIS))
        self.carPanel.setPreferredSize(Dimension(550,330))
        global FirstTime
        FirstTime = True
        self.carPanel.add(self.add_car_table('SerialRFID'))
        self.combinedPanel.add( self.carPanel)
        
        self.centerPanel.add( self.combinedPanel)
        #self.centerPanel.add(Box.createRigidArea(Dimension(25, 25)))
        
        self.close = JButton('Close', actionPerformed = self.close_dialog)
        self.update = JButton('Update Manifest', actionPerformed = self.update_manifest)
        self.controlPanel = JPanel()
        self.controlPanel.setLayout(BoxLayout( self.controlPanel, BoxLayout.X_AXIS))
        self.controlPanel.setPreferredSize(Dimension(550,50))
        self.controlPanel.add( self.update)
        self.controlPanel.add(Box.createRigidArea(Dimension(25, 25)))
        self.controlPanel.add( self.close)
        
        self.centerPanel.add( self.controlPanel)
        
        self.centerPanel.add(Box.createRigidArea(Dimension(25, 25)))
        self.add( self.centerPanel,BorderLayout.CENTER)
        self.setVisible(True)
        
    def add_car_table(self, forEngine):
            self.colNames = ('Type',"Color","Road Name", "Road Number")
            self.dataModel = DefaultTableModel( self.sort_car_data(forEngine), self.colNames)
            self.carTable = JTable( self.dataModel)
            self.carTable.getTableHeader().setReorderingAllowed(0)
            self.carTable.setSelectionMode(0)
            self.scrollPane = JScrollPane()
            self.scrollPane.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_ALWAYS)
            self.scrollPane.setPreferredSize(Dimension(330,125))
            self.scrollPane.getViewport().setView(self.carTable)
            self.panel = JPanel()
            self.panel.preferredSize = (Dimension(330,200))
            self.panel.add(self.scrollPane)
            return self.panel
        
    def add_engine_table(self):
            self.colNames = ('Type',"Model","Road Name", "Road Number")
            self.dataModel = DefaultTableModel(self.sort_engine_data(), self.colNames)
            self.engineTable = JTable(self.dataModel)
            self.engineTable.getTableHeader().setReorderingAllowed(0)
            self.engineTable.setSelectionMode(0)
            self.engineTable.setRowSelectionInterval(0, 0)
            self.scrollPane = JScrollPane()
            self.scrollPane.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_ALWAYS)
            self.scrollPane.setPreferredSize(Dimension(330,125))
            self.scrollPane.getViewport().setView(self.engineTable)
            self.panel = JPanel()
            self.panel.preferredSize = (Dimension(330,200))
            self.panel.add(self.scrollPane)
            return self.panel
        
    def update_manifest(self, event):
        try:
            self.allEngines = basic_get_list_of_engines()
            #self.allCars = basic_get_cars_for_pull_drop(forEngine)
            self.a = self.engineTable.getSelectedRow()
            #print "selected row = ",a
            self.delAddress = self.engineTable.getValueAt(self.a,0)   
            self.upDate = self.allEngines[self.a]
            self.update_manifest_table(self.upDate[6])
        except:
             print "something wrong with update manifest"
             print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]
            
    def close_dialog(self, event):
        self.dispose()
       
    def update_manifest_table(self, forEngine):
        #print "got to update manifest table"
        self.combinedPanel.remove(self.carPanel)
        self.revalidate()
        self.carPanel = JPanel()
        self.carPanel.setLayout(BoxLayout( self.carPanel, BoxLayout.Y_AXIS))
        self.carPanel.setPreferredSize(Dimension(550,330))
        self.carPanel.add(self.add_car_table(forEngine))
        self.combinedPanel.add( self.carPanel)
        self.revalidate()
        self.repaint() 
        
    def sort_car_data(self, forEngine):
      '''Sort installed readers list for table display'''
      #print "got to car sort data"
      try:
         global FirstTime  
         print "*********   forEngine = ", forEngine
         self.carData = []
         if FirstTime == True:
             self.carData = [["","","",""]] # open dialog with empty list
             FirstTime = False
             return self.carData
         self.carList = basic_get_cars_for_pull_drop(forEngine)
         print "carList = ", self.carList
         size = len(self.carList)
         print "size = ", size
         if size > 0:
             #self.allCars = get_serial_rfid_cars()
             self.temp = []
             self.temp = []
             for shrink in self.carList:
                 self.temp.append(shrink[1])
                 self.temp.append(shrink[2])
                 self.temp.append(shrink[3])
                 self.temp.append(shrink[4])
                 self.carData.append(self.temp)
                 self.temp = []
         else:
             self.carData = [["-","-","-","-"]]
         print "carData = ", self.carData
         return self.carData
      except:
         print "something wrong with sort_car_data"
         print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]

    def sort_engine_data(self):
         '''Sort installed readers list for table display'''
         #print "got to engine sort data"
         try:
             self.allEngines = basic_get_list_of_engines()
             self.temp = []
             self.engineData = []
             for shrink in self.allEngines:
                 self.temp = []
                 self.temp.append(shrink[1])
                 self.temp.append(shrink[2])
                 self.temp.append(shrink[3])
                 self.temp.append(shrink[4])
                 self.engineData.append(self.temp)
             return self.engineData
         except:
             print "something wrong with sort_engine_data"
             print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]

        
if __name__ == "__main__":
    print "Running readerGUI.py"
        