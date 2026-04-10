#include <SPI.h>
#include <SD.h>


// ===== Pins =====
const int lightPin = A0;       // Photoresistor output
const int chipSelect = 10;     // SD card module CS pin


File dataFile;


void setup() {
  Serial.begin(9600);
  delay(1000);


  Serial.println("Starting light logger...");


  // Initialize SD card
  Serial.print("Initializing SD card... ");
  if (!SD.begin(chipSelect)) {
    Serial.println("FAILED");
    while (true) {
      // Stop here if SD card init fails
    }
  }
  Serial.println("SUCCESS");


  // Create CSV file with header if it doesn't already exist
  if (!SD.exists("light.csv")) {
    Serial.println("light.csv not found. Creating file...");


    dataFile = SD.open("light.csv", FILE_WRITE);
    if (dataFile) {
      dataFile.println("elapsed_s,light_level");
      dataFile.close();
      Serial.println("Created light.csv with header.");
    } else {
      Serial.println("ERROR: Could not create light.csv");
      while (true) {
        // Stop here if file creation fails
      }
    }
  } else {
    Serial.println("light.csv already exists. Appending data.");
  }


  Serial.println("Logger is running...");
}


void loop() {
  // Time since Arduino started, in seconds
  unsigned long elapsed = millis() / 1000;


  // Read photoresistor
  int lightValue = analogRead(lightPin);


  // Print to Serial Monitor
  Serial.print(elapsed);
  Serial.print(",");
  Serial.println(lightValue);


  // Open file, append data, close file
  dataFile = SD.open("light.csv", FILE_WRITE);


  if (dataFile) {
    dataFile.print(elapsed);
    dataFile.print(",");
    dataFile.println(lightValue);
    dataFile.close();


    Serial.println("WRITE SUCCESS");
  } else {
    Serial.println("ERROR: Could not open light.csv");
  }


  delay(5000);  // Log every 5 seconds
}
