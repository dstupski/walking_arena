#!/usr/bin/env python

# Command line arguments
from optparse import OptionParser

# ROS imports
import roslib, rospy
import numpy as np
#import rosbag2py
import time
import random

import std_msgs.msg
import yaml
#from std_msgs.msg import Float32, Float32MultiArray, Float64MultiArray
#from multi_tracker.msg import Contourinfo, Contourlist
#from multi_tracker.msg import Trackedobject, Trackedobjectlist
import serial

class WalkingArena:
    def __init__(self, config_file):
        with open(config_file) as file:
            self.config = yaml.load(file)
        # Read in standard information from the configuration file
        #arduino parameters
        self.port= self.config['port']
        self.baudrate = self.config['baudrate']
        self.arduino = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=.1)

        #trigger paramaters such as the array of possible triggering events
        self.trigger_array = self.config['trigger_array']
        self.interval = self.config['interval']
        self.publisher_id = self.config['publisher']


        #node set up information
        rospy.init_node('WalkingNode', anonymous=True)
        self.publisher = rospy.Publisher(self.publisher_id, std_msgs.msg.Float64MultiArray, queue_size=10)
        self.msg = std_msgs.msg.Float64MultiArray()
        #Time since either initiation the node, or last trigger event.
        self.tcall = rospy.Time.now()
    def trigger(self):
        if int(rospy.Time.now().secs) - int(self.tcall.secs)>=self.interval:
            trigger_event = random.choice(self.trigger_array)

            arduino_byte = trigger_event[0]
            message_byte = trigger_event[1]

            self.arduino.write(arduino_byte)


            self.msg.data = [rospy.Time.now().to_sec(), message_byte]
            self.publisher.publish(self.msg)
            self.tcall = rospy.Time.now()

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("--config", type="str", dest="config", default='',
                      help="Full path that points to a config.yaml file. See ../configs/volume_trigger_config.yaml for an example")
    (options, args) = parser.parse_args()
    node = WalkingArena(config_file = options.config)
    try:
        while not rospy.is_shutdown():
            node.trigger()
        #rospy.Timer(rospy.Duration(5), node.trigger_test())# node.run()
    except rospy.ROSInterruptException:
        pass