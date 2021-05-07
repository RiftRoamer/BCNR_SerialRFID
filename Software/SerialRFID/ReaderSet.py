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
            gui = get_linked_gui()
            set_active_reader(reader)
            gui.update_dialog()
    
class ReaderSet(JDialog):
    def __init__(self):
        global changes
        changes = []
        JDialog.__init__(self, None, 'All Stand Alone Readers', True)
        #self.setDefaultCloseOperation(DO_NOTHING_ON_CLOSE)
        self.setSize(1100,330)
        self.setLayout(BorderLayout())
        self.setLocation(100,100)
        self.preferredSize = (Dimension(1100,330))
        self.setBackground(Color.LIGHT_GRAY)
        
        self.northPanel = JPanel()
        #northPanel.setLayout(BorderLayout())
        self.noteText = JLabel('   Stand-Alone Mode Installed readers   ')
        self.noteText.setForeground(Color.decode("#000dff"))
        self.noteText.setBackground(Color.decode("#000000"))
        self.noteText.setFont(Font("Serif", Font.PLAIN, 24))
        self.northPanel.add(self.noteText)
        self.add(self.northPanel,BorderLayout.NORTH)
        
        self.southPanel = JPanel()
        self.titleText = JLabel('   Click on a "row" and enter the "new name" in the text box - then Enter Change   ')
        self.titleText.setForeground(Color.decode("#000dff"))
        self.titleText.setBackground(Color.decode("#000000"))
        self.titleText.setFont(Font("Serif", Font.PLAIN, 20))
        self.southPanel.add(self.titleText)
        self.add(self.southPanel,BorderLayout.SOUTH)   

        self.westPanel = JPanel()
        self.westPanel.setPreferredSize(Dimension(315,330))
        self.westPanel.setLayout(BoxLayout(self.westPanel, BoxLayout.X_AXIS))
        self.westPanel.add(Box.createVerticalGlue())
        self.explain = ("To select a reader to be the active reader use the dropdown list and the assignment is automatic (No save required.)\n"
        "The active reader determines what will be displayed in other pop-ups, but it can be changed on those screens as well."
        "\n\nThe table lists all current 'Stand Alone' mode aassignments for each reader address. The default name is the same as the address." 
        "\nTo edit a name:\n1) Select the row with the name in it\n2) Enter the new name in the Change Box\n Press the Enter Change button\n\n"
        "When you have entered all your changes press:\n\n Save Changes -- save and exit\n Cancel -- exit without saving changes\n  .")
        self.westPanel.add(Box.createRigidArea(Dimension(15, 0)))
        self.helpText = (JTextArea(text = self.explain,
                editable = False,
                wrapStyleWord = True,
                lineWrap = True,
                alignmentX = Component.LEFT_ALIGNMENT,
                size = (300, 1)
        ))
        self.helpText.setCaretPosition(0);
        self.scrollPane = JScrollPane()
        self.scrollPane.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_ALWAYS)
        self.scrollPane.setPreferredSize(Dimension(330,125))
        self.scrollPane.getViewport().setView(self.helpText)
        self.westPanel.add(self.scrollPane)
        self.add(self.westPanel,BorderLayout.WEST)
        
        self.centerPanel = JPanel()
        self.centerPanel.setLayout(BoxLayout(self.centerPanel, BoxLayout.Y_AXIS))
        self.centerPanel.setPreferredSize(Dimension(350,330))
        self.tablePanel = JPanel()
        self.tablePanel.setLayout(BoxLayout(self.tablePanel, BoxLayout.X_AXIS))
        self.tablePanel.setPreferredSize(Dimension(350,330))
        self.tablePanel.add(self.add_sa_table())
        self.centerPanel.add(self.tablePanel)
        self.enterPanel = JPanel()
        self.enterPanel.setSize(350,100)
        self.enterPanel.preferredSize = (Dimension(350,100))
        self.enterPanel.setLayout(BoxLayout(self.enterPanel, BoxLayout.Y_AXIS))
        self.inputPanel = JPanel()
        self.inputPanel.setSize(350,75)
        self.inputPanel.preferredSize = (Dimension(350,75))
        self.inputPanel.setLayout(BoxLayout(self.inputPanel, BoxLayout.X_AXIS))
        global newName
        newName = JTextField(20)
        self.inputPanel.add(Box.createRigidArea(Dimension(130, 0)))
        self.inputPanel.add(newName)
        self.inputPanel.add(Box.createRigidArea(Dimension(130, 0)))
        self.enterPanel.add(self.inputPanel)
        self.buttonPanel = JPanel()
        self.buttonPanel.setSize(400,100)
        self.buttonPanel.preferredSize = (Dimension(400,100))
        self.buttonPanel.setLayout(BoxLayout(self.buttonPanel, BoxLayout.X_AXIS))
        self.change = JButton('Enter Change', actionPerformed = self.new_data)
        self.buttonPanel.add(self.change)
        self.enterPanel.add(self.buttonPanel)
        self.centerPanel.add(self.enterPanel)
        self.add(self.centerPanel,BorderLayout.CENTER)
        
        
        self.readText = "Active Reader " +  str(get_active_reader())
        self.locText = JLabel(self.readText)
        self.locText.setForeground(Color.decode("#000dff"))
        self.locText.setBackground(Color.decode("#000000"))
        self.locText.setFont(Font("Serif", Font.PLAIN, 24))
        
        
        
        self.combo = self.fill_combo()
        #eastPanel.add(Box.createRigidArea(Dimension(25, 10)))
        self.comboPanel = JPanel()
        self.comboPanel.setLayout(BoxLayout(self.comboPanel, BoxLayout.X_AXIS))
        self.comboPanel.preferredSize = (Dimension(25,25))
        self.comboPanel.add(self.combo)
        
        self.eastPanel = JPanel()
        self.eastPanel.setLayout(BoxLayout(self.eastPanel, BoxLayout.Y_AXIS))
        self.eastPanel.preferredSize = (Dimension(250,1))
        self.saveName = JButton('Save Changes', actionPerformed = self.save_data)
        self.cancel = JButton('Cancel', actionPerformed = self.cancel_data)
        self.eastPanel.add(self.locText)
        self.eastPanel.add(self.comboPanel)
        self.eastPanel.add(Box.createRigidArea(Dimension(25, 25)))
        self.eastPanel.add(self.saveName)
        self.eastPanel.add(Box.createRigidArea(Dimension(25, 25)))
        self.eastPanel.add(self.cancel)
        self.add(self.eastPanel,BorderLayout.EAST)
        set_linked_gui(self)
        
        self.setVisible(True)
    def update_dialog(self): 
        #print "got to update dialog"
        self.readText = "Active Reader " +  str(get_active_reader())
        self.locText.text = self.readText
        
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
    
    def add_sa_table(self):
            colNames = ('Adress','Name')
            dataModel = DefaultTableModel(sort_sa_data(), colNames)
            self.table = JTable(dataModel)
            self.table.getTableHeader().setReorderingAllowed(0)
            self.table.setSelectionMode(0)
            scrollPane = JScrollPane()
            scrollPane.setPreferredSize(Dimension(300,125))
            scrollPane.getViewport().setView(self.table)
            panel = JPanel()
            panel.add(scrollPane)
            return panel
     
     
    def new_data(self, event):
        print "got to new data"
        try:
            temp = [0,1]
            a = self.table.getSelectedRow()
            #print "selected row = ",a
            oldName = self.table.getValueAt(a,1)
            #print "value = ",oldName
            global newName
            #print "new name = ", newName.text
            self.table.setValueAt(newName.text,a,1)
            temp[0] = oldName
            temp[1] = newName.text
            global changes
            changes.append(temp)
            #print changes
        except:
            print "ReaderSet.py -- new_data failed"
            print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]
            pass
        
    def save_data(self, event):
        try:
            #print "got to save data"
            global changes
            a = len(changes)
            if a > 0:                         # pushed button with no changes made
                basic_set_stand_alone_names(changes)
            global changes 
            changes = []
            self.dispose()
        except:
            print "ReaderSet.py -- save_data failed"
            print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]
            pass
        
    def cancel_data(self, event):
        #print "got to cancel data"
        global changes
        changes = []
        #print changes
        self.dispose()
        
        
def sort_sa_data():
     '''Sort installed readers list for table display'''
     #print "got to sort sa data"
     try:
         readers = get_installed_readers()
         temp = []
         tableData = []
         for dictionary in readers:
             address = dictionary.get('address')
             name = dictionary.get('name')
             temp.append(address)
             #self.blank = "   "
             #self.temp.append(self.blank)
             temp.append(str(name))
             tableData.append(temp)
             temp = []
             #print tableData
         return tableData
     except:
         print "something wrong with sort_data"
         print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]

         

        
if __name__ == "__main__":
    print "Running readerGUI.py"
