from QtmTracker import QtmTracker
from water_plant import connect_to_arduino_serial, water_plant


def wait_for_gesture(tracker: QtmTracker):
    while True:
        bodies = tracker.get_all_bodies()
        # magic
        should_break = input()
        if should_break == "q":
            break


def wait_for_confirm(tracker: QtmTracker):
    # TODO: make sound to show start of confirm block
    while True:
        bodies = tracker.get_all_bodies()

        # do magic
        confirm_response = input("confirm gesture?")

        if confirm_response == "yes":
            return True
        elif confirm_response == "no":
            return False


def main():
    # ip from VVValter code
    tracker = QtmTracker("10.76.30.91")
    arduino = connect_to_arduino_serial()

    while True:
        wait_for_gesture(tracker)
        did_confrim = wait_for_confirm(tracker)
        if did_confrim:
            water_plant(arduino)


if __name__ == "__main__":
    main()
