char address = 'A';  //legal upper A to Y
// this is board with rfid reader
String command9();
#include <string.h>
//#include "checkRFIDcard.ino"
//#include "commands.ino"

// ************** software serial configuration *************************
#include <SoftwareSerial.h>
#define rxPin 8
#define txPin 7
#define _SS_MAX_RX_BUFF 128 // RX buffer size
SoftwareSerial mySerial(rxPin, txPin); // RX-RO, TX-DI
int enablePin = 4; // enable pin for slave

// ************** LCD display configuration   ***************************
#include <Wire.h> 
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27,20,4);  // set the LCD address to 0x27 for a 20 chars and 4 line display

// **************** Main Loop configuration  *****************************
boolean commandComplete = false;   // whether the string is complete
long BAUD = 9600;
char commandString[125];           // a string to hold incoming data
String Assigned = "none";          // assume JMRI mode at startup
String test = "open";
unsigned long cardTime = 0;       // 2 second timer
unsigned long holdTime = 0;       // 2 second timer
unsigned long poll = 0;           // timer result for checking RFID reader
String commandData = "";          // pull/drop data to send back as query result

// ****************** RFID reader configuration  *************************
#include <SPI.h>
#include <MFRC522.h>
#define SS_PIN 10
#define RST_PIN 9
#define Green A3
#define Red A2
#define Drop A1
#define Pull A0
#define Assign 2

MFRC522 mfrc522(SS_PIN, RST_PIN); // Instance of the class
MFRC522::StatusCode status;
MFRC522::MIFARE_Key key; 

byte nuidPICC[4];
String carType;         // primarily used in WriteCarData
String carColor;        // 
String carName;         // 
String carNumber;       //
String carOwner;        //
String carID;           //
String carTag;          // 

char newType[17];       // primarily used in ReadCarData
char newColor[17];
char newName[17];
char newNumber[17];
char newOwner[17];
char newID[17];
char newTag[17];

char msgArray[18];
char sizedData[16];        // buffer for dump_byte_array()

void dump_byte_array(byte *buffer, byte bufferSize);
String openCard();

//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//+++++++++++++++++++++++++++     Setup      ++++++++++++++++++++++++++++++
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


void setup()
{
  // ******************** mySerial & LCD display *************************
 pinMode(rxPin, INPUT);
  pinMode(txPin, OUTPUT);
  lcd.init();                      // initialize the lcd 
  lcd.backlight();
  lcd.print("Jim Kelly");     //Welcome Message
  lcd.setCursor(0,1); 
  lcd.print("RFID Reader");
  delay(2000);
  lcd.clear();
  mySerial.begin(BAUD);
  // setup enable pin for slave (always low)
  pinMode(enablePin, OUTPUT);
  pinMode(13, OUTPUT);
  digitalWrite(13, HIGH);
  delay(1000);
  digitalWrite(enablePin, LOW);
  digitalWrite(13, LOW);
  
  // ******************** RFID reader **********************************
  
  SPI.begin(); // Init SPI bus
  pinMode(SS_PIN, OUTPUT);
  mfrc522.PCD_Init();
  mfrc522.PCD_ClearRegisterBitMask(mfrc522.RFCfgReg, (0x07<<4));
  mfrc522.PCD_SetRegisterBitMask(mfrc522.RFCfgReg, (0x07<<4));
  if (status != MFRC522::STATUS_OK) {
  //Serial.print(F("Init() failed: "));
  //Serial.println(mfrc522.GetStatusCodeName(status));
  }
  digitalWrite(RST_PIN, HIGH); 
  for (byte i = 0; i < 6; i++) {  // prepare key FFFFFFFFFFFFh
    key.keyByte[i] = 0xFF;
  }

 // ************************ Main Loop *******************************
  pinMode(Green, OUTPUT);    // reading card + (blink)this card has incoming RX data
  digitalWrite(Green, HIGH);
  delay(1000);
  digitalWrite(Green, LOW);
  pinMode(Red, OUTPUT);     // card present + (blink) RX active
  digitalWrite(Red, LOW);
  pinMode(Pull, INPUT_PULLUP);
  pinMode(Drop, INPUT_PULLUP);
  pinMode(Assign, INPUT_PULLUP);
  Serial.begin(9600);
  //Serial.println(F("This code scan the MIFARE Classsic NUID."));
  Serial.print(F("Using the following key:"));
  dump_byte_array(key.keyByte, MFRC522::MF_KEY_SIZE);
  //flag = false;
  cardTime = millis();
  holdTime = millis();
  
}

// ****************************************************************************
// ***********************      Main Loop      ********************************
// ****************************************************************************


void loop(){

 cardTime = millis();
 poll = cardTime - holdTime;
 bool add = false;           // capture incoming buffer
 bool skip = false;          // buffer not captured
 char inChar = "";           // incoming byte
 int i =0;                   // count critical byte placement
 int state = 0;              // remember if card present (red = on)
 bool trap = false;          // capture state just once
 bool thisNode = false;      // select LED flicker pattern
 
 // ********************** panel switches ******************************
 
 if (not digitalRead(Pull)) {
     //Serial.println("******** pick up **********");
     command1();           // take car from this reader "pull" pick-up car  
     
 }
 
 if (not digitalRead(Drop)) { 
     command2();            // drop car at this reader "drop" leave car
 }

 if (not digitalRead(Assign)){   
     command3();            // assign engine to this readeer
 }


// ************************  start of COMM check *******************************

 
 while (mySerial.available()> 0) {       // monitor COMM bus from master
    if (not trap) {                      
        state = digitalRead(Red);        // set once on first entry to while 
        trap = true;                     // card present on reader
    }
    if (not thisNode){                   // incoming not adddressed for this node
        digitalWrite(Red, LOW);          // blink pattern
        delay(1);
        digitalWrite(Red, HIGH);
        delay(1);
        digitalWrite(Red, LOW);
    }

    inChar = (char)mySerial.read();                  // get the new byte:
    //Serial.print("i = ");
    //Serial.println(i);     
    //Serial.println(inChar);
    if (!skip){                                      // not valid start bit
         switch (i) {                                // which byte are we looking at
           case 0:
                if (inChar == '*'){                  // check for "command start (*)" char
                   //Serial.println("good *"); 
                   commandString[0] = 0;             // drop commnad start char
                }else{
                   skip = true;                      // not at command start
                   //Serial.println("skip 0");       
                }
                break;
           case 1:
                if (inChar == address){                     // check node address char (A -Y)
                   add = true;                       // remember address match
                   commandString[i-1] = inChar;
                   thisNode = true;                  // change flicker pattern
                   Serial.println("good address"); 
                }else{
                   skip = true;
                   commandString[0] = 0;
                   //Serial.println("skip 1");
                }  
                break;
           default:
                if (add){                                // collect all bytes
                   digitalWrite(Red, LOW);               // blink pattern
                   digitalWrite(Green, LOW);
                   delay(2);
                   digitalWrite(Red, HIGH);
                   digitalWrite(Green, HIGH);
                   delay(2);
                   digitalWrite(Red, LOW);
                   digitalWrite(Green, LOW);
                   delay(2);
                   commandString[i-1] = inChar;           // capture command
                   if (inChar == '\n') {                  // if the incoming character is 
                       commandComplete = true;            // a newline, set the flag so the
                                                          // main loop can do something about it:
                       trap = false;                      // reset for next test
                       thisNode = false;                  // reset for next test    
                       digitalWrite(Red, state);          // reset LED is card present ?
                       digitalWrite(Green, LOW);                                   
                       
                   }                                      
                }
                break;
         }
       i++;                                               // track next byte
       
      }
      else{
           trap = false;
           digitalWrite(Red, state);
      }   

    // No match means not a command from master ignore and cycle to clear buffer
    //                            OR     
    // wrong node address so cycle to empty buffer do nothing but clear buffer

 }  // end while  ******* end of COMM check **********
 


// ************************ start of command select ********************************

  if (commandComplete) {                           // pharse selected command
    String command;                                // all commands must be 2 characters long
    String reply = "";                             // sent back to master

    String prefix = "-";                           // add to reply - character changes based on command
    //Serial.println(commandComplete);                                        
    //if (commandString[1] == address) { // **** [0] ?????????
    if (address == address) {                      // make sure this message is for this   
                                                   // node. address A-Y
                                                   // skip commands if not an address match
                
        
        command = "";                              // all commands must be 2 characters long
        command = commandString[1];                // pharse command
        command.concat(commandString[2]);          // pharse command continued
        //Serial.print("command = ");
        //Serial.println(command);
        
        //reply = "-";                             // all no request replies start with "-"
        reply.concat(commandString[0]);            // add node address to reply
        reply.concat(command);                     // add command to reply  (-A08)
         
        
        int target = command.toInt();              // convert to integer for switch 
        //Serial.print("target = ");
        //Serial.println(target);
        String cmdReturn = "";
        int x = 0;                                 // is reader sending a query reply command
        switch (target) {                          // match command number
             case 1:  
                    // move car to engine -- "pick up"
                    // implimented by direct call using the pull panel switch
                    x = 0; // does nothing -- prevents compiler case failure
                    break;
              case 2: 
                    // leave car at this reader "drop" 
                    // implimented by direct call using the drop panel switch
                    x = 0;
                    break;
              case 3: 
                    // assign this engine to this reader
                    // implimented by direct call using the assign panel switch
                    x = 0;
                    break;
              case 4: // master wants RFID tag for car on reader
                    command4();
                    prefix = "-";
                    prefix.concat(reply);
                    reply = prefix;
                    reply.concat(carTag);
                    reply.concat("\n");                        // terminate reply 
                    sendReply(reply);
                    break;
              case 5: 
                    x = 0;
                    break;
              case 6:  
                    x = 0;
                    break;
               case 7:  
                    x = 0;
                    break;                                   
              case 8:  // query from master
                    //command8();
                    x = commandData.length();                    // this reader sending "pull" or "drop" request
                    //Serial.print("command 8 commandData =");
                    //Serial.println(x);
                    if (x > 0){                                  // that will be sent with next query from the master
                         reply = commandData;
         
                    }else{
                         prefix = "-";
                         prefix.concat(reply);                   // no request return reader address
                         reply = prefix;
                    }
                    reply.concat("\n");                          // terminate reply 
                    //Serial.print("--- #8 reply =  ----");
                    //Serial.println(reply);
                    sendReply(reply);
                    commandData = "";                            // prevent repeat of commands
                    break;                      
               case 9:  // Master wants to write car data to RFID chip on the car
                    //Serial.println("case 9  = ");
                    //Serial.println(reply);
                    cmdReturn = command9();
                    prefix = "-";
                    prefix.concat(reply);
                    reply = prefix;
                    reply.concat("\n");                        // terminate reply 
                    sendReply(reply);
                    break;                     
               case 10:
                    x = 0;
                    break;                    
              default:  // capture comm errors and recover
                    x = 0;
                    //Serial.println("default case");
                    //prefix = "-";
                    //prefix.concat(reply);
                    //reply = prefix;
                    //sendReply(reply);
                    break;
        }
      
    }     

      commandString[0] = 0;                       // clear the command
      commandComplete = false;                    // drop out of command select
    
 } // ****  end of command select ****


//*************************** start of card present test *************************

  if (poll >= 2500){                                // Check for car on reader every 2 1/2 seconds
    //Serial.print("poll = ");
    //Serial.println(poll);
    poll = 0;                                       // reset counter
    //Serial.print("test = ");
    //Serial.println(test);
     if (test == "open")                            // look for tag on reader
        {
            lcd.clear();
            lcd.setCursor(0,0);
            lcd.print("No Car");
            digitalWrite(Red, LOW);                 // no car present
            digitalWrite(Green, LOW);               // no read or write active
            test = openCard();
            //Serial.print("test open returned -- ");
            //Serial.println(test);
        }
  
     if (test == "opened") {
            digitalWrite(Red, HIGH);                // car present
            test = ReadCardData();                  // get RFID tag & display car infomation
            lcd.clear();
            lcd.setCursor(0,0);
            lcd.print(newType);
            lcd.setCursor(0,1);
            lcd.print(newColor);
            lcd.setCursor(0,2);
            lcd.print(newID);
            lcd.setCursor(0,3);
            lcd.print(newOwner);
        }    
     if (test == "read failed")                      // reset loop and try again
        {
            test = "open";
            lcd.clear();
            lcd.setCursor(0,0);
            lcd.print("Read Failed");
            digitalWrite(Red, LOW);                  // no car present
            digitalWrite(Green, LOW);                // no read or write active
            //delay(1000);
        }
     if (test == "write failed")                     // reset loop and try again
        {
             test = "open";
             lcd.clear();
             lcd.setCursor(0,0);
             lcd.print("Write Failed");
             digitalWrite(Red, LOW);                 // no car present
             digitalWrite(Green, LOW);               // no read or write active
             //delay(1000);
          
        }
       
     holdTime = millis();
     //Serial.println(test);
  } //  ***** end of 2 second card test ******  

} // *** end of main loop *****


//********************************** start of command reply *********************************************

void sendReply(String TX){
      //Serial.print("send reply = ");
      //Serial.println(RX);
      digitalWrite(enablePin, HIGH);              // enabel RS-485 TX mode
      mySerial.print(TX);                         // send back command recieved
      //mySerial.flush();                         
      digitalWrite(enablePin, LOW);               // enable RS-485 RX mode 
      commandString[0] = 0;
      //delay(15);
}  //*********** end of command reply **********
