from  javax.swing import *
from  java.awt import *
from  java.awt.event import *
from variables import *
from swingutils.events import *
from javax.swing.event import *
from javax.swing.BorderFactory import *
from configRFID import *
from importFiles import *
    
class ImportJMRIFiles(JDialog):
    def __init__(self):
        global changes
        changes = []
        JDialog.__init__(self, None, 'Import JMRI records', True)
        #self.setDefaultCloseOperation(DO_NOTHING_ON_CLOSE)
        self.setSize(925,330)
        self.setLayout(BorderLayout())
        self.setLocation(100,100)
        self.preferredSize = (Dimension(925,330))
        self.setBackground(Color.LIGHT_GRAY)
        
        northPanel = JPanel()
        #northPanel.setLayout(BorderLayout())
        noteText = JLabel('   Import JMRI Location/Engine/Car XML files   ')
        noteText.setForeground(Color.decode("#000dff"))
        noteText.setBackground(Color.decode("#000000"))
        noteText.setFont(Font("Serif", Font.PLAIN, 24))
        northPanel.add(noteText)
        self.add(northPanel,BorderLayout.NORTH)
        southPanel = JPanel()
        titleText = JLabel('   These files are used by the "Stand Alone Mode" like manually entered items   ')
        titleText.setForeground(Color.decode("#000dff"))
        titleText.setBackground(Color.decode("#000000"))
        titleText.setFont(Font("Serif", Font.PLAIN, 20))
        southPanel.add(titleText)
        self.add(southPanel,BorderLayout.SOUTH)   

        westPanel = JPanel()
        westPanel.setPreferredSize(Dimension(315,330))
        westPanel.setLayout(BoxLayout(westPanel, BoxLayout.X_AXIS))
        westPanel.add(Box.createVerticalGlue())
        explain = ("\n Importing JMRI files is meant to be an easy way for users who want to use SerialRFID as a Stand-Alone program " 
        "but do have JMRI data files.\n\nThe data is added to SerialRFID importJMRI.xml file which also holds manually entered data. "
        "The importJMRI file distinguishes the difference by marking the data as imported=YES/NO.:\n\n Imported = Yes -- This data "
        "will be replaced if you perform a second import. \n Imported = No -- This data will be retained if you perform a second import.\n"
        "\n\nImport Files -- Starts the import operation.\nClose -- exit without importng files.\n")
        westPanel.add(Box.createRigidArea(Dimension(15, 0)))
        text = (JTextArea(text = explain,
                editable = False,
                wrapStyleWord = True,
                lineWrap = True,
                alignmentX = Component.LEFT_ALIGNMENT,
                size = (300, 1)
        ))
        scrollPane = JScrollPane()
        scrollPane.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_ALWAYS)
        scrollPane.setPreferredSize(Dimension(330,125))
        scrollPane.getViewport().setView(text)

        westPanel.add(scrollPane)
        
        self.add(westPanel,BorderLayout.WEST)
        
        centerPanel = JPanel()
        centerPanel.setLayout(BoxLayout(centerPanel, BoxLayout.Y_AXIS))
        centerPanel.setPreferredSize(Dimension(350,330))
        nextPanel = JPanel()
        nextPanel.setLayout(BoxLayout(nextPanel, BoxLayout.Y_AXIS))
        nextPanel.setPreferredSize(Dimension(350,330))
        self.available = "*"
        self.nextText = JLabel(self.available)
        self.nextText.setForeground(Color.decode("#000dff"))
        self.nextText.setBackground(Color.decode("#000000"))
        self.nextText.setFont(Font("Serif", Font.PLAIN, 60))
        
        capPanel = JPanel()
        capPanel.setLayout(BoxLayout(capPanel, BoxLayout.X_AXIS))
        capPanel.setPreferredSize(Dimension(350,330))
        capText = JLabel('Import Status')
        capText.setForeground(Color.decode("#000dff"))
        capText.setBackground(Color.decode("#000000"))
        capText.setFont(Font("Serif", Font.PLAIN, 16))
        capPanel.add(capText)
        
        nextPanel.add(self.nextText)
        nextPanel.add(capPanel)
        
        centerPanel.add(nextPanel)
        enterPanel = JPanel()
        enterPanel.setSize(350,100)
        enterPanel.preferredSize = (Dimension(350,100))
        enterPanel.setLayout(BoxLayout(enterPanel, BoxLayout.Y_AXIS))

        centerPanel.add(enterPanel)
        self.add(centerPanel,BorderLayout.CENTER)
        
        eastPanel = JPanel()
        eastPanel.setLayout(BoxLayout(eastPanel, BoxLayout.Y_AXIS))
        eastPanel.preferredSize = (Dimension(150,1))
        saveAddresss = JButton('Import Files', actionPerformed = self.do_import)
        cancel = JButton('Close', actionPerformed = self.cancel_data)
        eastPanel.add(Box.createRigidArea(Dimension(25, 25)))
        eastPanel.add(saveAddresss)
        eastPanel.add(Box.createRigidArea(Dimension(25, 25)))
        eastPanel.add(cancel)
        self.add(eastPanel,BorderLayout.EAST)
        
        self.setVisible(True)
        set_linked_gui(self)
        
    def do_import(self, event):
         self.setCursor(Cursor.getPredefinedCursor(Cursor.WAIT_CURSOR))
         self.available = "Importing"
         self.nextText.text = self.available 
         x = ImportFiles()
         self.available = "Complete"
         self.nextText.text = self.available 
         self.setCursor(Cursor.getPredefinedCursor(Cursor.DEFAULT_CURSOR))
   
    def cancel_data(self, event):
        #print "got to cancel data"
        global changes
        changes = []
        #print changes
        self.dispose()
         

        
if __name__ == "__main__":
    print "Running readerGUI.py"
