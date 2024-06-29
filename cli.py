import socket
import json

TARGET_IP = "127.0.0.1"
TARGET_PORT = 8889

class ChatClient:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (TARGET_IP,TARGET_PORT)
        self.sock.connect(self.server_address)
        self.tokenid=""

    def proses(self,cmdline):
        j=cmdline.split(" ")
        try:
            command=j[0].strip()
            if (command=='login'):
                username=j[1].strip()
                password=j[2].strip()
                return self.login(username,password)
            elif (command=='register'):
                username=j[1].strip()
                password=j[2].strip()
                return self.register(username,password)
            elif (command=='logout'):
                return self.logout()
            elif (command=='getusername'):
                return self.getusername()
            elif (command=='inboxall'):
                return self.inboxall()
            elif (command=='inbox'):
                chatid=j[1].strip()
                return self.inbox(chatid)
            else:
                return "*Maaf, command tidak benar"
        except IndexError:
                return "-Maaf, command tidak benar"

    def sendstring(self,string):
        try:
            self.sock.sendall(string.encode())
            receivemsg = ""
            while True:
                data = self.sock.recv(1024)
                print("diterima dari server",data)
                if (data):
                    receivemsg = "{}{}" . format(receivemsg,data.decode())  #data harus didecode agar dapat di operasikan dalam bentuk string
                    if receivemsg[-4:]=='\r\n\r\n':
                        print("end of string")
                        return json.loads(receivemsg)
        except:
            self.sock.close()
            return { 'status' : 'ERROR', 'message' : 'Gagal'}

    def login(self,username,password):
        string="login {} {} \r\n" . format(username,password)
        result = self.sendstring(string)
        if result['status']=='OK':
            self.tokenid=result['tokenid']
            return "username {} logged in, token {} " .format(username,self.tokenid)
        else:
            return "Error, {}" . format(result['message'])
        
    def register(self,username,password):
        string="register {} {} \r\n" .format(username,password)
        result = self.sendstring(string)
        if result['status']=='OK':
            self.tokenid=result['tokenid']
            return "username {} registered, token {} " .format(username, self.tokenid)
        else:
            return "Error, {}" . format(result['message'])
        
    def logout(self):
        if (self.tokenid==""):
            return "Error, not authorized"
        string="logout {} \r\n" .format(self.tokenid)
        result = self.sendstring(string)
        if result["status"] == "OK":
            return "user logged out"
        else:
            return "Error, {}".format(result["message"])
        
    def getusername(self):
        if (self.tokenid==""):
            return "Error, not authorized"
        string="getusername {} \r\n" .format(self.tokenid)
        result = self.sendstring(string)
        if result["status"] == "OK":
            return "{}" . format(json.dumps(result['data']))
        else:
            return "Error, {}".format(result["message"])
        
    def inboxall(self):
        if (self.tokenid==""):
            return "Error, not authorized"
        string="inboxall {} \r\n" .format(self.tokenid)
        result = self.sendstring(string)
        if result["status"] == "OK":
            return "{}" . format(json.dumps(result['data']))
        else:
            return "Error, {}".format(result["message"])
        
    def inbox(self, chatid):
        if (self.tokenid==""):
            return "Error, not authorized"
        string="inbox {} {} \r\n" .format(self.tokenid, chatid)
        result = self.sendstring(string)
        if result["status"] == "OK":
            return "{}" . format(json.dumps(result['data']))
        else:
            return "Error, {}".format(result["message"])

cc = ChatClient()