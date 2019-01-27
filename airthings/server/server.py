from bluepy.btle import UUID, Peripheral
from datetime import datetime
from wsgiref.simple_server import make_server
import sys
import time
import struct
import re


class Sensor:
    def __init__(self, name, uuid, format_type, unit, scale):
        self.name = name
        self.uuid = uuid
        self.format_type = format_type
        self.unit = unit
        self.scale = scale

def get_data():
    str_out = ""        
    try:
        sensors = []
        sensors.append(Sensor("DateTime", UUID(0x2A08), 'HBBBBB', "\t", 0))
        sensors.append(Sensor("Temperature", UUID(0x2A6E), 'h', "deg C\t", 1.0/100.0))
        sensors.append(Sensor("Humidity", UUID(0x2A6F), 'H', "%\t\t", 1.0/100.0))
        sensors.append(Sensor("Radon 24h avg", "b42e01aa-ade7-11e4-89d3-123b93f75cba", 'H', "Bq/m3\t", 1.0))
        sensors.append(Sensor("Radon long term", "b42e0a4c-ade7-11e4-89d3-123b93f75cba", 'H', "Bq/m3\t", 1.0))

        addr =  "98:07:2d:05:bf:2f"
        p = Peripheral(addr)


        for s in sensors:
            ch  = p.getCharacteristics(uuid=s.uuid)[0]
            if (ch.supportsRead()):
                val = ch.read()
                val = struct.unpack(s.format_type, val)
                if s.name == "DateTime":
                    str_out += str(datetime(val[0], val[1], val[2], val[3], val[4], val[5])) + ","
                else:
                    str_out += str(val[0] * s.scale) + ","
                    
        str_out += addr
    finally:
        p.disconnect()

    return str_out 


def application(environ, start_response):
    start_response('200 OK', [('Content-type', 'text/plain')])
    retval =  get_data()
    return retval

make_server('', 8888, application).serve_forever()
