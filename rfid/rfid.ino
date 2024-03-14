/**
* "Object Placement" Puzzle
*
* This puzzle requires the player to place one or more items in the
* correct location, at which point an RFID tag embedded in the object
* is detected by a sensor.
* When all sensors read the tag of the correct object, the puzzle is solved.
*
* Demonstrates:
* - SPI interface shared between several devices
* - RFID library
*/

// DEFINES
// Provides debugging information over serial connection if defined
#define DEBUG

// LIBRARIES
// Standard SPI library comes bundled with the Arduino IDE
#include <SPI.h>
// Download and install from https://github.com/miguelbalboa/rfid
#include <MFRC522.h>

// CONSTANTS
// The number of RFID readers
const byte numReaders = 4;
// Each reader has a unique Slave Select pin
const byte ssPins[] = {2, 3, 4, 5};
// They'll share the same reset pin
const byte resetPin = 8;
// This pin will be driven LOW to release a lock when puzzle is solved
const byte lockPin = A0;
// The sequence of NFC tag IDs required to solve the puzzle
const String correctIDs[] = { "a4feee5b",  "4cb805e",  "a4dadf5b", "a4fe595b" };
const String correctIDs2[] = { "14271c5e",  "b45625b",  "14a1ff5e", "4e28a5e" };

// GLOBALS
// Initialise an array of MFRC522 instances representing each reader
MFRC522 mfrc522[numReaders];
// The tag IDs currently detected by each reader
String currentIDs[numReaders];


/**
 * Initialisation
 */
void setup() {

  #ifdef DEBUG
  // Initialise serial communications channel with the PC
  Serial.begin(9600);
  Serial.println(F("Serial communication started"));
  #endif
  
  // Set the lock pin as output and secure the lock
  pinMode(lockPin, OUTPUT);
  digitalWrite(lockPin, HIGH);
  
	// We set each reader's select pin as HIGH (i.e. disabled), so 
	// that they don't cause interference on the SPI bus when
	// first initialised
	for (uint8_t i=0; i<numReaders; i++) {
		pinMode(ssPins[i], OUTPUT);
		digitalWrite(ssPins[i], HIGH);
	}
	
  // Initialise the SPI bus
  SPI.begin();

  for (uint8_t i=0; i<numReaders; i++) {
  
    // Initialise the reader
    // Note that SPI pins on the reader must always be connected to certain
    // Arduino pins (on an Uno, MOSI=> pin11, MISO=> pin12, SCK=>pin13)
    // The Slave Select (SS) pin and reset pin can be assigned to any pin
    mfrc522[i].PCD_Init(ssPins[i], resetPin);
    
    // Set the gain to max - not sure this makes any difference...
    // mfrc522[i].PCD_SetAntennaGain(MFRC522::PCD_RxGain::RxGain_max);
    
	#ifdef DEBUG
    // Dump some debug information to the serial monitor
    Serial.print(F("Reader #"));
    Serial.print(i);
    Serial.print(F(" initialised on pin "));
    Serial.print(String(ssPins[i]));
    Serial.print(F(". Antenna strength: "));
    Serial.print(mfrc522[i].PCD_GetAntennaGain());
    Serial.print(F(". Version : "));
    mfrc522[i].PCD_DumpVersionToSerial();
	#endif
    
    // Slight delay before activating next reader
    delay(100);
  }
  
  #ifdef DEBUG
  Serial.println(F("--- END SETUP ---"));
  #endif
}

/**
 * Main loop
 */
void loop() {

  // Assume that the puzzle has been solved
  boolean puzzleSolved = true;

  // Assume that the tags have not changed since last reading
  boolean changedValue = false;

  // Loop through each reader
  for (uint8_t i=0; i<numReaders; i++) {
    boolean match = false;

    // Initialise the sensor
    mfrc522[i].PCD_Init();
    
    // String to hold the ID detected by each sensor
    String readRFID = "";
    
    // If the sensor detects a tag and is able to read it
    if(mfrc522[i].PICC_IsNewCardPresent() && mfrc522[i].PICC_ReadCardSerial()) {
      // Extract the ID from the tag
      readRFID = dump_byte_array(mfrc522[i].uid.uidByte, mfrc522[i].uid.size);
    }
    
    // If the current reading is different from the last known reading
    if(readRFID != currentIDs[i]){
      // Set the flag to show that the puzzle state has changed
      changedValue = true;
      // Update the stored value for this sensor
      currentIDs[i] = readRFID;
    }
    
    // If the reading fails to match the correct ID for this sensor 
    if(currentIDs[i] == correctIDs[i]) {
      match = true;
    }
    if (currentIDs[i] == correctIDs2[i]) {
      match = true;
    }

    if (match == false) {
      // The puzzle has not been solved
      puzzleSolved = false;
    }

    // Halt PICC
    mfrc522[i].PICC_HaltA();
    // Stop encryption on PCD
    mfrc522[i].PCD_StopCrypto1(); 
  }

  #ifdef DEBUG
  // If the changedValue flag has been set, at least one sensor has changed
  if(changedValue){
    // Dump to serial the current state of all sensors
    for (uint8_t i=0; i<numReaders; i++) {
      Serial.print(F("Reader #"));
      Serial.print(String(i));
      Serial.print(F(" on Pin #"));
      Serial.print(String((ssPins[i])));
      Serial.print(F(" detected tag: "));
      Serial.println(currentIDs[i]);
    }
    Serial.println(F("---"));
  }
  #endif

  // If the puzzleSolved flag is set, all sensors detected the correct ID
  if(puzzleSolved){
    onSolve();
  }
 
  // Add a short delay before next polling sensors
  //delay(100); 
}

/**
 * Called when correct puzzle solution has been entered
 */
void onSolve(){

  #ifdef DEBUG
  // Print debugging message
  Serial.println(F("Puzzle Solved!"));
  #endif
  
  // Release the lock
  digitalWrite(lockPin, LOW);

  while(true) {
    delay(1000);
  }
  
}

/**
 * Helper function to return a string ID from byte array
 */
String dump_byte_array(byte *buffer, byte bufferSize) {
  String read_rfid = "";
  for (byte i=0; i<bufferSize; i++) {
    read_rfid = read_rfid + String(buffer[i], HEX);
  }
  return read_rfid;
}
