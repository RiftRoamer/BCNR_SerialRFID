 
#include <stdio.h>
#include <string.h>

String ReadCard (int sector, int blockAddr, int trailerBlock);
String ReadBlock (int sector, int blockAddr, int trailerBlock);

// ************************************************************
String displayCar(){
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print(carType);
  lcd.setCursor(0,1);
  lcd.print(carColor);
  lcd.setCursor(0,2);
  lcd.print(carName);
  lcd.setCursor(0,3);
  lcd.print(carNumber);
return "opened";
} 

// **************************************************************
String ReadCardData (){
    String stat = "";
    //String failed = "read failed";
    delay(20);
    digitalWrite(Green, HIGH);
    stat = ReadBlock(1,4,7);
    strcpy(newType, msgArray);
    if (stat == "bad"){
      return "read failed";
    }
    delay(20);
    digitalWrite(Green, LOW);
    //Serial.print("carType = ");
    //Serial.println(newType);
    
    delay(20);
    digitalWrite(Green, HIGH);
    stat = ReadBlock(1,5,7);
    strcpy(newColor, msgArray);
    if (stat == "bad"){
      return "read failed";
    }
    delay(20);
    digitalWrite(Green, LOW);
    //Serial.print("carColor = ");
    //Serial.println(newColor);
    
    delay(20);
    digitalWrite(Green, HIGH);
    stat = ReadBlock(1,6,7);
    strcpy(newName, msgArray);
    if (stat == "bad"){
      return "read failed";
    }
    delay(20);
    digitalWrite(Green, LOW);
    //Serial.print("carName = ");
    //Serial.println(newName);

    delay(20);
    digitalWrite(Green, HIGH);
    stat = ReadBlock(2,8,11);
    strcpy(newNumber, msgArray);
    if (stat == "bad"){
      return "read failed";
    }
    delay(20);
    digitalWrite(Green, LOW);
    //Serial.print("carNumber = ");
    //Serial.println(newNumber);
    
    delay(20);
    digitalWrite(Green, HIGH);
    stat = ReadBlock(2,9,11);;
    strcpy(newOwner, msgArray);
    if (stat == "bad"){
      return "read failed";
    }
    delay(50);
    digitalWrite(Green, LOW);
    //Serial.print("carOwner = ");
    //Serial.println(newOwner);
    
    delay(20);
    digitalWrite(Green, HIGH);
    stat = ReadBlock(3,12,15);
    strcpy(newID, msgArray);
    if (stat == "bad"){
      return "read failed";
    }
    delay(20);
    digitalWrite(Green, LOW);

    return "opened";

}

// *************************************************************
String WriteCardData (){
    String stat = "" ;
    stat = WriteBlock(carType,4,7);
    if (stat == "bad"){
      return "write failed";
    }
    //Serial.println(stat);
    // for engines carColor holds model information
    stat = WriteBlock(carColor,5,7);
    if (stat == "bad"){
      return "write failed";
    }
    //Serial.println(stat);
    stat = WriteBlock(carName,6,7);
    if (stat == "bad"){
      return "write failed";
    }
    //Serial.println(stat);
    stat = WriteBlock(carNumber,8,11);
    if (stat == "bad"){
      return "write failed";
    }
    //Serial.println(stat);
    stat = WriteBlock(carOwner,9,11);
    if (stat == "bad"){
      return "write failed";
    }
    //Serial.println(stat);
    stat = WriteBlock(carID,12,15);
    if (stat == "bad"){
      return "write failed";
    }
    //Serial.println(stat);
    return "final good";
}

// ***************************************************************************
void dump_byte_array(byte *buffer, byte bufferSize) {
    for (byte i = 0; i < bufferSize; i++) {
        //Serial.print(buffer[i] < 0x10 ? " 0" : " ");
        //Serial.print(buffer[i], HEX);
        msgArray[i] = buffer[i];
        //Serial.print(msgArray[i]);
    }
}
// **********************************************************************
String openCard(){
for (int i=0; i<10; i++){
         if ( mfrc522.PICC_IsNewCardPresent()){
            mfrc522.PICC_ReadCardSerial();
            return "opened";
         }
         //Serial.print(F(" open i = "));
         //Serial.println(i);
   }
return "open"; 
} 
// ********************************************************************
String closeCard(){
     // Halt PICC
    mfrc522.PICC_HaltA();
    // Stop encryption on PCD
    mfrc522.PCD_StopCrypto1();
    return "open";
}
// *********************************************************************
String ReadBlock (int sector, int blockAddr, int trailerBlock){
    String eval= "bad";
    byte buffer[18];
    byte size = sizeof(buffer);
    // Authenticate using key A
    //Serial.println(F("Authenticating using key A..."));
    status = (MFRC522::StatusCode) mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, trailerBlock, &key, &(mfrc522.uid));
    if (status != MFRC522::STATUS_OK) {
         //Serial.print(F("PCD_Authenticate() failed: "));
         //Serial.println(mfrc522.GetStatusCodeName(status));
         return eval;
    }
    // Read data from the block
    //Serial.print(F("Reading data from block ")); Serial.print(blockAddr);
    //Serial.println(F(" ..."));
    status = (MFRC522::StatusCode) mfrc522.MIFARE_Read(blockAddr, buffer, &size);
    if (status != MFRC522::STATUS_OK) {
         //Serial.print(F("MIFARE_Read() failed: "));
         //Serial.println(mfrc522.GetStatusCodeName(status));
         return eval;
    }
    //Serial.print(F("Data in block ")); Serial.print(blockAddr); Serial.println(F(":"));
    dump_byte_array(buffer, 16); 
    //Serial.println();
    //Serial.println();
    int t = 0;
    for (int i=0; i<16; i++){
      t = msgArray[i] + 0;
      if ((t<32) || (t>126))    // check for random byte values that aren't acceptable ASCII
        {
           msgArray[i] = 35;    // change bad value to a space bar
        } 
    } 
  eval = "good";
return eval;  
}

// ********************************************
String WriteBlock (String storeData, int blockAddr, int trailerBlock){
    // Serial.println("enter function");
    String eval= "bad";
    lcd.clear();
    lcd.setCursor(0,0);
    lcd.print("Writing Car");
    storeData.trim();
    int w = storeData.length();
    if (w < 16) {     // data musst be length of 16
      for (int i=0; i < (16-w); i++){
        storeData += " "; 
      }
      // Serial.println("pad data");
      for (int i=0; i < 16; i++){
        sizedData[i] = storeData[i];
      }
    }
    else if (w > 16){  // remove excess characters
       for (int i=0; i < 16; i++){
        sizedData[i] = storeData[i];
      }
      // Serial.println("removed some data");
    }
    //MFRC522::StatusCode status;
    byte buffer[18];
    byte size = sizeof(buffer);
    // Authenticate using key A
    // Serial.println(F("Authenticating using key A..."));
    status = (MFRC522::StatusCode) mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, trailerBlock, &key, &(mfrc522.uid));
    if (status != MFRC522::STATUS_OK) {
        //Serial.print(F("PCD_Authenticate() failed: "));
        //Serial.println(mfrc522.GetStatusCodeName(status));
        return eval;
    }
 
    // Write data to the block
    // Serial.print(F("Writing data into block ")); Serial.print(blockAddr);
    // Serial.println(F(" ..."));
    //dump_byte_array(sizedData, 16); Serial.println();
    status = (MFRC522::StatusCode) mfrc522.MIFARE_Write(blockAddr, sizedData, 16);
    if (status != MFRC522::STATUS_OK) {
         //Serial.print(F("MIFARE_Write() failed: "));
         //Serial.println(mfrc522.GetStatusCodeName(status));
         return eval;
    }
    //digitalWrite(Green, LOW);
    // Serial.println("end of function");
    eval = "good";
return eval;

}
// ********************************************
String ReadCard (int sector, int blockAddr, int trailerBlock) {
   String content= "";
   for (byte i = 0; i < mfrc522.uid.size; i++) 
    {
     //Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
     //Serial.print(mfrc522.uid.uidByte[i], HEX);
     content.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
     content.concat(String(mfrc522.uid.uidByte[i], DEC));
    }
   //Serial.print("Message : ");
   //Serial.println(content);
   return content;
}
  
// ********************************************
