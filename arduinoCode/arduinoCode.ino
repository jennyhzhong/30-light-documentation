#include <SPI.h>   // Enables SPI communication, which the microSD module uses
#include <SD.h>    // Lets the Arduino create, open, and write files on the microSD card

// =========================
// Pin Definitions
// =========================
const int lightPin = A0;      // Analog pin connected to the photoresistor voltage divider output
const int chipSelect = 10;    // microSD module CS (chip select) pin

// File object used for writing data to the CSV file
File dataFile;

void setup() {
  // Start Serial Monitor so we can see status messages and sensor readings
  Serial.begin(9600);

  // Small delay to give the Serial Monitor time to start
  delay(1000);

  Serial.println("Starting light logger...");

  // =========================
  // Initialize the microSD card
  // =========================
  Serial.print("Initializing SD card... ");

  // SD.begin() tries to start communication with the microSD card
  // If this fails, the Arduino stops here
  if (!SD.begin(chipSelect)) {
    Serial.println("FAILED");

    // Infinite loop: stop the program if SD card initialization fails
    while (true) {
      // Do nothing
    }
  }

  Serial.println("SUCCESS");

  // =========================
  // Check whether the CSV file already exists
  // =========================
  if (!SD.exists("light.csv")) {
    Serial.println("light.csv not found. Creating file...");

    // Open the file in write mode
    dataFile = SD.open("light.csv", FILE_WRITE);

    if (dataFile) {
      // Write the CSV header only once when the file is first created
      dataFile.println("elapsed_s,light_level");

      // Always close the file after writing
      dataFile.close();

      Serial.println("Created light.csv with header.");
    } else {
      Serial.println("ERROR: Could not create light.csv");

      // Stop program if file creation fails
      while (true) {
        // Do nothing
      }
    }
  } else {
    // If the file already exists, the program will append new data to it
    Serial.println("light.csv already exists. Appending data.");
  }

  Serial.println("Logger is running...");
}

void loop() {
  // =========================
  // Get elapsed time
  // =========================
  // millis() returns the number of milliseconds since the Arduino started running
  // Dividing by 1000 converts it to seconds
  unsigned long elapsed = millis() / 1000;

  // =========================
  // Read light sensor value
  // =========================
  // analogRead() returns a value from 0 to 1023
  // based on the voltage at pin A0
  int lightValue = analogRead(lightPin);

  // =========================
  // Print data to Serial Monitor
  // =========================
  // This lets you see the readings live while the Arduino is running
  Serial.print(elapsed);
  Serial.print(",");
  Serial.println(lightValue);

  // =========================
  // Open CSV file and append one new row
  // =========================
  dataFile = SD.open("light.csv", FILE_WRITE);

  if (dataFile) {
    // Write elapsed time
    dataFile.print(elapsed);
    dataFile.print(",");

    // Write sensor reading, then move to a new line
    dataFile.println(lightValue);

    // Close the file so data is actually saved
    dataFile.close();

    Serial.println("WRITE SUCCESS");
  } else {
    // If the file could not be opened, print an error
    Serial.println("ERROR: Could not open light.csv");
  }

  // =========================
  // Wait before next reading
  // =========================
  // 5000 ms = 5 seconds
  delay(5000);
}
