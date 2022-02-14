import re
import subprocess
import bluetooth_configuration

class UsbConnection:

    def __init__(self):

        self.devices = []
        self.tag_list = []

        
    def device_information(self):
    
        device = re.compile(b"Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$", re.I)

        devices_information = subprocess.check_output("lsusb")

        self.devices = []

        for device_info in devices_information.split(b'\n'):
                    
            if device_info:
                        
                info = device.match(device_info)
                        
                if info:
                            
                    dinfo = info.groupdict()
                            
                    dinfo['device'] = '/dev/bus/usb/%s/%s' % (dinfo.pop('bus'), dinfo.pop('device'))
                            
                    self.devices.append(dinfo)

    def list_of_tags_devices(self):

        for i in range(len(self.devices)):
            
           self.tag_list.append(str(self.devices[i]['tag']))


    def delete_changeable_part_in_tags(self):
    
        for i in range(len(self.tag_list)):
            
            if self.tag_list[i][0:4] == "b'So":

                self.tag_list[i] = self.tag_list[i].replace(self.tag_list[i][25:]," ")

    def check_gamepad_connection(self):
    
        if "b'Sony Corp. DualShock 4  " in  self.tag_list :

            print("GamePad is connected by USB connection")

        else :
            
            print("GamePad is not connected to the USB Port")

            BluetoothConnection1 = bluetooth_configuration.BluetoothConnection()
            BluetoothConnection1.searching_nearby_devices()
            BluetoothConnection1.no_device_detected()
            BluetoothConnection1.device_list()
            BluetoothConnection1.gamepad_not_detected()
            BluetoothConnection1.gamepad_connection()
          

UsbConnection1 = UsbConnection()

UsbConnection1.device_information()

UsbConnection1.list_of_tags_devices()

UsbConnection1.delete_changeable_part_in_tags()

UsbConnection1.check_gamepad_connection()
    

