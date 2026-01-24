# SPDX-FileCopyrightText: Copyright (c) 2025 lbuque
#
# SPDX-License-Identifier: MIT


import time
import mqtthost
import wlan
import LED

import mha

import machine
import binascii

#aDeviceString=binascii.hexlify(machine.unique_id()).decode('utf-8')
aDeviceString="001122AABBC1"
device = mha.HADevice(aDeviceString)  
#Create a random name at start
#device = mha.HADevice()  


sta=wlan.do_connect('mhaswitch')

mqtt = mha.HAMqtt(device)

device.set_name("MHA Test")
device.set_software_version("0.1.0")
device.set_manufacturer("Espressif")
device.set_model("ESP32-C3")

switch = mha.HASwitch("blue_led")

switch.set_current_state(True)
switch.set_name("Blue LED")
switch.set_icon("mdi:lightbulb")

def on_switch_command(sender: mha.HASwitch, state: bool):
    print("Switch state:", state)
    sender.set_state(state)
    # ON is OFF for ESP32C3 LED. Go figure
    if state:
        LED.LED.value(0)
    else:
        LED.LED.value(1)
        
    # to some action here

switch.on_command(on_switch_command)

mqtt.begin(mqtthost.MQTT_HOST)

last_time = time.time()

while True:
    mqtt.loop()
#    if time.time() - last_time > 5:
#        switch.set_state(not switch.get_current_state())
#        last_time = time.time()
