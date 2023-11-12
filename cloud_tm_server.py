import math
import time
from typing import List
from QtmTracker import QtmTracker
from qtm.packet import RT6DBodyEuler
from water_plant import connect_to_arduino_serial, water_plant
import matplotlib.pyplot as plt

BODY_NAME = "Finger1"

def collect_snapshots(tracker: QtmTracker):
    snapshots: List[RT6DBodyEuler] = []
    while True:
        # magic
        take_snapshot = input()
        if take_snapshot == "q":
            break
        else:
            time.sleep(5)
            start = current = time.time()
            end = start + 10
            while current < end:
                current = time.time()
                finger_angles = tracker.get_all_bodies()[BODY_NAME]
                print(finger_angles)
                snapshots.append(finger_angles)
            
            input("Done...")
            plt.plot([x.a1 for x in snapshots])
            plt.plot([x.a2 for x in snapshots])
            plt.plot([x.a3 for x in snapshots])
            plt.show()

def distance_from_start_gesture(eulers: RT6DBodyEuler):
    return abs(abs(eulers.a1) - 90) + abs(abs(eulers.a3) - 90)

def is_start_gesture(eulers: RT6DBodyEuler):
    return distance_from_start_gesture(eulers) < 30

def wait_for_gesture(tracker: QtmTracker):
    WIN_SIZE = 50
    rolling_average = 0.5
    while True:
        finger_angles = tracker.get_all_bodies()[BODY_NAME]
        if finger_angles.a1 != math.nan: # bad way to check for nan
            rolling_average = (rolling_average * (WIN_SIZE - 1) + is_start_gesture(finger_angles)) / WIN_SIZE
        print(rolling_average, distance_from_start_gesture(finger_angles))
        if rolling_average > .7:
            return

def wait_for_confirm(tracker: QtmTracker):
    """Make the user confirm their gesture by breaking the start position"""
    # TODO: make sound to show start of confirm block
    print("PLEASE CONFIRM")
    print("PLEASE CONFIRM")
    print("PLEASE CONFIRM")
    print("PLEASE CONFIRM")
    print("PLEASE CONFIRM")
    start = time.time()
    end = start + 5 # user has five seconds to be out of the position
    
    WIN_SIZE = 50
    rolling_average = 0.5
    while True:
        finger_angles = tracker.get_all_bodies()[BODY_NAME]
        cur_frame = is_start_gesture(finger_angles) if finger_angles.a1 > -200 else 1
        rolling_average = (rolling_average * (WIN_SIZE - 1) + cur_frame) / WIN_SIZE
        # print(rolling_average, abs(abs(finger_angles.a1) - 90) + abs(abs(finger_angles.a3) - 90))
        if rolling_average < .3:
            return True # user put their hand down
        if time.time() > end:
            return False

def main():
    # ip from VVValter code
    tracker = QtmTracker("10.76.30.91")
    arduino = connect_to_arduino_serial()
    # time.sleep(2)
    # water_plant(arduino)
    # while True:
    #     bodies = tracker.get_all_bodies()
    #     print(bodies)

    while True:
        wait_for_gesture(tracker)

        did_confrim = wait_for_confirm(tracker)
        if did_confrim:
            water_plant(arduino)
        else:
            time.sleep(2)


if __name__ == "__main__":
    main()
