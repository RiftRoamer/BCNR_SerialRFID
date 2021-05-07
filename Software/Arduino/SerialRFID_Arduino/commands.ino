
// ---------------------------- command structure --------------------------------
// -------------------------------------------------------------------------------
//                    * = beginning of command from master         (ASCII 42)
//                    A - Y capital letter reader address (Z) = global address
//                    01 -99 command number
//                    ~ = separator in data stream                 (126)
//                    - = a no request reply to a master query     (45)
//                    ! = more reply data to come from a reader    (33)
//                    ^ = end of reply data from a reader          (94)
//                    ? = reader is replying to a query by sending datato the master  (63)
//                    \n = end of command
//
//                    *A09data~data~data~data\n   command from master
//                    -A08\n                      reader query reply
//                    ?A01data~data\n             reader query reply with request


// ************************************** command 1 ***************************************
// *********************************** Add car to engine "Pull car"  ************************************
void command1(){
      //Serial.println("got to command 1");               
      if (Assigned == "none"){
             //Serial.println("do nothing ----------");
      }else{
             lcd.clear();
             lcd.setCursor(0,0);
             lcd.print("Picking up Car");
             lcd.setCursor(0,1);
             lcd.print(newID);
             lcd.setCursor(0,2);
             lcd.print("-- Pulled --");
             //lcd.setCursor(0,3);
             //lcd.print("");
             //delay(750);
             String temp, temp2;
             temp.concat(Assigned); temp.replace(" ", "");
             temp2.concat(newID);   temp2.replace(" ", "");
             commandData = "?"; commandData.concat(address); commandData.concat("01"); commandData.concat(temp); commandData.concat("~"); commandData.concat(temp2);
      } 
}

// ************************************** command 2 ***************************************
// *********************************** Drop car to this reader "drop car" ************************************
void command2(){
  //Serial.println("got to command 2");
  // leave car at this reader "drop"
  if (Assigned == "none"){
          //Serial.println("do nothing ----------");
  }else{
          lcd.clear();
          lcd.setCursor(0,0);
          lcd.print("Dropping Car");
          lcd.setCursor(0,1);
          lcd.print(Assigned);
          lcd.setCursor(0,2);
          lcd.print("-- Dropped --");
          //lcd.setCursor(0,3);
          //lcd.print("");
          //delay(750);
          String temp, temp2;
          temp.concat(address); temp.replace(" ", "");
          temp2.concat(newID);   temp2.replace(" ", "");
          commandData = "kelly";
          commandData = "?"; commandData.concat(address); commandData.concat("02"); commandData.concat(temp); commandData.concat("~"); commandData.concat(temp2);

 }
}

// ************************************** command 3 ***************************************
// ****************************** Assign engine to this reader ****************************
void command3(){
          
          //Serial.println("----------   got to command 3 --------------");
          //Serial.println(Assigned);
          lcd.clear();
          lcd.setCursor(0,0);
          lcd.print("engine");
          lcd.setCursor(0,1);
          lcd.print(Assigned);
          lcd.setCursor(0,2);
          lcd.print("is asssigned");
          lcd.setCursor(0,3);
          lcd.print("to this reader");
          //delay(750);
          Assigned = newID;
}

// ***************************************** command 4 ************************************
// ******************************** Read card RFID tag number *****************************
void command4(){
  //Serial.println("got to command 4");
  carTag = ReadCard(0,0,3);
  //Serial.print("command 4 theCard = ");
  //Serial.println(carTag);
  
}

// ************************************** command 5 ***************************************
// ******************************** not implimented ********************************
//void command5(){
//}

// ************************************** command 6 ***************************************
// *********************************** not implimented ************************************
//void command6(){
//}

// ************************************** command 7 ***************************************
// *********************************** not implimented ************************************
//void command7(){
//}

// ************************************** command 8 ***************************************
// *********************************** polling command ************************************
void command8(){
    // implimented directly by command select (case 8) 
}

// ************************************** command 9 ***************************************
// ********************************* write car to RFID tag ********************************
String command9(){
  //Serial.println("got to command 9");
  //Serial.print("Data = ");Serial.println(commandString);
  //Serial.println (strlen(commandString));
  char chr;                                    // test each character in commanddata
  int x;                                       // holdnumber of characters in commandData
  int y = 0;                                   // limit length of each data item in commandData
  int index = 0;                               // track each piece of data
  //String pharse[6];                          // array for 6 items
  char pharse[6][17];                          // hold 6 items (18 char each)
  char item[17];                               // hold 1 data item
  x = strlen(commandString);     
  //Serial.print("x = ");Serial.println(x);
  for ( int i=3; i < x; i++){                  // iterate each data character
    chr = commandString[i];                    // start at 3 to remove address & command A09
    //Serial.print("command chr = ");Serial.println(chr);
    if ((chr != '~') && (y < 16)){             // data item seperater
      pharse[index][y] = chr;                  // build data item     
      y = y+1;                                 // increment data length
    }
    else {
      //Serial.print("index = ");Serial.println(index);
      pharse[index][y] = 0;                    // terminate string
      //Serial.print("pharse[index] = ");Serial.println(pharse[index]);
      index = index+1;                         // move to next array element
      y = 0;
    }
  }
    carType =  pharse[0];                      // move char array element to a string
    carColor = pharse[1];
    carName =  pharse[2];
    carNumber= pharse[3];
    carOwner = pharse[4];
    carID =    pharse[5];

    //Serial.print("carType = "); Serial.println(pharse[0]);
    //Serial.print("carColor = "); Serial.println(pharse[1]);
    //Serial.print("carName = "); Serial.println(pharse[2]);
    //Serial.print("carNumber = "); Serial.println(pharse[3]);
    //Serial.print("carOwner = "); Serial.println(pharse[4]);
    //Serial.print("carID = "); Serial.println(pharse[5]);
    String state = "";                        // prep test for card ready
    state = WriteCardData();                  // do the write

    return state;
 }

// ************************************** command 10 **************************************
// *********************************** not implimented ************************************
//void command10(){
//}
