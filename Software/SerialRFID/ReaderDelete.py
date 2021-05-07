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

        
class ReaderDelete(JDialog):
    def __init__(self):
        global changes
        changes = []
        JDialog.__init__(self, None, 'Delete a Reader', True)
        #self.setDefaultCloseOperation(DO_NOTHING_ON_CLOSE)
        self.setSize(925,330)
        self.setLayout(BorderLayout())
        self.setLocation(100,100)
        self.preferredSize = (Dimension(925,330))
        self.setBackground(Color.LIGHT_GRAY)
        
        northPanel = JPanel()
        #northPanel.setLayout(BorderLayout())
        noteText = JLabel('   Delete the Selected reader   ')
        noteText.setForeground(Color.decode("#000dff"))
        noteText.setBackground(Color.decode("#000000"))
        noteText.setFont(Font("Serif", Font.PLAIN, 24))
        northPanel.add(noteText)
        self.add(northPanel,BorderLayout.NORTH)
        
        southPanel = JPanel()
        titleText = JLabel('   Click on a "row" to select the reader to delete - then Delete Reader  ')
        titleText.setForeground(Color.decode("#000dff"))
        titleText.setBackground(Color.decode("#000000"))
        titleText.setFont(Font("Serif", Font.PLAIN, 20))
        southPanel.add(titleText)
        self.add(southPanel,BorderLayout.SOUTH)   

        westPanel = JPanel()
        westPanel.setPreferredSize(Dimension(315,330))
        westPanel.setLayout(BoxLayout(westPanel, BoxLayout.X_AXIS))
        westPanel.add(Box.createVerticalGlue())
        explain = ("\nThis RFID reader will be removed from:\n\n1) the installed list\n2) the polling list\n3)Any JMRI file links\n\nAnd  " 
        "all of its SD Card 'Car content' will be erased, but the card address will not be changed."
        "\n\n Delete Address -- remove card and exit\n Cancel -- exit without making a deletion\n  .")
        westPanel.add(Box.createRigidArea(Dimension(15, 0)))
        westPanel.add(JTextArea(text = explain,
                editable = False,
                wrapStyleWord = True,
                lineWrap = True,
                alignmentX = Component.LEFT_ALIGNMENT,
                size = (300, 1)
        ))
        self.add(westPanel,BorderLayout.WEST)
        
        centerPanel = JPanel()
        centerPanel.setLayout(BoxLayout(centerPanel, BoxLayout.Y_AXIS))
        centerPanel.setPreferredSize(Dimension(350,330))
        tablePanel = JPanel()
        tablePanel.setLayout(BoxLayout(tablePanel, BoxLayout.X_AXIS))
        tablePanel.setPreferredSize(Dimension(350,330))
        tablePanel.add(self.add_sa_table())
        centerPanel.add(tablePanel)
        enterPanel = JPanel()
        enterPanel.setSize(350,100)
        enterPanel.preferredSize = (Dimension(350,100))
        enterPanel.setLayout(BoxLayout(enterPanel, BoxLayout.Y_AXIS))
        inputPanel = JPanel()
        inputPanel.setSize(350,75)
        inputPanel.preferredSize = (Dimension(350,75))
        inputPanel.setLayout(BoxLayout(inputPanel, BoxLayout.X_AXIS))
        global newName
        self.noSelection = JLabel("Be sure to select a row to delete")
        inputPanel.add(Box.createRigidArea(Dimension(130, 0)))
        inputPanel.add(self.noSelection)
        inputPanel.add(Box.createRigidArea(Dimension(130, 0)))
        enterPanel.add(inputPanel)
        buttonPanel = JPanel()
        buttonPanel.setSize(400,100)
        buttonPanel.preferredSize = (Dimension(400,100))
        buttonPanel.setLayout(BoxLayout(buttonPanel, BoxLayout.X_AXIS))
        buttonPanel.add(Box.createRigidArea(Dimension(130, 0)))
        #change = JButton('Enter Change', actionPerformed = self.new_data)
        #buttonPanel.add(change)
        enterPanel.add(buttonPanel)
        centerPanel.add(enterPanel)
        self.add(centerPanel,BorderLayout.CENTER)
        
        eastPanel = JPanel()
        eastPanel.setLayout(BoxLayout(eastPanel, BoxLayout.Y_AXIS))
        eastPanel.preferredSize = (Dimension(150,1))
        saveName = JButton('Delete Reader', actionPerformed = self.save_data)
        cancel = JButton('Cancel', actionPerformed = self.cancel_data)
        eastPanel.add(Box.createRigidArea(Dimension(25, 25)))
        eastPanel.add(saveName)
        eastPanel.add(Box.createRigidArea(Dimension(25, 25)))
        eastPanel.add(cancel)
        self.add(eastPanel,BorderLayout.EAST)
        
        
        self.setVisible(True)
        
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

    def save_data(self, event):
        try:
            #print "got to save data"
            a = self.table.getSelectedRow()
            #print "selected row = ",a
            delAddress = self.table.getValueAt(a,0)
            #print "value = ",delAddress
            #global changes
            a = len(delAddress)
            if a > 0:                         # pushed button with no changes made
                #print "address is good"
                basic_del_installed_reader(delAddress)
            #global changes 
            #changes = []
            self.dispose()
        except:
            print "ReaderSaDelGUI.py -- save_data failed"
            print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]

                    
                   
        
    def cancel_data(self, event):
        #print "got to cancel data"
        global changes
        changes = []
        #print changes
        self.dispose()
        
        
def sort_sa_data():
     '''Sort installed readers list for table display'''
     print "got to sort sa data"
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
        