# SPDX-FileCopyrightText: Copyright (c) 2024 lbuque
#
# SPDX-License-Identifier: MIT

import sys
#sys.path.append('..')


import mha
import time
import wlan
import mqtthost
import LED

# import machine
# import binascii


device = mha.HADevice("001122AABBC1")  # (binascii.hexlify(machine.unique_id()).decode('utf-8'))

sta=wlan.do_connect('voltmeter')
mqtt = mha.HAMqtt(device)

device.set_name("voltmeter")
device.set_software_version("0.1.0")
device.set_manufacturer("Espressif")
device.set_model("ESP32-C3")

sensor = mha.HAIntegerSensor("voltmeter_sensor")

sensor.set_current_state(0)
sensor.set_name("Voltmeter")
sensor.set_device_class("power")
sensor.set_icon("mdi:gauge")

mqtt.begin(mqtthost.MQTT_HOST,mqtthost.MQTT_PORT)

last_time = time.time()

while True:
    mqtt.loop()

    if time.time() - last_time > 5:
        cv=sensor.get_current_state()+1
        sensor.set_state(cv)
        print(cv)
        LED.LED.value(cv%2)
        last_time = time.time()

