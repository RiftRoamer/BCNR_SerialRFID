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
from basicImportedData import *
        
class EnginePickupDropoffCar(JDialog):
    def __init__(self):
        global changes
        changes = []
        link = get_rfid_eng_assign()
        global EngineID
        EngineID = link[0]
        global LocText
        LocText = link[1]
        global LocReader
        LocReader = link[2]
        print "eng = ", EngineID
        print "Loc = ", LocText
        print "reader = ", LocReader
        if EngineID == "unassigned":
            self.no_engine()
            return
        JDialog.__init__(self, None, 'Pick up or Drop off a car from this Engine', True)
        #self.setDefaultCloseOperation(DO_NOTHING_ON_CLOSE)
        self.setSize(925,350)
        self.setLayout(BorderLayout())
        self.setLocation(100,100)
        self.preferredSize = (Dimension(1100,350))
        self.setBackground(Color.LIGHT_GRAY)
        
        self.northPanel = JPanel()
        self.buildText = "    Location                                                          Engine"
        self.titleText = JLabel(self.buildText)
        self.titleText.setForeground(Color.decode("#000dff"))
        self.titleText.setBackground(Color.decode("#000000"))
        self.titleText.setFont(Font("Serif", Font.PLAIN, 24))
        self.northPanel.add( self.titleText)
        self.add( self.northPanel,BorderLayout.NORTH)
        
        self.southPanel = JPanel()
        self.southPanel.setPreferredSize(Dimension(500,75))
        self.southPanel.setLayout(BoxLayout( self.southPanel, BoxLayout.Y_AXIS))
        self.dropText = JLabel("   Drop Car -- Pick car from Engine Table to place it in the Location table. Click <-- Drop car ")
        self.dropText.setForeground(Color.decode("#000dff"))
        self.dropText.setBackground(Color.decode("#000000"))
        self.dropText.setFont(Font("Serif", Font.PLAIN, 20))
        self.southPanel.add( self.dropText)
        self.pullText = JLabel("   Pull Car -- Pick car from Location Table to place it in the Engine Table. Click Pull Car --> ")
        self.pullText.setForeground(Color.decode("#000dff"))
        self.pullText.setBackground(Color.decode("#000000"))
        self.pullText.setFont(Font("Serif", Font.PLAIN, 20))
        self.southPanel.add( self.pullText)
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
        
        self.locationPanel = JPanel()
        self.locationPanel.setLayout(BoxLayout( self.locationPanel, BoxLayout.Y_AXIS))
        self.locationPanel.setPreferredSize(Dimension(550,330))
        global startup
        startup = True     # skip reader and fill table with blank data for a fast dialog open
        self.locationPanel.add(self.add_location_table())
        self.combinedPanel.add( self.locationPanel)
        
        self.enginePanel = JPanel()
        self.enginePanel.setLayout(BoxLayout( self.enginePanel, BoxLayout.Y_AXIS))
        self.enginePanel.setPreferredSize(Dimension(550,330))
        global EngineID
        self.enginePanel.add(self.add_engine_table(EngineID))
        self.combinedPanel.add( self.enginePanel)
        
        self.centerPanel.add( self.combinedPanel)
        
        self.close = JButton('Close', actionPerformed = self.close_dialog)
        self.drop = JButton('<-- Drop Car', actionPerformed = self.drop_click)
        self.pull = JButton('Pull Car -->', actionPerformed = self.pull_click)
        self.controlPanel = JPanel()
        self.controlPanel.setLayout(BoxLayout( self.controlPanel, BoxLayout.X_AXIS))
        self.controlPanel.setPreferredSize(Dimension(550,50))
        self.controlPanel.add( self.pull)
        self.controlPanel.add(Box.createRigidArea(Dimension(25, 25)))
        self.controlPanel.add( self.close)
        self.controlPanel.add(Box.createRigidArea(Dimension(25, 25)))
        self.controlPanel.add( self.drop)
        self.centerPanel.add( self.controlPanel)
        
        self.centerPanel.add(Box.createRigidArea(Dimension(25, 25)))
        self.add( self.centerPanel,BorderLayout.CENTER)
        self.setVisible(True)
        set_linked_gui(self)   #add to variable
        self.delayLoad()
        
    def delayLoad(self):    
        delayTime = 20
        holdTime = int(round(time.time()*1000)) 
        delta = 0 
        while delta < delayTime:               
              loopTime =  int(round(time.time()*1000))
              delta = loopTime - holdTime 
        print "timer done"
        global LocReader
        self.update_tables(LocReader)
        
        
    def add_engine_table(self, forEngine):
            self.colNames = ('Type',"Color","Road Name", "Road Number")
            self.dataModel = DefaultTableModel( self.sort_engine_data(forEngine), self.colNames)
            self.engineTable = JTable( self.dataModel)
            self.engineTable.getTableHeader().setReorderingAllowed(0)
            self.engineTable.setSelectionMode(0)
            #self.engineTable.setRowSelectionInterval(0, 0)
            self.scrollPane = JScrollPane()
            self.scrollPane.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_ALWAYS)
            self.scrollPane.setPreferredSize(Dimension(330,125))
            self.scrollPane.getViewport().setView(self.engineTable)
            self.panel = JPanel()
            self.panel.preferredSize = (Dimension(330,200))
            self.panel.setLayout(BoxLayout( self.panel, BoxLayout.Y_AXIS))
            global EngineID
            self.titleText2 = JLabel(EngineID)
            self.titleText2.setForeground(Color.decode("#000dff"))
            self.titleText2.setBackground(Color.decode("#000000"))
            self.titleText2.setFont(Font("Serif", Font.PLAIN, 24))
            self.panel.add(self.titleText2)
            self.panel.add(self.scrollPane)
            return self.panel
        
    def add_location_table(self):
            self.colNames = ('Type',"Color","Road Name", "Road Number")
            self.dataModel = DefaultTableModel(self.sort_location_data(), self.colNames)
            self.locationTable = JTable(self.dataModel)
            self.locationTable.getTableHeader().setReorderingAllowed(0)
            self.locationTable.setSelectionMode(0)
            self.scrollPane = JScrollPane()
            self.scrollPane.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_ALWAYS)
            self.scrollPane.setPreferredSize(Dimension(330,125))
            self.scrollPane.getViewport().setView(self.locationTable)
            self.panel = JPanel()
            self.panel.preferredSize = (Dimension(330,200))
            self.panel.setLayout(BoxLayout( self.panel, BoxLayout.Y_AXIS))
            global LocText
            global LocReader
            self.buildIt = " " + LocText + "  " + LocReader
            self.titleText3 = JLabel(self.buildIt)
            self.titleText3.setForeground(Color.decode("#000dff"))
            self.titleText3.setBackground(Color.decode("#000000"))
            self.titleText3.setFont(Font("Serif", Font.PLAIN, 24))
            self.panel.add(self.titleText3)
            self.panel.add(self.scrollPane)
            return self.panel
    
    def update_tables(self, reader):
        ''' fill table with new data and display it'''
        self.remove(self.centerPanel)
        self.revalidate()
        print "got to update tables **********************"
        self.centerPanel = JPanel()
        self.centerPanel.setLayout(BoxLayout( self.centerPanel, BoxLayout.Y_AXIS))
        self.centerPanel.setPreferredSize(Dimension(600,375))
        self.combinedPanel = JPanel()
        self.combinedPanel.setLayout(BoxLayout( self.combinedPanel, BoxLayout.X_AXIS))
        self.combinedPanel.setPreferredSize(Dimension(600,330))
        self.locationPanel = JPanel()
        self.locationPanel.setLayout(BoxLayout( self.locationPanel, BoxLayout.Y_AXIS))
        self.locationPanel.setPreferredSize(Dimension(550,330))
        global startup
        startup = False
        self.locationPanel.add(self.add_location_table())
        self.combinedPanel.add( self.locationPanel)
        self.enginePanel = JPanel()
        self.enginePanel.setLayout(BoxLayout( self.enginePanel, BoxLayout.Y_AXIS))
        self.enginePanel.setPreferredSize(Dimension(550,330))
        global EngineID
        self.enginePanel.add(self.add_engine_table(EngineID))
        self.combinedPanel.add( self.enginePanel)
        self.centerPanel.add( self.combinedPanel)
        self.close = JButton('Close', actionPerformed = self.close_dialog)
        self.drop = JButton('<-- Drop Car', actionPerformed = self.drop_click)
        self.pull = JButton('Pull Car -->', actionPerformed = self.pull_click)
        self.controlPanel = JPanel()
        self.controlPanel.setLayout(BoxLayout( self.controlPanel, BoxLayout.X_AXIS))
        self.controlPanel.setPreferredSize(Dimension(550,50))
        self.controlPanel.add( self.pull)
        self.controlPanel.add(Box.createRigidArea(Dimension(25, 25)))
        self.controlPanel.add( self.close)
        self.controlPanel.add(Box.createRigidArea(Dimension(25, 25)))
        self.controlPanel.add( self.drop)
        self.centerPanel.add( self.controlPanel)
        self.centerPanel.add(Box.createRigidArea(Dimension(25, 25)))
        self.add( self.centerPanel,BorderLayout.CENTER)
        self.revalidate()
        self.repaint()
     
    def close_dialog(self, event):
        self.dispose()
       
    def sort_engine_data(self, forEngine):
      '''Sort installed readers list for table display'''
      #print "***************      engine = ", forEngine
      try:
         global  engineCars
         engineCars = basic_get_cars_for_pull_drop(forEngine)
         self.temp = []
         self.engineData = []
         self.temp = []
         for shrink in engineCars:  # pick data for display
             self.temp.append(shrink[1])
             self.temp.append(shrink[2])
             self.temp.append(shrink[3])
             self.temp.append(shrink[4])
             self.engineData.append(self.temp)
             self.temp = []
         return self.engineData
      except:
         print "enginePickupDropOffCar.py --  something wrong with sort_engine_data"
         print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]

    def sort_location_data(self):
         '''at dialog opening display empty table, after that get cars from a reader to display'''
         try:
             global locationCars
             locationCars= basic_get_location_for_pull_drop(LocReader)
             self.temp = []
             self.locationData = []
             self.temp = []
             for shrink in locationCars:                                            # pick data for display
                 self.temp.append(shrink[1])
                 self.temp.append(shrink[2])
                 self.temp.append(shrink[3])
                 self.temp.append(shrink[4])
                 self.locationData.append(self.temp)
                 self.temp = []
             return self.locationData
         except:
             print "enginePickupDropOffCar.py --  something wrong with sort_location_data"
             print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]
                  
        
    def drop_click(self, event): 
            '''move car from engine to the location (reader)'''
            global engineCars
            a = self.engineTable.getSelectedRow()
            if a < 0:
                showMessageDialog('You must pick a car from the Engine table to be dropped..\n' ,'No car to drop')
                return
            try:
                index = self.engineTable.getSelectedRow()
                car = engineCars[index]
                global EngineID
                carID = car[6]
                basic_drop_car_to_location(LocReader, carID)
                self.update_tables(LocReader)
            except:
                print "enginePickupDropOffCar.py -- drop_click has a problem"
                print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]

    def pull_click(self, event): 
                '''move car from location to the engine'''
                global locationCars
                b = self.locationTable.getSelectedRow()
                if b < 0:
                    showMessageDialog('You must pick a car from the Location table to be pulled..\n' ,'No car to pull')
                    return
                try:
                    index = self.locationTable.getSelectedRow()
                    car = locationCars[index]
                    global EngineID
                    carID = car[6]
                    basic_add_car_to_engine(EngineID, carID)
                    self.update_tables(LocReader)
                except:
                    print "enginePickupDropOffCar.py --  pull_click has a problem"
                    print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]

    def no_engine(self):
                    '''used for pick and drop mush have an engine'''
                    showMessageDialog('An Engine must first be assigned to a location\n'
                    'before you may use the Pick up or Drop off feature\n ',"Assignment Error")

                    

       
if __name__ == "__main__":
    print "Running enginePickDropCarGUI.py"
        