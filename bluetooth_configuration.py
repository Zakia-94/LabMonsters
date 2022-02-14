import socket
import bluetooth


class BluetoothConnection:

    def __init__(self):

        self.list_of_nearby_devices = []

    def searching_nearby_devices(self):

        print("Searching For Devices ...")

        self.nearby_devices = bluetooth.discover_devices(lookup_names = True)


    def no_device_detected(self):

        if len(self.nearby_devices) == 0 :

            print("No device has been detected,keep searching ...")
        
            self.searching_nearby_devices()
            self.no_device_detected()
            self.device_list()
            self.gamepad_not_detected()
            self.gamepad_connection()

    def device_list(self):

        if len(self.nearby_devices) > 0 :

            for device in self.nearby_devices:
            
                self.list_of_nearby_devices.append(device[1])

    def gamepad_not_detected(self):

        if "Wireless Controller" not in self.list_of_nearby_devices:
                                             
            self.searching_nearby_devices()
            self.no_device_detected()
            self.device_list()
            self.gamepad_not_detected()
            self.gamepad_connection()

    def gamepad_connection(self):

        if "Wireless Controller" in self.list_of_nearby_devices:
    
            for device in self.nearby_devices:

                if device[1] == 'Wireless Controller' :
                    
                    MacAdress = device[0]
                            
                    try:
                    
                        serverMACAddress = MacAdress

                        port = 10

                        s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)

                        s.connect((serverMACAddress,port))

                    except ConnectionRefusedError:

                        print("Connection successfully")
                                
                        break          
    

  
                

    
            
        
        
        
    
        
