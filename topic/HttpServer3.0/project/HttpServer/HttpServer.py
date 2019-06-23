#!/etc/bin/env python3
#coding = utf-8
'''
name: Lz
time: 2019-4-23
title: http server 3.0
'''

from socket import *
import sys
import re
from threading import Thread
from setting import *
import time
import traceback

class HTTPServer(object):
	def __init__(self,addr=('0.0.0.0',80)):
		self.sockfd = socket()
		self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
		self.addr = addr
		self.bind(addr)

	def bind(self,addr):
		self.ip = addr[0]
		self.port = addr[1]
		self.sockfd.bind(addr)

	# HTTP服务器启动
	def serve_forever(self):
		self.sockfd.listen(10)
		print('Listen to the port %d ...'%self.port)
		while True:
			try:
				connfd,addr = self.sockfd.accept()
				print('Connect from',addr)
			except KeyboardInterrupt:
				sys.exit('退出服务器')
			except Exception:
				traceback.print_exc()
				continue
			handle_client = Thread(target=self.handle_request,args=(connfd,))
			handle_client.setDaemon(True)
			handle_client.start()

	def handle_request(self,connfd):
		# 接收浏览器请求
		request = connfd.recv(4096)
		request_lines = request.splitlines()
		# 获取请求行
		request_line = request_lines[0].decode()
		# 正则提取请求方式和请求内容
		pattern = r'(?P<METHOD>[A-Z]+)\s+(?P<PATH>/\S*)'
		try:
			env = re.match(pattern,request_line).groupdict()
		except:
			response_headlers = "HTTP1.1 500 Server Error\r\n"
			response_headlers += "\r\n"
			response_body = "Server Error"
			response = response_headlers + response_body
			connfd.send(response.encode())
			return

		# 将请求发送给WebFrame，得到返回数据结果
		status,response_body = self.send_request(env['METHOD'],env['PATH'])

		# 根据响应码组织响应头内容
		response_headlers = self.get_headlers(status)
		# 将结果组织为http response 格式发送给客户端
		response = response_headlers + response_body
		connfd.send(response.encode())
		connfd.close()

	# 和Frame进行交互，发送request，获取response
	def send_request(self,method,path):
		s = socket()
		# 连接WebFrame套接字
		s.connect(frame_addr)
		# 向WebFrame发送method和path
		s.send(method.encode())
		time.sleep(0.1)
		s.send(path.encode())

		# 接收WebFrame反馈的信息
		status = s.recv(128).decode()
		response_body = s.recv(4096).decode()

		return status,response_body
		
	def get_headlers(self,status):
		if status == '200':
			response_headlers = "HTTP/1.1 200 OK\r\n"
			response_headlers += "\r\n"
		elif status == '404':
			response_headlers = "HTTP/1.1 400 Not Found\r\n"
			response_headlers += "\r\n" 

		return response_headlers


def main():
	httpd = HTTPServer(ADDR)
	httpd.serve_forever()


if __name__ == "__main__":
	main()