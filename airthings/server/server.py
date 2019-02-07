from bluepy.btle import UUID, Peripheral, Scanner, DefaultDelegate
from datetime import datetime
from wsgiref.simple_server import make_server
import sys
import time
import struct
import re
import json

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
        data = {}
        sensors.append(Sensor("DateTime", UUID(0x2A08), 'HBBBBB', "\t", 0))
        sensors.append(Sensor("Temperature", UUID(0x2A6E), 'h', "deg C\t", 1.0/100.0))
        sensors.append(Sensor("Humidity", UUID(0x2A6F), 'H', "%\t\t", 1.0/100.0))
        sensors.append(Sensor("Radon 24h avg", "b42e01aa-ade7-11e4-89d3-123b93f75cba", 'H', "Bq/m3\t", 1.0))
        sensors.append(Sensor("Radon long term", "b42e0a4c-ade7-11e4-89d3-123b93f75cba", 'H', "Bq/m3\t", 1.0))

        for key in devs.keys():
            data[key] = {}
            addr = str(devs[key])
            print addr
            p = Peripheral(addr)


            for s in sensors:
                ch  = p.getCharacteristics(uuid=s.uuid)[0]
                if (ch.supportsRead()):
                    val = ch.read()
                    val = struct.unpack(s.format_type, val)

                    if s.name == "DateTime":
                        str_out += str(datetime(val[0], val[1], val[2], val[3], val[4], val[5])) + ","
                        data[key][s.name] = str(datetime(val[0], val[1], val[2], val[3], val[4], val[5]))
                    else:
                        str_out += str(val[0] * s.scale) + ","
                        data[key][s.name] = str(val[0] * s.scale)
                        
            str_out += addr
            data[key]['MAC'] = addr
            str_out += ","
            if 'p' in locals():
                p.disconnect()
        str_out += "END"        
    except Exception as e:
	print("Could not request Wave value. %s" %  e)
        str_out = ""
		
    finally:
        if 'p' in locals():
            p.disconnect()

    #print(data)
    json_data = json.dumps(data)

    print(json_data)
    return json_data; 
    #return str_out 

def parseSerialNumber(ManuDataHexStr):
    if (ManuDataHexStr == "None"):
        SN = "Unknown"
    else:
        ManuData = bytearray.fromhex(ManuDataHexStr)

        if (((ManuData[1] << 8) | ManuData[0]) == 0x0334):
            SN  =  ManuData[2]
            SN |= (ManuData[3] << 8)
            SN |= (ManuData[4] << 16)
            SN |= (ManuData[5] << 24)
        else:
            SN = "Unknown"
    return SN


def application(environ, start_response):
    start_response('200 OK', [('Content-type', 'text/plain')])
    retval =  get_data()
    print(retval)
    return retval

def findDevs():
    devs = {}
    scanner     = Scanner().withDelegate(DefaultDelegate())
    searchCount = 0
    while searchCount < 20:
        devices      = scanner.scan(0.2) # 0.1 seconds scan period
        searchCount += 1
        for dev in devices:
            ManuData = dev.getValueText(255)
            SN = parseSerialNumber(ManuData)
            if (SN != "Unknown"):
                    devs[SN] = dev.addr        
    return devs

devs = findDevs()

for key in devs.keys():
    print key, devs[key]

make_server('', 8888, application).serve_forever()
