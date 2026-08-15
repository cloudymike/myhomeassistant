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

DaSwitch = machine.Pin(3, machine.Pin.OUT)

#aDeviceString=binascii.hexlify(machine.unique_id()).decode('utf-8')
aDeviceString="001122AABBC1"
device = mha.HADevice(aDeviceString)  
#Create a random name at start
#device = mha.HADevice()  


sta=wlan.do_connect('skylight')

mqtt = mha.HAMqtt(device)

device.set_name("skylight")
device.set_software_version("0.1.0")
device.set_manufacturer("Espressif")
device.set_model("ESP32-C3")

switch = mha.HASwitch("skylight")

switch.set_current_state(True)
switch.set_name("Skylight")
switch.set_icon("mdi:lightbulb")

def on_switch_command(sender: mha.HASwitch, state: bool):
    print("Switch state:", state)
    sender.set_state(state)
    # ON is OFF for ESP32C3 LED. Go figure
    if state:
        LED.LED.value(0)
        DaSwitch.on()
    else:
        LED.LED.value(1)
        DaSwitch.off()
        
switch.on_command(on_switch_command)

mqtt.begin(mqtthost.MQTT_HOST,mqtthost.MQTT_PORT)

last_time = time.time()

while True:
    mqtt.loop()
#    print("running")
