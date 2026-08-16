# SPDX-FileCopyrightText: Copyright (c) 2024 lbuque
#
# SPDX-License-Identifier: MIT

import sys
#sys.path.append('..')


import mha
import time
import wlan
import mqtthost

# import machine
# import binascii


device = mha.HADevice("001122AABBC0")  # (binascii.hexlify(machine.unique_id()).decode('utf-8'))

sta=wlan.do_connect('voltmeter')
mqtt = mha.HAMqtt(device)

device.set_name("voltmeter")
device.set_software_version("0.1.0")

sensor = mha.HABinarySensor("voltmeter_sensor")

sensor.set_current_state(True)
sensor.set_name("Voltmeter")
sensor.set_device_class("power")
sensor.set_icon("mdi:gauge")

mqtt.begin(mqtthost.MQTT_HOST,mqtthost.MQTT_PORT)

last_time = time.time()

while True:
    mqtt.loop()

    if time.time() - last_time > 5:
        sensor.set_state(not sensor.get_current_state())
        last_time = time.time()

