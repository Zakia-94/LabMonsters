from flask import Flask,request,render_template
from wifi import Cell, Scheme
import os
import urllib.request
from time import sleep
import requests

share_hotspot = os.system('nmcli dev wifi hotspot ifname wlan0 ssid LABMONSTERS password "123456789" ')

app = Flask(__name__)
@app.route('/', methods=['GET','POST'])

def wifi_config():
    
    scanned_networks1 = str(list(Cell.all('wlan0'))).replace('Cell(ssid=','')
    
    scanned_networks2 = scanned_networks1.replace(')','')
    
    final_scanned_networks = scanned_networks2.strip('][').split(',')
    
    if request.method == 'GET' :
        
        for i in range(len(final_scanned_networks)):
            
            return render_template('web_interface.html', final_scanned_networks = final_scanned_networks, msg_to_display = 'Please select Wifi to connect to!')
    else:
        
        userDetails = request.form
        
        password = userDetails['psw']
        
        SSID = (request.form.get('WIFILIST'))
        
        connected = os.system('nmcli dev wifi connect  '+SSID+' password '+password)
        
        sleep(3)
        
        if connected == 0 :            
            connection_state = 'Connected'
            print(connection_state)
        else:
            connection_state='Couldn\'t connect.Try again!'
            print(connection_state)
            
        return render_template('web_interface.html', final_scanned_networks = final_scanned_networks, msg_to_display = connection_state)
    
        
if __name__ == '__main__':
    app.run(debug=True,host='10.42.0.1',port=5069)