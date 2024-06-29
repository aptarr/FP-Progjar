import sys
import os
import json
import uuid
import logging
import socket
import threading
from queue import Queue

class Chat:
	def __init__(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# sessions:
		# 	sessionid: {uuid: users}
		self.sessions={}
		self.realm_auth = "secret1"
		self.realm_ip = "127.0.0.1"
		self.users = {}
		# 	users:
		# 		name
		# 		password
		# 		chat: [] (chats id)
		self.users['messi']={'password': 'secret', 'chats' : []}
		self.users['henderson']={'password': 'secret', 'chats': []}
		self.users['lineker']={'password': 'secret','chats': []}

		# 	chats:
		# 		id
		# 		type: cp/group
		# 		name: {cp: userto, group: group_name}
		# 		message: messages
		# 		member: [username]
		# 		updatedAt: last message timestamp

		# 	messages:
		# 		from
		# 		to
		# 		message
		# 		status: read/unread
		# 		timestamp
		self.chats = {}

		self.realms = {}
		# realms:
		# 	ip 
		# 	port
		# 	users
		#   auth
		self.realms["127.0.0.2"] = {
				"port": 8889,
				"users": [
					"hmd",
					"hfd"
				],
				"auth": "secret2"
			}
		self.realms["127.0.0.3"] = {
				"port": 8889,
				"users": [
					"apt",
					"hq",
					"rzn"
				],
				"auth": "secret3"
			}
		
  
	def proses(self,data):
		j=data.split(" ")
		try:
			command=j[0].strip()
			if (command == 'login'):
				username=j[1].strip()
				password=j[2].strip()
				logging.warning("AUTH: login {} {}" . format(username, password))
				return self.autentikasi_user(username, password)

			elif (command == 'register'):
				username=j[1].strip()
				password=j[2].strip()
				logging.warning("REGISTER: register {} {}" . format(username, password))
				return self.register(username, password)

			elif (command == 'logout'):
				tokenid=j[1].strip()
				return self.logout(tokenid)

			elif (command == 'addUserRealm'):
				auth=j[1].strip()
				ipRealm=j[2].strip()
				username=j[3].strip()
				logging.warning("SYNC: addUserRealm {} {} {}" . format(auth, ipRealm, username))
				result = self.add_user_realm(auth, ipRealm, username)
				return result
			
			else:
				return {'status': 'ERROR', 'message': '**Protocol Tidak Benar'}
		except KeyError:
			return { 'status': 'ERROR', 'message' : 'Informasi tidak ditemukan'}
		except IndexError:
			return {'status': 'ERROR', 'message': '--Protocol Tidak Benar'}

	def sendstring(self, string, targetIp, targetPort):
		server_address = (targetIp,targetPort)
		self.sock.connect(server_address)
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

	def check_user(self, username):
		if (username in self.users):
			return True
		for realm in self.realms:
			if username in realm['users']:
				return True
		return False

	def autentikasi_user(self, username, password):
		if (username not in self.users):
			return { 'status': 'ERROR', 'message': 'User Tidak Ada' }
		if (self.users[username]['password'] != password):
			return { 'status': 'ERROR', 'message': 'Password Salah' }
		tokenid = str(uuid.uuid4()) 
		self.sessions[tokenid] = { 'username': username, 'userdetail':self.users[username]}
		return { 'status': 'OK', 'tokenid': tokenid }

	def add_user_realm(self, auth, ipRealm, username):
		if self.realms[ipRealm]['auth'] != auth:
			return { 'status': 'ERROR', 'message': 'Autentikasi Realm Salah' }
		self.realms[ipRealm]['users'].append(username)
		return { 'status': 'OK', 'message': f'Berhasil menambahkan {username} kedalam {ipRealm} pada realm {self.realm_ip}' }

	def register(self,username,password):
		if (self.check_user(username)):
			return { 'status': 'ERROR', 'message': 'User Sudah Ada' }
		self.users[username] = {"password": password, "chats": []}
		tokenid = str(uuid.uuid4()) 
		self.sessions[tokenid] = { 'username': username, 'userdetail': self.users[username]}
		
		# sync new users across realms
		for ipRealm in self.realms:
			string="addUserRealm {} {} {} \r\n" . format(self.realm_auth, self.realm_ip, username)
			result = self.sendstring(string, ipRealm, self.realms[ipRealm]['port'])
			if result['status']=='OK':
				return "{}" . format(result['message'])
			else:
				return "Error, {}" . format(result['message'])
				
		return { 'status': 'OK', 'tokenid': tokenid }
		
	def logout(self, tokenid):
		if tokenid not in self.sessions:
			return {'status': 'ERROR', 'message': 'User Belum Login'}
		del self.sessions[tokenid]
		return {'status': 'OK', 'message': 'User Berhasil Logout'}
     
if __name__=="__main__":
	j = Chat()
	
	# testing register
	sesi = j.proses("register geprek secret ")
	print(j.users)

	sesi2 = j.proses("register geprek secret ")
	print(j.users)