# from https://www.adventuresintechland.com/how-to-control-arduinos-serial-monitor-with-python/
from serial import Serial  # pySerial
import time
from enum import Enum


def connect_to_arduino_serial():
    # If on Windows or "No such file '/dev/ttyACM0'" change
    # to serial.Serial(9600)
    # TODO: what should this address be
    return Serial("/dev/ttyACM0", 9600)


class ArdunioCommand(Enum):
    OPEN_VALVE = b"OPEN_VALVE"
    CLOSE_VALVE = b"CLOSE_VALVE"


def send_command(arduino: Serial, command: ArdunioCommand):
    arduino.write(command.value)  # send command
    arduino.write(b"\n")  # terminator
    arduino.flush()  # do we need this?


SECONDS_TO_OPEN = 4


def water_plant(arduino: Serial):
    print("Starting watering cycle")

    print("Opening valve...", end=" ", flush=True)
    send_command(arduino, ArdunioCommand.OPEN_VALVE)

    result = arduino.read_until().strip()
    assert (
        result == b"opening"
    ), f"Expected valve to start opening, got response {result.decode()}"

    result = arduino.read_until().strip()
    assert (
        result == b"opened"
    ), f"Expected valve to fully open, got response {result.decode()}"

    print("open")

    time.sleep(SECONDS_TO_OPEN)

    print("Closing valve...", end=" ", flush=True)
    send_command(arduino, ArdunioCommand.CLOSE_VALVE)

    result = arduino.read_until().strip()
    assert (
        result == b"closing"
    ), f"Expected valve to start closing, got response {result.decode()}"

    result = arduino.read_until().strip()
    assert (
        result == b"closed"
    ), f"Expected valve to fully close, got response {result.decode()}"

    print("closed")

    print("End of watering cycle")
