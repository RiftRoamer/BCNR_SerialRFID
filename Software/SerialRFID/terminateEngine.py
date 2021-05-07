from  javax.swing import *
from  java.awt import *
from  java.awt.event import *
from variables import *
from swingutils.events import *
from javax.swing.event import *
from javax.swing.BorderFactory import *
from configRFID import *
import sys

    
class TerminateEngine(JDialog):
    def __init__(self):
        global changes
        changes = []
        JDialog.__init__(self, None, 'Terminate this Engine', True)
        #self.setDefaultCloseOperation(DO_NOTHING_ON_CLOSE)
        self.setSize(925,330)
        self.setLayout(BorderLayout())
        self.setLocation(100,100)
        self.preferredSize = (Dimension(925,330))
        self.setBackground(Color.LIGHT_GRAY)
        
        northPanel = JPanel()
        #northPanel.setLayout(BorderLayout())
        noteText = JLabel('   This will terminate Engine:   ')
        noteText.setForeground(Color.decode("#000dff"))
        noteText.setBackground(Color.decode("#000000"))
        noteText.setFont(Font("Serif", Font.PLAIN, 24))
        northPanel.add(noteText)
        self.add(northPanel,BorderLayout.NORTH)
        southPanel = JPanel()
        titleText = JLabel('   Select terminate to DROP all cars and / or engines to this location.  ')
        titleText.setForeground(Color.decode("#000dff"))
        titleText.setBackground(Color.decode("#000000"))
        titleText.setFont(Font("Serif", Font.PLAIN, 20))
        southPanel.add(titleText)
        self.add(southPanel,BorderLayout.SOUTH)   

        centerPanel = JPanel()
        centerPanel.setLayout(BoxLayout(centerPanel, BoxLayout.Y_AXIS))
        centerPanel.setPreferredSize(Dimension(350,330))
        
        enginePanel = JPanel()
        enginePanel.setLayout(BoxLayout(enginePanel, BoxLayout.Y_AXIS))
        enginePanel.setPreferredSize(Dimension(350,100))
        assignment =   get_rfid_eng_assign()
        engine = assignment[0]
        location = assignment[1]
        reader = assignment[2]
        engineText = JLabel(engine)
        engineText.setForeground(Color.decode("#000dff"))
        engineText.setBackground(Color.decode("#000000"))
        engineText.setFont(Font("Serif", Font.PLAIN, 60))
        enginePanel.add(engineText)
        centerPanel.add(enginePanel)
        
        forPanel = JPanel()
        forPanel.setLayout(BoxLayout(forPanel, BoxLayout.Y_AXIS))
        forPanel.setPreferredSize(Dimension(350,100))
        forText = JLabel('At this location')
        forText.setForeground(Color.decode("#000dff"))
        forText.setBackground(Color.decode("#000000"))
        forText.setFont(Font("Serif", Font.PLAIN, 24))
        forPanel.add(forText)
        centerPanel.add(forPanel)
        
        locationPanel = JPanel()
        locationPanel.setLayout(BoxLayout(locationPanel, BoxLayout.Y_AXIS))
        locationPanel.setPreferredSize(Dimension(350,100))
        locationText = JLabel(location)
        locationText.setForeground(Color.decode("#000dff"))
        locationText.setBackground(Color.decode("#000000"))
        locationText.setFont(Font("Serif", Font.PLAIN, 60))
        locationPanel.add(locationText)
        centerPanel.add(locationPanel)
        
        self.add(centerPanel,BorderLayout.CENTER)
        
        eastPanel = JPanel()
        eastPanel.setLayout(BoxLayout(eastPanel, BoxLayout.Y_AXIS))
        eastPanel.preferredSize = (Dimension(150,1))
        saveAddresss = JButton('Terminate', actionPerformed = self.do_terminate)
        cancel = JButton('Cancel', actionPerformed = self.cancel_data)
        eastPanel.add(Box.createRigidArea(Dimension(25, 25)))
        eastPanel.add(saveAddresss)
        eastPanel.add(Box.createRigidArea(Dimension(25, 25)))
        eastPanel.add(cancel)
        self.add(eastPanel,BorderLayout.EAST)
        
        self.setVisible(True)
        

    def do_terminate(self, event):
        try:
           basic_terminate_engine()
           self.dispose()
        except:
            print "terminateEngine.py -- do_terminate failed"
            print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]
            pass
        
    def cancel_data(self, event):
        #print "got to cancel data"
        self.dispose()
         

        
if __name__ == "__main__":
    print "Running readerGUI.py"
