#!/usr/bin/env python3
# Source: Union College Evo-Robo Lab under John Rieffel
# Edited by Kyle Doney
# Edited by Charlie McVicker

"""
    Simple tracker class to aid getting a single tracked location
"""

import asyncio
from typing import Dict
import xml.etree.ElementTree as ET
import pkg_resources
import qtm
from qtm import QRTPacket
from qtm.packet import RT6DBodyEuler
import math
import numpy as np
from time import sleep


class QtmTracker:
    def __init__(self, ip):
        self.loop = asyncio.get_event_loop()
        self.connection = None
        self.xml_string = None
        self.ip = ip
        self.eulers = None  # Currently the Yaw of the first body in Radians
        self.position = None  # [x,y,z] average (center) of bodies
        self.bodyDictionary = {}  # Dict of QTM Bodies {ID Value, 'Body Name'}
        self.eulerDict = None
        self.loop.run_until_complete(self.__connect_to_qtm(self.ip))

    async def __connect_to_qtm(self, ip):
        while self.connection is None:
            self.connection = await qtm.connect(ip, version="1.21")

            if self.connection is None:
                print("Failed to connect: waiting 5s")
                await asyncio.sleep(30)

            self.xml_string = await self.connection.get_parameters(parameters=["6d"])

    async def ensure_connected(self):
        """
        I hope we can delete this fn
        """
        if self.connection is None or not self.connection.has_transport():
            await self.__connect_to_qtm(self.ip)

    def __on_packet(self, packet: QRTPacket):
        """Handles a data packet. Updates the Global Position and Rotation of the tracked bodies. Averages to get the center of robot."""
        data = packet.get_6d_euler()

        if data is None:
            return

        info, bodies = data
        numBodies = info[0]
        # print("bodyDict", self.bodyDictionary)
        posDict = {}
        self.eulerDict = {} if self.eulerDict is None else self.eulerDict

        for bodyKey in self.bodyDictionary:
            posDict[bodyKey] = bodies[bodyKey][0]
            self.eulerDict[bodyKey] = bodies[bodyKey][1]

        x = y = z = 0
        for bodyPosition in posDict.values():
            x += bodyPosition[0]
            y += bodyPosition[1]
            z += bodyPosition[2]

        # Prevents bad values being saved
        if not math.isnan(x) and not math.isnan(y) and not math.isnan(z):
            self.position = [x / 3, y / 3, z / 3]

        if not math.isnan(self.eulerDict[0][2]):
            self.eulers = math.radians(
                self.eulerDict[0][2]
            )  # Currently the Yaw of the first body

        # print("POSITION",self.position)
        # print("EULERS",self.eulers)

    def get_global_pos(self):
        """Returns a tuple of robot's global (position, euler angle)"""
        self.loop.run_until_complete(self.__live_stream_pos())
        return self.position, self.eulers

    def get_all_bodies(self) -> Dict[str, RT6DBodyEuler]:
        self.loop.run_until_complete(self.__live_stream_pos())
        return { name: self.eulerDict[id] for id, name in self.bodyDictionary.items() }

    async def __live_stream_pos(self):
        """Creates a dictionary of (ID, body) for all bodies."""

        body_index = self.__create_body_index(self.xml_string)
        keyval_pairs = {
            body_index[bodyname]: bodyname for bodyname in body_index.keys()
        }

        self.bodyDictionary = keyval_pairs

        await self.connection.stream_frames(
            components=["6d", "6deuler"], on_packet=self.__on_packet
        )
        # await self.connection.stream_frames_stop()

    def __create_body_index(self, xml_string: str):
        """Extract a name to index dictionary from 6dof settings xml"""
        xml = ET.fromstring(xml_string)

        body_to_index = {}
        for index, body in enumerate(xml.findall("*/Body/Name")):
            if not body.text:
                continue
            body_to_index[body.text.strip()] = index

        return body_to_index


def main():
    tracker = QtmTracker("10.76.30.91")
    should_continue = "y"
    while should_continue != "n":
        print(tracker.get_global_pos())
        sleep(1)
        # should_continue = input("Go again - y or n: ")


if __name__ == "__main__":
    main()
