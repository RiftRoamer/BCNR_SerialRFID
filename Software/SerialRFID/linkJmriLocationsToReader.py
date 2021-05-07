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
from basicImportedData import *

global cbList
cbList =[]

class GetListener(ItemListener):
    def  __init__(self):
        ItemListener.__init__(self)

    def itemStateChanged(self, ItemEvent ):
        ''' combo box selection event 1 = selected '''
        selected = ItemEvent.getStateChange()
        if selected == 1:
            reader = ItemEvent.getItem()
            set_active_reader(reader)
            gui = get_linked_gui()  # get from variables
            global cbList
            cbList = []
            gui.update_reader_list(self)
            
           

class LinkJmriLocationsToReader(JDialog):
    def __init__(self):
        JDialog.__init__(self, None, 'Link JMRI Locations to a Reader', True)
        self.setSize(1200,500)
        self.setLayout(BorderLayout())
        self.setLocation(100,100)
        self.preferredSize = 1000,500
        self.setBackground(Color.LIGHT_GRAY)
        
        self.northPanel = JPanel()
        self.noteText = JLabel('     Locations           Tracks        ')
        self.noteText.setForeground(Color.decode("#000dff"))
        self.noteText.setBackground(Color.decode("#000000"))
        self.noteText.setFont(Font("Serif", Font.PLAIN, 24))
        self.northPanel.add(self.noteText)
        self.add(self.northPanel,BorderLayout.NORTH)
        
        self.southPanel = JPanel()
        self.titleText = JLabel('   JMRI Operations Locations    ')
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
        self.cancel = JButton('Cancel', actionPerformed = self.cancel_data)
        self.save    = JButton('  Save  ', actionPerformed = self.save_data)
        self.eastPanel.add(Box.createRigidArea(Dimension(25, 10)))
        self.comboPanel = JPanel()
        self.comboPanel.setLayout(BoxLayout(self.comboPanel, BoxLayout.X_AXIS))
        self.comboPanel.preferredSize = (Dimension(25,25))
        self.comboPanel.add(self.combo)
        self.eastPanel.add(self.comboPanel)
        self.eastPanel.add(self.save)
        self.eastPanel.add(Box.createRigidArea(Dimension(25, 10)))
        self.eastPanel.add(self.cancel)
        self.add(self.eastPanel,BorderLayout.EAST)
        
        self.westPanel = JPanel()
        self.westPanel.setLayout(BoxLayout(self.westPanel, BoxLayout.X_AXIS))
        self.westPanel.add(Box.createRigidArea(Dimension(10, 25)))
        self.westPanel.preferredSize = (Dimension(350,350))
        self.helpText = self.help_column()
        self.westPanel.add(Box.createRigidArea(Dimension(10, 25)))
        self.westPanel.add(self.helpText)
        self.add(self.westPanel,BorderLayout.WEST)
        
        self.centerPanel = JPanel()
        self.centerPanel.setLayout(BoxLayout(self.centerPanel, BoxLayout.Y_AXIS))
        self.centerPanel.preferredSize = (Dimension(350,300))
        self.checkPanel = JPanel()
        self.checkPanel.setLayout(BoxLayout(self.checkPanel, BoxLayout.X_AXIS))
        self.checkPanel.setPreferredSize(Dimension(350,300))
        self.checkPanel.add(self.sort_jmri_data())
        self.centerPanel.add(self.checkPanel)
        self.add(self.centerPanel,BorderLayout.CENTER)
        self.pack()
        self.setVisible(True)
        set_linked_gui(self)   #add to variables
     
    def help_column(self):
       ''' Put 'how to' text into assignment panel'''
       self.text = ("'To the right is a scroll pane filled with JMRI Operations locations. It consists of two columns, Locations & Tracks retrieved from "
            "the OperationsLocationRoster.XML file. The locations column is read-only and serves as a location 'title' In JMRI for a location to be "
            "maeningful it must have at least one track assigned to it, so SerialRFID imposes that requirement too. Think of a location such as a yard or "
            "industrial area. each of these areas most likely would have more than one track. Each track for that location will be listed as a seperate check-box\n\n"
            "SerialRFID readers are not tied to any JMRI location, but are designed to be fexable. Depending on the size and physical characteristics of your layout "
            " you may choose to install a reader for each location as a single unit, one per track or even split a reader between multiple locations.\n\n"
            "All the action therefore takes place in the tracks column in conjuction with a selected reader. From the dropdown box select the desired reader to "
            "make assignments to (by default the window always opens with reader A selected.) The blue text 'Current read A' will update to show the newly selected "
            "reader. Once a reader is selected the track column will update to show all tracks assigned to or available to that reader.\n\nSome Locations may appear to have no tracks "
            "(JMRI allows you to create a location with no track assignment but this is not usually why the track column would appear empty for a Location) in "
            "practical terms a blank column (or missing track) indicates that all the tracks (or the missing track) associated with that location are not available because they are assigned to "
            "a different reader.\n\nHOW TO USE THE CHECKBOXES\n\nIf the box is CHECKED it is already assigned to the selected reader. If the box is UNCHECKED then "
            "the track is available for assignment. you can now make two choices:\n1> Check a box to assign that track\n2> Uncheck a box to remove a track from the selected reader "
            "and make it available to another reader.\n\nThe SAVE button\nAs you would expect it saves any changes you have made, BUT it saves only changes for the currently selected reader."
            "So assuming you are currently using reader A and make a new assignment, before selecting another reader you must SAVE the changes made to reader A.\n"
            "If you change the reader assignment before doing a save all changes will be lost.\n\nThe CANCEL button\nCloses the window without saving changes.\n\n STEP BY STEP\n"
            "1> Select a reader\n2> Check box to assign track(s)\n AND / OR\n 2> Uncheck box to release a track(s) assignment\n3> Save button\nRepeat steps 1 -3 as needed\n4> "
            "Cancel button to close window"
            )
       self.mainText = JTextArea()
       self.mainText.text = self.text
       self.mainText.lineWrap = True
       self.mainText.wrapStyleWord = True
       self.mainText.setSize(300, 325)
       self.mainText.setBackground(Color.LIGHT_GRAY)
       self.mainScroll = JScrollPane(self.mainText)
       self.mainScroll.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_ALWAYS)
       self.mainScroll.setPreferredSize(Dimension(325, 350))
       self.mainScroll.getViewport().setView((self.mainText))
       self.mainPanel = JPanel()
       self.mainPanel.setBackground(Color.LIGHT_GRAY)
       self.mainPanel.add(self.mainScroll)
       return self.mainPanel  
        
    def update_reader_list(self, reader):
        ''' get new data and update display'''
        self.centerPanel.remove(self.checkPanel)
        self.revalidate()
        self.checkPanel = JPanel()
        self.checkPanel.setLayout(BoxLayout(self.checkPanel, BoxLayout.X_AXIS))
        self.checkPanel.setPreferredSize(Dimension(350,350))
        self.checkPanel.add(self.sort_jmri_data())
        self.centerPanel.add(self.checkPanel)
        self.readText = "Active Reader " +  str(get_active_reader())
        self.locText.setText(self.readText) 
        self.revalidate()
        self.repaint()
        
    def cancel_data(self, event):
        ''' simple close of dialog'''
        self.dispose()
        
    def save_data(self, event):
        '''remove current assignment and add new checkbox assignments'''
        global cbList
        assignLocation = []
        removeLocation = []
        for x in cbList:
            locId = isinstance(x, str)
            if locId:
                name = x
            box = isinstance(x, JCheckBox) 
            if box:
                if x.isSelected():                           # assign to reader tracked selected
                    add = []
                    add.append(name)                   # track ID
                    #add.append(str(x.text))            # track name
                    add.append(get_active_reader())       # assign to this reader
                    assignLocation.append(add)
                    #print "name = ",name
                    #print "checked"
                else:
                    nothing = 0                                 # does nothing just place holder for else testing
                    #print "name = ", name
                    #print "unchecked"
        count = len(assignLocation)
        if count == 0:         # no tracks selected or all selections removed
            emptyList = []
            emptyList.append('empty')
            emptyList.append(get_active_reader())  # delete all assignments for this reader
            assignLocation.append(emptyList)
        basic_update_track_assignments(assignLocation)
        self.update_reader_list(get_active_reader()) 
        
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
        
    def on_check(self, event): 
            '''does nothing'''
            box = event.getActionCommand()
            #print "check box event = ", box

    def sort_jmri_data(self):
     '''list all JMRI locations and make a checkbox for every JMRI Operations track'''
     currentReader = get_active_reader()
     global preAssigned
     global wholeList
     wholeList =  get_basic_loc_track_tags()                    # all locations
     global assigned
     assigned =  get_basic_reader_assignments()               # all assigned locations
     blackline = BorderFactory.createLineBorder(Color.black)
     self.boxPanel = JPanel()
     self.boxPanel.setLayout(BoxLayout(self.boxPanel, BoxLayout.Y_AXIS))
     self.boxPanel.preferredSize = (Dimension(250,300))

     try:     
         matchedTrack = False
         locationID = 0
         for locations in wholeList:                                                       # list of all locations with tracks
             for location in locations:                                                             # [ [{location dictionary}], [ [track list], [track list] ] ]
                     #print "location = ", location
                     self.leftPanel = JPanel()
                     self.leftPanel.preferredSize = (Dimension(200,500))

                     self.rightPanel = JPanel()
                     self.rightPanel.setLayout(BoxLayout(self.rightPanel, BoxLayout.Y_AXIS))
                     self.rightPanel.preferredSize = (Dimension(200,500))

                     isLocation = isinstance(location, dict)             # test if this is a location dictionary
                     if isLocation:
                          #print "location is true"
                          jmriName = location.get("name")           # Location name
                          locationID = location.get('id')                          # location ID
                          #print "location name = ", jmriName
                          #print "location ID = ", locationID

    # **************************************************************************************************************
                     trackList = isinstance(location, list)          # test if this is a list of tracks for this location (1 to many tracks)
                     if trackList :
                         #print "trackList is true"
                         #print "length of trackList = ", len(location)
                         numberTracks = len(location)
                         for each in range(numberTracks):
                             #print location[each]
                             matchedTrack = False
                             tracks = location[each]                     # test each track from list to see if Serial RFID has it assigned to a reader
                             matchedTrack = False
                             #print "tracks = ", tracks
                             trackName = tracks.get("name")    # track name
                             trackID = tracks.get('id')                  # track ID 
                             self.cb = str(trackID)                              # create name for JCheckBox if needed
                             #if matchedTrack == False:
                             for compare in assigned:                   # assigned is the list of assigned tracks
                                     #print "assigned = ", assigned
                                     #print "compare to = ", compare
                                     matchedTrack = False
                                     if  trackID == compare[1]:  # test if this track is in the assigned list
                                         if currentReader == compare[0]:
                                             self.cb = JCheckBox(compare[2], actionPerformed = self.on_check) 
                                             self.cb.selected = 1                 # set the check box display
                                             global cbList
                                             cbList.append(trackID)
                                             cbList.append(self.cb)
                                             self.rightPanel.add(self.cb)           # add track for display as assigned to this reader -- checked
                                             matchedTrack = True
                                             #print "trackassignment matched = true "
                                             break

                             if matchedTrack == False:
                                 for compare in assigned:                   # skip -- don't add it to for display
                                     if  trackID == compare[1]:              # test if this track assigned to any reader by matching ID's
                                         matchedTrack = True
                                         #print "some other reader matched = true "

                             if matchedTrack == False: 
                                 #print "matched = false "
                                 #print "trackID = ", trackID
                                 self.cb = JCheckBox(trackName, actionPerformed = self.on_check)
                                 global cbList
                                 cbList.append(trackID)
                                 cbList.append(self.cb)
                                 self.rightPanel.add(self.cb)           # add track for display as available -- unchecked
                                 #print "matched location but not selected "

             self.locPanel = JPanel()
             self.locPanel.setLayout(BoxLayout(self.locPanel, BoxLayout.X_AXIS))
             #self.locPanel.preferredSize = (Dimension(250,400))
             self.locPanel.setBorder(blackline)

             self.currentLocation = JLabel(jmriName)
             self.leftPanel.add(self.currentLocation)
             self.locPanel.add(self.leftPanel)
             self.locPanel.add(self.rightPanel)
             self.boxPanel.add(self.locPanel)

         self.scrollPane = JScrollPane(self.boxPanel)
         self.scrollPane.setPreferredSize(Dimension(360,300))
         self.scrollPane.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_ALWAYS)

         self.pack()
         global cbList
         return self.scrollPane   

     except:
         print "linkJmriLocationsToReader -- something wrong with sort_data"
         print "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]


if __name__ == "__main__":
    print "Running linkJmriLocationsGUI.py"
