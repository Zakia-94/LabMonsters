#import modules
from datetime import datetime
import sqlite3
import json
import serial
import pygame
import socketio

sio = socketio.Client()
class GameController:
    
    """ Game Controller Class"""
    
    is_done,isConnected,Game_Status = False,False,[]

    def __init__(self):
        pygame.init(),pygame.joystick.init()
        self.controller,self.ser = pygame.joystick.Joystick(0),serial.Serial('/dev/ttyS0',115200)
        self.controller.init()
        self.axe,self.boutton,self.hat = "", "", ""
        self.Axe = [0,0,0,0,0,0]
        self.old_data = self.axe+self.boutton+self.hat
        self.L2_axes, self.R2_axes, self.send_pause = False, False, False
        
    def axes(self):
        if self.controller.get_axis(2) != 0: self.L2_axes = True 
        if self.controller.get_axis(5) != 0: self.R2_axes = True
        for i,num in enumerate([0,1,2,3,4,5]):
            #Fix the axe value to 4 decimals
            if self.controller.get_axis(i) >= 0 :
                #Fix the axe value to 4 decimals
                val = '{0:.4f}'.format(self.controller.get_axis(i))
                self.Axe[i] = "".join(["+",str(val)])
            else: self.Axe[i] = '{0:.4f}'.format(self.controller.get_axis(i)) 
        #Concattenate the axes
        axe = self.Axe[0],self.Axe[1],self.Axe[3],self.Axe[4],self.Axe[2],self.Axe[5]
        self.axe = "".join(axe)
        return f"{self.axe}"
    
    def buttons(self):
        #Differentiate between the axes & buttons values by a pipe symbol
        self.boutton = "|"
        for i,num in enumerate([0,1,2,3,4,5,6,7,8,9,10,11,12]):
            self.boutton += str(self.controller.get_button(i))
        return f"{self.boutton}"
        
    def hats(self):
        #H presents the hats/D-PAD Buttons
        self.hat = ""
        #convert tuple to a list
        self.list_hats = list(self.controller.get_hat(0))
        
        if self.list_hats[1] >= 0 <= self.list_hats[0]:
            self.string_concatenate = "".join(["+",str(self.list_hats[0]),"+",str(self.list_hats[1])])
            
        elif  self.list_hats[1] >= 0 > self.list_hats[0]: 
            self.string_concatenate = "".join([str(self.list_hats[0]),"+",str(self.list_hats[1])])
            
        elif self.list_hats[0] >= 0 > self.list_hats[1]:
            self.string_concatenate = "".join(["+"+str(self.list_hats[0])+str(self.list_hats[1])])
        self.hat = "".join(self.string_concatenate)
        return f"{self.hat}"


    def all_data(self):
        while not self.is_done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: self.is_done = True
                
            self.data = self.axes()+self.buttons()+self.hats()
            
            state_0 = "+0.0000+0.0000+0.0000+0.0000+0.0000+0.0000|0000000000000+0+0"
            state_1 = "+0.0000+0.0000+0.0000+0.0000+0.0000-1.0000|0000000000000+0+0"
            state_2 = "+0.0000+0.0000+0.0000+0.0000-1.0000+0.0000|0000000000000+0+0"
            state_3 = "+0.0000+0.0000+0.0000+0.0000-1.0000-1.0000|0000000000000+0+0"
            
            #Conditions for R2 and L2
            if((self.data != state_0 and self.L2_axes is False and self.R2_axes is False)
            or (self.data != state_1 and self.L2_axes is False and self.R2_axes is True)
            or (self.data != state_2 and self.L2_axes is True and self.R2_axes is False)
            or (self.data != state_3  and self.L2_axes is True and self.R2_axes is True)):
                self.send_data() if GameController.isConnected is True else self.storage_data()
            
            elif (self.data == state_0) or (self.data == state_1) or (self.data == state_2) or (self.data == state_3):
                self.send_pause = True 
                      
            if self.send_pause is True :
                self.send_pause = False

                if self.data != self.old_data :
                    self.send_data() if GameController.isConnected is True else self.storage_data()  
                                          
            self.old_data = self.data
            
    def send_data(self):
        #Send data to arduino
        self.ser.write(("P: "+self.data+"\n").encode())
        current_time = datetime.now()
        #print data to the console in python
        print(self.data+" "+'{:.6f}'.format(current_time.timestamp()))
        #emit data to socket
        sio.emit('action-data',self.data+" " +'{:.6f}'.format(current_time.timestamp()))
        
    def storage_data(self):
        current_time = datetime.now()
        #print data to the console in python
        print(self.data+" "+'{:.6f}'.format(current_time.timestamp()))
        #Connection to the dataBase
        conn = sqlite3.connect('labMons.db')
        cursor_obj = conn.cursor()
        create_table = lambda : cursor_obj.execute("create table if not exists DataGame(data json,date json)")

        def data_entry():
            with open('labMons.db','a') :
                cursor_obj.execute("insert into DataGame(data,date) values("+json.dumps(self.data)+","+json.dumps('{:.6f}'.format(current_time.timestamp()))+")")
                conn.commit()
        create_table()
        data_entry()
        