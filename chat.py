import sys
import os
import json
import uuid
import logging
import socket
import threading
from queue import Queue
from datetime import datetime

class Chat:
	def __init__(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.realm_auth = "secret1"
		self.realm_ip = "172.16.16.101"

		# sessions:
		# 	sessionid
		# 	username
		# 	userdetail
		self.sessions={}

		self.users = {}
		# 	users:
		# 		name
		# 		password
		# 		chat: [] (chats id)
		self.users['messi']={'password': 'secret', 'chats' : ['1', '2']}
		self.users['henderson']={'password': 'secret', 'chats': ['1', '2']}
		self.users['lineker']={'password': 'secret', 'chats': ['2']}
		# self.users['hmd']={'password': 'secret', 'chats' : []}
		# self.users['hfd']={'password': 'secret', 'chats': []}

		# 	chats:
		# 		id
		# 		type: cp/group
		# 		name: {cp: userto, group: group_name}
		# 		message: messages
		# 		member: [username]
		# 		updatedAt: last message timestamp

		# 	messages:
		# 		sender
		# 		message
		# 		timestamp
		self.chats = {}
		self.chats['1'] = {
			'type': 'private',
			'name': 'messi',
			'message': [
				{
					'sender': 'messi',
					'message': 'Hello',
					'timestamp': '2021-10-10 10:10:10'
				},
				{
					'sender': 'henderson',
					'message': 'Hi',
					'timestamp': '2021-10-10 10:10:10'
				}
			],
			'member': ['messi', 'henderson'],
			'updatedAt': '2021-10-10 10:10:10'
		}

		self.chats['2'] = {
			'type': 'group',
			'name': 'group1',
			'message': [
				{
					'sender': 'messi',
					'message': 'Hello',
					'timestamp': '2021-10-10 10:10:10'
				},
				{
					'sender': 'henderson',
					'message': 'Hi',
					'timestamp': '2021-10-10 10:10:10'
				},
				{
					'sender': 'lineker',
					'message': 'Hi',
					'timestamp': '2021-10-10 10:10:10'
				}
			],
			'member': ['messi', 'henderson', 'lineker', 'hmd'],
			'updatedAt': '2021-10-10 10:10:10'
		}

		self.realms = {}
		# realms:
		# 	ip 
		# 	port
		# 	users
		#   auth
		# self.realms["172.16.16.101"] = {
		# 		"port": 8889,
		# 		"users": [
		# 			"messi",
		# 			"henderson",
        #             "lineker"
		# 		],
		# 		"auth": "secret1"
		# 	}
		self.realms["172.16.16.102"] = {
				"port": 8889,
				"users": [
					"hmd",
					"hfd"
				],
				"auth": "secret2"
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
				return self.add_user_realm(auth, ipRealm, username)
			
			elif (command == 'getusername'):
				tokenid=j[1].strip()
				logging.warning("GETUSERNAME: {}" . format(tokenid))
				return self.get_username(tokenid)
			
			elif (command == 'sendmsg'):
				tokenid=j[1].strip()
				chat_id=j[2].strip()
				message = " ".join(j[3:])
				message = message[:-4]
				logging.warning("SENDMSG: {}" . format(tokenid, chat_id, message))
				return self.send_message(tokenid, chat_id, message)
			
			elif (command == 'syncmsg'):
				auth=j[1].strip()
				ipRealm=j[2].strip()
				chat_id=j[3].strip()
				sender=j[4].strip()
				timestamp=j[5].strip()
				message = " ".join(j[6:])
				message = message[:-4]
				logging.warning("SYNC: syncmsg {} {} {} {} {} {}" . format(auth, ipRealm, chat_id, sender, timestamp, message))
				result = self.sync_message(auth, ipRealm, chat_id, sender, message, timestamp)
				print(self.chats[chat_id])
				return result
			
			elif(command == 'addRealmChat'):
				chat_id = j[1].strip()
				username = j[2].strip()
				logging.warning("SYNC: addRealmChat {} {} {}" . format(chat_id, chat_dict, username))
				result = self.add_realm_chats(chat_id, username)
				return result
			
			elif(command == 'changeSelfChat'):
				chat_id = j[1].strip()
				chat_dict = ' '.join(j[2:]).strip()
				logging.warning("SYNC: changeSelfChat {} {}" . format(chat_id, chat_dict))

			elif (command == 'createGroup'):#type, group_name, members banyak
				tokenid = j[1].strip()
				type= j[2].strip()
				group_name = j[3].strip()
				password = j[4].strip()
				logging.warning("CREATE_GROUP: createGroup {} {} {}" . format(type, group_name, password))
				result = self.create_chat(tokenid, type, group_name, password = password)
				return result
			
			elif(command == 'createChat'): #type, member
				tokenid = j[1].strip()
				type = j[2].strip()
				group_name = j[3].strip()
				member = j[3].strip()
				logging.warning("CREATE_CHAT: createGroup {} {} {}" . format(type, group_name, member))
				result = self.create_chat(type, group_name, member = member)
				return result
			
			elif (command == 'inboxall'):
				tokenid=j[1].strip()
				logging.warning("INBOXALL: {}" . format(tokenid))
				return self.get_all_inbox(tokenid)
			
			elif (command == 'inbox'):
				tokenid=j[1].strip()
				chat_id=j[2].strip()
				logging.warning("INBOX: {} {}" . format(tokenid, chat_id))
				return self.get_inbox(tokenid, chat_id)
			
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
			if username in self.realms[realm]['users']:
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
			return { 'status': 'ERROR', 'message': 'Autentikasi Realm Gagal' }
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
	
	def get_username(self, tokenid):
		if tokenid not in self.sessions:
			return {'status': 'ERROR', 'message': 'User Belum Login'}
		return {'status': 'OK', 'data': self.sessions[tokenid]['username']}
	
	def add_realm_chats(self, chat_id, username): # memasukkan chat_id kedalam parameter user
		self.users[username]['chats'].append(chat_id)
		# self.chats[chat_id]= chat_dict
		return { 'status': 'OK', 'message': f'Berhasil menambahkan chat {chat_id} kedalam {self.realm_ip} pada user {username}' }
	
	def change_self_chat(self, chat_id, chat_dict):
		self.chats[chat_id] = chat_dict
		return { 'status': 'OK', 'message': f'Berhasil mengubah chat chats dengan chat_id {chat_id} kedalam {self.realm_ip}' }

	def create_chat(self,tokenid, type, group_name, member = None, password = None):
		if tokenid not in self.sessions:
			return {'status': 'ERROR', 'message': 'User Belum Login'}
		members = []
		user = self.sessions[tokenid]
		username = user['username']
		members.append(username)
		if member is not None:
			if self.check_user(member) == False:
				return {'status': 'ERROR', 'message': 'User Tidak Ditemukan'}
			members.append(member)
		now = datetime.now()
		current_time = now.strftime("%Y-%m-%d %H:%M:%S")
		chat_id = str(uuid.uuid4())
		chat_dict = {
			'type': type,
			'name': group_name,
			'password': password,
			'message': {},
			'members': members,
			'UpdatedAt': current_time
		}
		self.chats[chat_id] = chat_dict
		user['userdetail']['chats'].append(chat_id)
		# melakukan broadcast chat group ke semua user
		if type == 'group':
			for ip,val in self.realms.items():
				string="changeSelfChat {} {} \r\n" . format(chat_id, chat_dict)
				self.sendstring(string, ip, self.realms[ip]['port'])
		# untuk member akan disambungkan ke realm yang bersangkutan
		if member is not None: # jika ada member
			if  member not in self.users.keys(): # jika member tidak dari realm ini
				for ip,val in self.realms.items(): # mencari di realm lain
					if member in val['users']:
						string="addUserChat {} {} {} \r\n" . format(chat_id, member, chat_dict)
						result = self.sendstring(string, ip, self.realms[ip]['port'])
						if result['status']=='OK':
							return "{}" . format(result['message'])
						else:
							return "Error, {}" . format(result['message'])
						break
			else:
				self.users[member]['chats'].append(chat_id)
		return { 'status': 'OK', 'message': f'Berhasil membuat chat' }

	def sync_message(self, auth, ipRealm, chat_id, sender, message, timestamp):
		if self.realms[ipRealm]['auth'] != auth:
			return { 'status': 'ERROR', 'message': 'Autentikasi Realm Gagal' }
		
		if chat_id not in self.chats:
			return {'status': 'ERROR', 'message': 'Chat tidak ditemukan'}

		self.chats[chat_id]['message'].append({
			'sender': sender,
			'message': message,
			'timestamp': timestamp
		})

		self.chats[chat_id]['updatedAt'] = timestamp

		return {'status': 'OK', 'message': 'Pesan berhasil disinkronisasi'}

	def send_message(self, tokenid, chat_id, message):
		if tokenid not in self.sessions:
			return {'status': 'ERROR', 'message': 'User Belum Login'}
		users = self.sessions[tokenid]['userdetail']

		if chat_id not in users['chats']:
			return {'status': 'ERROR', 'message': 'Chat tidak ditemukan'}
		
		timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		sender = self.sessions[tokenid]['username']

		self.chats[chat_id]['message'].append({
			'sender': sender,
			'message': message,
			'timestamp': timestamp
		})

		self.chats[chat_id]['updatedAt'] = timestamp

		# sync new message across realms
		for ipRealm in self.realms:
			for member in self.chats[chat_id]['member']:
				if member in self.realms[ipRealm]['users']:
					string="syncmsg {} {} {} {} {} {} \r\n" . format(self.realm_auth, self.realm_ip, chat_id, sender, timestamp, message)
					result = self.sendstring(string, ipRealm, self.realms[ipRealm]['port'])
					if result['status']=='OK':
						break
					else:
						return "Error, {}" . format(result['message'])

		return {'status': 'OK', 'message': 'Pesan berhasil dikirim'}

	def get_all_inbox(self, tokenid):
		if tokenid not in self.sessions:
			return {'status': 'ERROR', 'message': 'User Belum Login'}
		users = self.sessions[tokenid]['userdetail']
		inbox = []
		for chat_id in users['chats']:
			inbox.append({
				"id": chat_id,
				"type": self.chats[chat_id]['type'],
				"name": self.chats[chat_id]['name'],
				"message": self.chats[chat_id]['message'][-1],
				"member": self.chats[chat_id]['member'],
				"updatedAt": self.chats[chat_id]['updatedAt']
			})
		return {'status': 'OK', 'data': inbox}	
	
	def get_inbox(self, tokenid, chat_id):
		if tokenid not in self.sessions:
			return {'status': 'ERROR', 'message': 'User Belum Login'}
		users = self.sessions[tokenid]['userdetail']

		if chat_id not in users['chats']:
			return {'status': 'ERROR', 'message': 'Chat tidak ditemukan'}

		inbox = {
			"id": chat_id,
			"type": self.chats[chat_id]['type'],
			"name": self.chats[chat_id]['name'],
			"message": self.chats[chat_id]['message'],
			"member": self.chats[chat_id]['member'],
			"updatedAt": self.chats[chat_id]['updatedAt']
		}
		return {'status': 'OK', 'data': inbox}

if __name__=="__main__":
	j = Chat()

	# testing getusername
	sesi1 = j.proses("login messi secret ")
	print(j.proses("getusername {} ".format(sesi1['tokenid'])))
	
	print(j.proses("getusername {} ".format("FAKE_TOKENID")))
	
	# # testing register
	# sesi = j.proses("register geprek secret ")
	# print(j.users)

	# sesi2 = j.proses("register geprek secret ")
	# print(j.users)

	# # testing inbox dan inboxall
	# sesi1 = j.proses("login messi secret")
	# print(j.proses("inboxall {}".format(sesi1['tokenid'])))
	# print(j.proses("inbox {} {}".format(sesi1['tokenid'], '1')))

	# sesi2 = j.proses("login henderson secret")
	# print(j.proses("inboxall {}".format(sesi2['tokenid'])))
	# print(j.proses("inbox {} {}".format(sesi2['tokenid'], '2')))

	# sesi3 = j.proses("login lineker secret")
	# print(j.proses("inboxall {}".format(sesi3['tokenid'])))
	# print(j.proses("inbox {} {}".format(sesi3['tokenid'], '1')))

	# # testing sendmsg
	# sesi1 = j.proses("login messi secret")
	# print(j.proses("sendmsg {} {} {}".format(sesi1['tokenid'], '1', 'testing send msg')))
	# print(j.proses("inbox {} {}".format(sesi1['tokenid'], '1')))

	# sesi2 = j.proses("login lineker secret")
	# print(j.proses("sendmsg {} {} {}".format(sesi2['tokenid'], '2', 'testing send msg')))
	# print(j.proses("inbox {} {}".format(sesi2['tokenid'], '2')))
