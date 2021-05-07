from  javax.swing import *
from  java.awt import *
from  java.awt.event import *
from variables import *
import sys
from configRFID import *
from javax.swing import JComboBox
from java.awt.event import ItemListener
from java.awt import BorderLayout;
from java.awt import Color;
from mycommport import *
from basicImportedData import *
global reader
reader = ""   

class GetListener(ItemListener):
    def  __init__(self):
        ItemListener.__init__(self)

    def itemStateChanged(self, ItemEvent ):
        ''' combo box selection event 1 = selected'''
        selected = ItemEvent.getStateChange()
        if selected == 1:   
            global reader
            reader = ItemEvent.getItem()       #hold selection in case dialog is closed without an update
            #print "new reader is ", reader

class ListCarsFromReader(JDialog):
    def __init__(self):
        JDialog.__init__(self, None, 'List all cars from a Reader', True)
        global s
        self.setSize(1200,400)
        self.setLayout(BorderLayout())
        self.setLocation(100,100)
        self.preferredSize = 1000,400
        self.setBackground(Color.LIGHT_GRAY)
        
        self.northPanel = JPanel()
        self.noteText = JLabel('     Cars        ')
        self.noteText.setForeground(Color.decode("#000dff"))
        self.noteText.setBackground(Color.decode("#000000"))
        self.noteText.setFont(Font("Serif", Font.PLAIN, 24))
        self.northPanel.add(self.noteText)
        self.add(self.northPanel,BorderLayout.NORTH)
        
        self.southPanel = JPanel()
        self.titleText = JLabel('   Read-only list of cars from a reader    ')
        self.titleText.setForeground(Color.decode("#000dff"))
        self.titleText.setBackground(Color.decode("#000000"))
        self.titleText.setFont(Font("Serif", Font.PLAIN, 20))
        self.southPanel.add(self.titleText)
        self.add(self.southPanel,BorderLayout.SOUTH)
        
        self.eastPanel = JPanel()
        self.eastPanel.setLayout(BoxLayout(self.eastPanel, BoxLayout.Y_AXIS))
        self.eastPanel.preferredSize = (Dimension(250,100))
        self.readText = "Active Reader " +  str(get_active_reader())
        self.locText = JLabel(self.readText)
        self.locText.setForeground(Color.decode("#000dff"))
        self.locText.setBackground(Color.decode("#000000"))
        self.locText.setFont(Font("Serif", Font.PLAIN, 24))
        self.eastPanel.add(self.locText)
        self.combo = self.fill_combo()
        self.close = JButton('Close', actionPerformed = self.close_panel)
        self.getList = JButton('Update', actionPerformed = self.on_click)
        self.eastPanel.add(Box.createRigidArea(Dimension(25, 10)))
        self.comboPanel = JPanel()
        self.comboPanel.setLayout(BoxLayout(self.comboPanel, BoxLayout.X_AXIS))
        self.comboPanel.preferredSize = (Dimension(25,25))
        self.comboPanel.add(self.combo)
        self.eastPanel.add(self.comboPanel)
        self.eastPanel.add(Box.createRigidArea(Dimension(25, 10)))
        self.eastPanel.add(self.getList)
        self.eastPanel.add(self.close)
        self.add(self.eastPanel,BorderLayout.EAST)
        
        self.westPanel = JPanel()
        self.westPanel.setLayout(BoxLayout(self.westPanel, BoxLayout.X_AXIS))
        self.westPanel.preferredSize = (Dimension(10,350))
        self.westPanel.add(Box.createRigidArea(Dimension(10, 25)))
        self.add(self.westPanel,BorderLayout.WEST)
        
        self.centerPanel = JPanel()
        self.centerPanel.setLayout(BoxLayout(self.centerPanel, BoxLayout.Y_AXIS))
        self.centerPanel.preferredSize = (Dimension(425,1))
        self.checkPanel = JPanel()
        self.checkPanel.setLayout(BoxLayout(self.checkPanel, BoxLayout.X_AXIS))
        self.checkPanel.setPreferredSize(Dimension(400,300))
        global startup
        self.checkPanel.add(self.add_table())
        self.centerPanel.add(self.checkPanel)    
        self.add(self.centerPanel,BorderLayout.CENTER)
        self.pack()
        self.setVisible(True)
        set_linked_gui(self)   #add to variable
        global reader
        reader =  str(get_active_reader())
            
    def update_reader_list(self, reader):
        ''' fill table with new data and display it'''
        self.centerPanel.remove(self.checkPanel)
        self.revalidate()
        self.checkPanel = JPanel()
        self.checkPanel.setLayout(BoxLayout(self.checkPanel, BoxLayout.X_AXIS))
        self.checkPanel.setPreferredSize(Dimension(400,300))
        self.checkPanel.add(self.add_table())
        self.centerPanel.add(self.checkPanel)    
        self.add(self.centerPanel,BorderLayout.CENTER)
        self.locText.text = "Active Reader " +  str(get_active_reader())
        self.revalidate()
        self.repaint()
        
    def close_panel(self, event):
        ''' simple close with dispose'''
        self.dispose()
       
    def fill_combo(self):
        '''get all installed readers and fill dropdown list'''
        self.installed = get_installed_readers()
        self.fill =[]
        for reader in self.installed:
            x = str(reader.get('address'))
            self.fill.append(x)
        self.p = JPanel()
        self.cb2 = JComboBox(self.fill)
        self.cb2.setSelectedItem(get_active_reader())
        self.cb2.addItemListener(GetListener())
        self.p.add(self.cb2)
        return self.p   
        
    def on_click(self, event): 
            '''set new active reader and start the display update'''
            global reader
            set_active_reader(reader)     # last selection from active reader dropdown list
            self.update_reader_list(get_active_reader())
            
    def add_table(self):
            ''' Initial table fill at opening of dialog'''
            colNames = ('RFID','Type','Color','Road Name','Road Number','Owner','CarID')
            self.table = JTable( self.sort_data(), colNames)
            self.table.getTableHeader().setReorderingAllowed(0)
            self.table.setSelectionMode(0)
            scrollPane = JScrollPane()
            scrollPane.setPreferredSize(Dimension(600,250))
            scrollPane.getViewport().setView(self.table)
            panel = JPanel()
            panel.add(scrollPane)
            return panel
        
    def rec_data_error(self):
        '''no reply from comm port'''
        #print "show dialog"
        showMessageDialog('This dialog timed out waiting for a COM port reply.\n' ,'Internal command 5')
        #set_polling(False)
     
    def sort_data(self):
     '''at dialog opening display empty table, after that get cars from a reader to display'''
     try: 
        cars = basic_list_cars_engines_from_reader()
        return cars
     except:
        cars = [[' ', ' ' ,' ',' ',' ',' ',' ']]
        global startup
        return cars 
        print "something wrong with linkCarsFromReader.py -- sort_data"
        print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]
             


if __name__ == "__main__":
    print "Running linkCarsFromReader.py"
