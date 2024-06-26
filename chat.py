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
		self.sessions={}
		self.users = {}
		self.users['messi']={'password': 'surabaya', 'incoming' : {}, 'outgoing': {}}
		self.users['henderson']={'password': 'surabaya', 'incoming': {}, 'outgoing': {}}
		self.users['lineker']={'password': 'surabaya','incoming': {}, 'outgoing':{}}
		self.groups = {}
		self.realms = {}
		self.realms_info = {}
  
	def proses(self,data):
		j=data.split(" ")
		try:
			command=j[0].strip()
			if (command == 'auth'):
				username=j[1].strip()
				password=j[2].strip()
				logging.warning("AUTH: auth {} {}" . format(username, password))
				return self.autentikasi_user(username, password)
			elif (command == 'register'):
				username=j[1].strip()
				password=j[2].strip()
				logging.warning("REGISTER: register {} {}" . format(username, password))
				return self.register(username, password)
			elif (command == 'logout'):
				tokenid=j[1].strip()
				return self.logout(tokenid)
			else:
				return {'status': 'ERROR', 'message': '**Protocol Tidak Benar'}
		except KeyError:
			return { 'status': 'ERROR', 'message' : 'Informasi tidak ditemukan'}
		except IndexError:
			return {'status': 'ERROR', 'message': '--Protocol Tidak Benar'}

	def autentikasi_user(self,username,password):
		if (username not in self.users):
			return { 'status': 'ERROR', 'message': 'User Tidak Ada' }
		if (self.users[username]['password']!= password):
			return { 'status': 'ERROR', 'message': 'Password Salah' }
		tokenid = str(uuid.uuid4()) 
		self.sessions[tokenid]={ 'username': username, 'userdetail':self.users[username]}
		return { 'status': 'OK', 'tokenid': tokenid }

	def register(self,username,password):
		if (username in self.users):
			return { 'status': 'ERROR', 'message': 'User Sudah Ada' }
		self.users[username] = {"password": password, "incoming": {}, "outgoing": {}}
		tokenid = str(uuid.uuid4()) 
		self.sessions[tokenid]={ 'username': username, 'userdetail':self.users[username]}
		return { 'status': 'OK', 'tokenid': tokenid }
		
	def logout(self, tokenid):
		if tokenid not in self.sessions:
			return {'status': 'ERROR', 'message': 'User Belum Login'}
		del self.sessions[tokenid]
		return {'status': 'OK', 'message': 'User Berhasil Logout'}
     
if __name__=="__main__":
	j = Chat()