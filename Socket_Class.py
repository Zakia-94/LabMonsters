#import modules
import sqlite3
import socketio
import gameController_file

def sql_connection():
    conn = sqlite3.connect('labMons.db')
    return conn
    
def select_all_data(conn):
    cursor_obj = conn.cursor()
    cursor_obj.execute("SELECT * FROM DataGame")
    rows = cursor_obj.fetchall()
    for row in rows:
        #Convert the first element of the row  in the database from tuple type to string
        data_0 = ''.join(row[0])
        #Convert the second element of the row  in the database from float type to string
        timestamp_1 = str(row[1])
        #Concatenate data_0 and timestam_1
        data_t = data_0+" "+timestamp_1
        print(data_t)
        gameController_file.GameController().ser.write(("P: "+data_t+"\n").encode())
        gameController_file.sio.emit('action-data',data_t)
    #After sending the database we will delete the table created
    cursor_obj.execute("DELETE FROM DataGame")
    print("We have deleted",cursor_obj.rowcount,'rows from the table.')

def checking_game_state():
    #Check the value pushed in the list
    if len(gameController_file.GameController.Game_Status) >= 1:
        if gameController_file.GameController.Game_Status[-1] == 1:
            print("play")
            gameController_file.GameController().all_data()
            gameController_file.GameController.is_done = False
        elif gameController_file.GameController.Game_Status[-1] == 2:
            print("Pause")
            gameController_file.GameController.is_done = True
        elif gameController_file.GameController.Game_Status[-1] == 3:
            print("Stop")
            gameController_file.GameController.is_done = True
        gameController_file.GameController.Game_Status.clear()
    print("list is empty") 
                
gameController_file.sio = socketio.Client()
class Socket(gameController_file.GameController):
    
    @staticmethod   
    @gameController_file.sio.on("connect")
    def on_connect():
        gameController_file.GameController.isConnected = True
        print("connected")
        gameController_file.sio.emit('send-key-user','BIOZVTY9M0G')
        conn = sql_connection()
        cursor_obj = conn.cursor()
        cursor_obj.execute(''' SELECT count(name) FROM sqlite_master WHERE TYPE='table' AND name='DataGame' ''')
        if cursor_obj.fetchone()[0] == 1:
            print('table exists.')
            conn = sql_connection()
            select_all_data(conn)     
        else:
            print('table does not exist') 
        conn.commit()
        conn.close()
    checking_game_state()

    gameController_file.sio.connect("https://socketio-server-wn4bpuoada-uc.a.run.app")

    @staticmethod     
    @gameController_file.sio.on("disconnect")
    def on_disconnect():
        gameController_file.GameController.isConnected = False
        print("Disconnected from the server")

    @staticmethod   
    @gameController_file.sio.on("check-play-game-q")  
    def on_check_game(data):
        gameController_file.GameController.Game_Status.append(1)
        print('play')
        #emit an event to the server
        gameController_file.sio.emit('check-paly-reponse',1)
        gameController_file.GameController().all_data()
        gameController_file.GameController.is_done = False

    @staticmethod  
    @gameController_file.sio.on("check-pause-game-q")
    def on_check_pause_device(data):
        gameController_file.GameController.Game_Status.append(2)
        print('pause')
        #emit an event to the server
        gameController_file.sio.emit('check-pause-reponse',1)
        gameController_file.GameController.is_done = True

    @staticmethod  
    @gameController_file.sio.on("check-stop-game-q")
    def on_stop_game(data):
        gameController_file.GameController.Game_Status.append(3)
        print('stop')
        gameController_file.sio.emit('check-stop-reponse',1)
        gameController_file.GameController.is_done = True
    
    @staticmethod
    @gameController_file.sio.on("check-replay-game-q")
    def on_check_replay(data):
        print(data+"\n")
        gameController_file.GameController().ser.write(("R: "+data+"\n").encode())
                                              
    while 1:
        pass  
   