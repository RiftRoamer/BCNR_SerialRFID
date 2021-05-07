from  javax.swing import *
from  java.awt import *
from  java.awt.event import *
from variables import *
from swingutils.events import *
from javax.swing.event import *
from javax.swing.BorderFactory import *
from configRFID import *
import sys

    
class ReaderAdd(JDialog):
    def __init__(self):
        global changes
        changes = []
        JDialog.__init__(self, None, 'Add a New Reader', True)
        #self.setDefaultCloseOperation(DO_NOTHING_ON_CLOSE)
        self.setSize(925,330)
        self.setLayout(BorderLayout())
        self.setLocation(100,100)
        self.preferredSize = (Dimension(925,330))
        self.setBackground(Color.LIGHT_GRAY)
        
        northPanel = JPanel()
        #northPanel.setLayout(BorderLayout())
        noteText = JLabel('   The next available reader address is:   ')
        noteText.setForeground(Color.decode("#000dff"))
        noteText.setBackground(Color.decode("#000000"))
        noteText.setFont(Font("Serif", Font.PLAIN, 24))
        northPanel.add(noteText)
        self.add(northPanel,BorderLayout.NORTH)
        southPanel = JPanel()
        titleText = JLabel('   Enter the "Stand Alone Mode" location name in the text box - then Add Address   ')
        titleText.setForeground(Color.decode("#000dff"))
        titleText.setBackground(Color.decode("#000000"))
        titleText.setFont(Font("Serif", Font.PLAIN, 20))
        southPanel.add(titleText)
        self.add(southPanel,BorderLayout.SOUTH)   

        westPanel = JPanel()
        westPanel.setPreferredSize(Dimension(315,330))
        westPanel.setLayout(BoxLayout(westPanel, BoxLayout.X_AXIS))
        westPanel.add(Box.createVerticalGlue())
        explain = ("\nAll Serial RFID readers come preconfigured with the address 'A'. Before adding a new card to the bus you must use the " 
        "provided Arduino program and set the card address to the address displayed on this screen.\n\nPlease referr to the 'ReadMe' file "
        "for hardware install details.:\n\nNew card will be added to polling imediately.\n\n Add Address -- save and exit\n Cancel -- exit without saving changes\n  .")
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
        nextPanel = JPanel()
        nextPanel.setLayout(BoxLayout(nextPanel, BoxLayout.Y_AXIS))
        nextPanel.setPreferredSize(Dimension(350,330))
        global available
        available =  get_available_reader()
        nextText = JLabel(available)
        nextText.setForeground(Color.decode("#000dff"))
        nextText.setBackground(Color.decode("#000000"))
        nextText.setFont(Font("Serif", Font.PLAIN, 60))
        
        capPanel = JPanel()
        capPanel.setLayout(BoxLayout(capPanel, BoxLayout.X_AXIS))
        capPanel.setPreferredSize(Dimension(350,330))
        capText = JLabel('JMRI links are added under the locations menu')
        capText.setForeground(Color.decode("#000dff"))
        capText.setBackground(Color.decode("#000000"))
        capText.setFont(Font("Serif", Font.PLAIN, 16))
        capPanel.add(capText)
        
        nextPanel.add(nextText)
        nextPanel.add(capPanel)
        
        centerPanel.add(nextPanel)
        enterPanel = JPanel()
        enterPanel.setSize(350,100)
        enterPanel.preferredSize = (Dimension(350,100))
        enterPanel.setLayout(BoxLayout(enterPanel, BoxLayout.Y_AXIS))
        inputPanel = JPanel()
        inputPanel.setSize(350,75)
        inputPanel.preferredSize = (Dimension(350,75))
        inputPanel.setLayout(BoxLayout(inputPanel, BoxLayout.X_AXIS))
        global newName
        newName = JTextField(available, 20)
        inputPanel.add(Box.createRigidArea(Dimension(130, 0)))
        inputPanel.add(newName)
        inputPanel.add(Box.createRigidArea(Dimension(130, 0)))
        enterPanel.add(inputPanel)
        
        
        buttonPanel = JPanel()
        buttonPanel.setSize(350,100)
        buttonPanel.preferredSize = (Dimension(350,100))
        buttonPanel.setLayout(BoxLayout(buttonPanel, BoxLayout.X_AXIS))
        change = JLabel('Location name')
        change.setForeground(Color.decode("#000dff"))
        change.setBackground(Color.decode("#000000"))
        change.setFont(Font("Serif", Font.PLAIN, 16))
        buttonPanel.add(change)
        
        
        enterPanel.add(buttonPanel)
        centerPanel.add(enterPanel)
        self.add(centerPanel,BorderLayout.CENTER)
        
        eastPanel = JPanel()
        eastPanel.setLayout(BoxLayout(eastPanel, BoxLayout.Y_AXIS))
        eastPanel.preferredSize = (Dimension(150,1))
        saveAddresss = JButton('Add Address', actionPerformed = self.save_data)
        cancel = JButton('Cancel', actionPerformed = self.cancel_data)
        eastPanel.add(Box.createRigidArea(Dimension(25, 25)))
        eastPanel.add(saveAddresss)
        eastPanel.add(Box.createRigidArea(Dimension(25, 25)))
        eastPanel.add(cancel)
        self.add(eastPanel,BorderLayout.EAST)
        
        
        self.setVisible(True)
        

    def save_data(self, event):
        try:
            #print "got to save data"
            global newName
            global available
            addReader = []
            #print "newName is ", newName.text
            #print "available is ", available
            a = len(newName.text)
            if a < 1:                                      # set name same as address
                newName.text = available  
            addReader.append(available)
            addReader.append(newName.text)
            basic_set_installed_reader(addReader)
            self.dispose()
        except:
            print "ReaderAdd.py -- save_data failed"
            print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]
            pass
        
    def cancel_data(self, event):
        #print "got to cancel data"
        global changes
        changes = []
        #print changes
        self.dispose()
         

        
if __name__ == "__main__":
    print "Running readerGUI.py"
