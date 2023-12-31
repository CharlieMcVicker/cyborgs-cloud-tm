// This file is made by splicing the stepper motor lab code for this course with
// This https://www.adventuresintechland.com/how-to-control-arduinos-serial-monitor-with-python/

// include a library of functions to use the servo
#include <AccelStepper.h> //Include AccelStepper library, via Arduino or Internet

// stepper definitions
#define DIR 7                  // DIR pin from A4988 to pin 7
#define STEP 4                 // STEP pin from A4988 to pin 4
#define MOTOR_INTERFACE_TYPE 1 // How many motors are connected (Maximum motors are 4)
byte numSteps = 0;             // The number of steps to take.
int currentSteps = 0;          // The current number of steps taken.
#define MAX_STEPS 100          // This is the maximum number of steps that will advance (You can modify this value).
#define FULLSTEP 4
// I think maybe there are only 200 steps per rotation... the "step angle" is
// listed as 1.80º
#define STEP_PER_REVOLUTION 200 // this value is from datasheet -- this comment is from john, said 2048

AccelStepper stepper = AccelStepper(MOTOR_INTERFACE_TYPE, STEP, DIR); // Create a new instance of the AccelStepper class

void setup()
{
  // Start serial connection
  Serial.begin(9600);
  Serial.flush();

  // Setup the motor
  stepper.setMaxSpeed(100.0);   // set the maximum speed
  stepper.setAcceleration(20.0); // set acceleration
  stepper.setSpeed(200);         // set initial speed
  stepper.setCurrentPosition(0); // set position
  // stepper.moveTo(STEP_PER_REVOLUTION); // set target position: 64 steps <=> one revolution
}

enum State
{
  WaitingForCommand,
  Opening,
  Closing,
};

State state = WaitingForCommand;
String command = "";

void loop()
{

  switch (state)
  {
  case WaitingForCommand:
    command = Serial.readStringUntil('\n');
    if (command == "OPEN_VALVE")
    {
      Serial.println("opening");
      state = Opening;
      stepper.moveTo(STEP_PER_REVOLUTION / 4);
    }
    else if (command == "CLOSE_VALVE")
    {
      Serial.println("closing");
      state = Closing;
      stepper.moveTo(0);
    }
  case Opening:
  case Closing:
    runMotor();
  }
}

void runMotor()
{
  stepper.run();

  if (stepper.distanceToGo() == 0)
  {
    // mot sure what this does? maybe keeps it spinning?
    stepper.moveTo(stepper.currentPosition());

    switch (state)
    {
    case Closing:
      Serial.println("closed");
      break;
    case Opening:
      Serial.println("opened");
      break;
    }

    state = WaitingForCommand;
  }
}
