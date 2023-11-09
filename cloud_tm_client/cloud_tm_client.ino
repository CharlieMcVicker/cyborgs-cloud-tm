// This file is made by splicing the stepper motor lab code for this course with
// This https://www.adventuresintechland.com/how-to-control-arduinos-serial-monitor-with-python/

// include a library of functions to use the servo
#include <AccelStepper.h> //Include AccelStepper library, via Arduino or Internet

// stepper definitions
#define DIR 7                   //DIR pin from A4988 to pin 7
#define STEP 4                  //STEP pin from A4988 to pin 4
#define MOTOR_INTERFACE_TYPE 1  //How many motors are connected (Maximum motors are 4)
byte numSteps = 0;              // The number of steps to take.
int currentSteps = 0;           // The current number of steps taken.
#define MAX_STEPS 100            // This is the maximum number of steps that will advance (You can modify this value).
#define FULLSTEP 4
#define STEP_PER_REVOLUTION 2048 // this value is from datasheet

AccelStepper stepper = AccelStepper(MOTOR_INTERFACE_TYPE, STEP, DIR); //Create a new instance of the AccelStepper class

int led = 13; // Pin 13

void setup()
{
  pinMode(led, OUTPUT); // Set pin 13 as digital out

  // Start serial connection
  Serial.begin(9600);
  Serial.flush();

  stepper.setMaxSpeed(1000.0);   // set the maximum speed
  stepper.setAcceleration(50.0); // set acceleration
  stepper.setSpeed(200);         // set initial speed
  stepper.setCurrentPosition(0); // set position
  stepper.moveTo(STEP_PER_REVOLUTION); // set target position: 64 steps <=> one revolution
}

void loop()
{
  String input = "";

  // Read any serial input
  while (Serial.available() > 0)
  {
    input += (char)Serial.read(); // Read in one char at a time
    delay(5);                     // Delay for 5 ms so the next char has time to be received
  }

  if (input == "on")
  {
    if (digitalRead(13) == HIGH)
    {
      Serial.write("Led is already ON \n");
    }
    else
    {
      digitalWrite(led, HIGH); // on
      Serial.write("LED is on \n");
    }
  }
  else if (input == "off")
  {
    if (digitalRead(13) == LOW)
    {
      Serial.write("Led is already OFF \n");
    }
    else
    {
      digitalWrite(led, LOW); // on
      Serial.write("LED is off \n");
    }
  }
}