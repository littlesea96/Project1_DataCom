#!/usr/bin/env python

import socket as sk
import os
from urlparse import urlparse
import sys
def headerDownloadRequest(serv, objName):
	return ("HEAD {o} HTTP/1.1\r\n"+"Host: {s}"+"\r\n" + "\r\n\r\n").format(o=objName, s=serv)

def mkDownloadRequest(serv, objName, filesize):
	return ("GET {o} HTTP/1.1\r\n"+"Host: {s}"+"\r\n" + "Range: bytes={h}-"+"\r\n\r\n").format(o=objName, s=serv, h=str(filesize))

def resumeDownloadRequest(serv, objName, filesize, end_point):
	return ("GET {o} HTTP/1.1\r\n"+"Host: {s}"+"\r\n" + "Range: bytes={h}-{e}"+"\r\n\r\n").format(o=objName, s=serv, h=str(filesize), e=str(end_point))

def open_socket(path, file_name, start_point):

	url = urlparse(path)

	servName = url[1]
	obj = url[2]
	port = url.port

	if port == None:
		port = 80

	## creat an empty socket
	sock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)

	## connect to a destination as specified by the pair
	sock.connect((servName, port))

	request = mkDownloadRequest(servName, obj, start_point)
	sock.send(request)

	return sock

def open_socket_for_resume(path, file_name, start_point, end_point):

	url = urlparse(path)

	servName = url[1]
	obj = url[2]
	port = url.port

	if port == None:
		port = 80

	## creat an empty socket
	sock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)

	## connect to a destination as specified by the pair
	sock.connect((servName, port))

	request = resumeDownloadRequest(servName, obj, start_point, end_point)
	sock.send(request)

	return sock

def get_header_socket(path):
	url = urlparse(path)

	servName = url[1]
	obj = url[2]
	port = url.port

	if port == None:
		port = 80

	## creat an empty socket
	sock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)

	## connect to a destination as specified by the pair
	sock.connect((servName, port))

	request = headerDownloadRequest(servName, obj)
	sock.send(request)

	header = sock.recv(1024)

	sock.close()

	return header

def get_header(sock_):
	data = ""
	while True:
		data_chunk = sock_.recv(1024)
		data += data_chunk
		if "\r\n\r\n" in data:
			end_header_index = data.find("\r\n\r\n")
			header = data[:end_header_index+3] # +3 for \r\n\r\n
			the_rest = data[end_header_index+4:] # +4 for \r\n\r\n
			break

	return header, the_rest



def get_content_length(header):

	if "Content-Length:" not in header:
		content_length_num = 0
	else:
		content_length_index = header.find("Content-Length:")
		end_header_index = header.find("\r\n\r\n")
		content_length_line = header[content_length_index:end_header_index]

		end_content_length_line_index = content_length_line.find("\r\n")
		colon_index = content_length_line.find(":")

		content_length_num = content_length_line[colon_index+2:end_content_length_line_index]


	return content_length_num


def srget():
	path = sys.argv[3]
	file_name = sys.argv[2]

	if "https" in path:
		sys.exit(2)
	elif "http://" not in path:
		path = "http://" + path

	if os.path.exists(file_name):
		
		file_size = os.path.getsize(file_name)

		content_length = get_content_length(get_header_socket(path))

		print "content_length", content_length
		print "file_size", file_size
		print file_size == int(content_length)

		if file_size == int(content_length):
			print "The file is already complete."
			sys.exit(2)

		else:

			print "enter else resume"

			fh = open("header_"+file_name+"_temp.txt", "r")

			ETag_old_file_id = ""

			content_length = 0

			for line in fh:
				if "ETag:" in line:
					find_quote = line.find('"')
					end_line = line.find("\r\n")

					ETag_old_file_id = line[find_quote:end_line]

					# print "ETag_old_file_id", ETag_old_file_id

				if "Last-Modified" in line:
					find_colon = line.find(": ")
					end_line = line.find("\r\n")
					last_modified_old_file = line[find_colon+2:end_line]
					
				if "Content-Length:" in line:
					find_colon = line.find(": ")
					end_line = line.find("\r\n")
					content_length = int(line[find_colon+2:end_line])

			fh.close()


			sock = open_socket_for_resume(path, file_name, file_size, content_length)
			# sock = open_socket_for_resume(path, file_name, 117095, 117129)

			header, the_rest = get_header(sock)

			data_body = the_rest


			#check the content length if it full or not
			#if full, do nothing
			last_modified = ""

			if "ETag:" in header:
				print "found Etag"

				ETag_index = header.find("ETag:")
				ETag_ = header[ETag_index:]

				end_ETag_line_index = ETag_.find("\r\n")
				ETag_line = ETag_[:end_ETag_line_index]
				quote_index = ETag_line.find('"')
				ETag = ETag_line[quote_index:]

			else:
				last_modified_index = header.find("Last-Modified")
				last_modified_ = header[last_modified_index:]
				end_last_modified_line_index = header.find("\r\n")
				colon_index = last_modified_.find(": ")
				last_modified = last_modified_[colon_index+2:end_last_modified_line_index]

			len_content = file_size + len(the_rest)

			print "ETag_old_file_id", ETag_old_file_id
			print "ETag", ETag

			print ETag_old_file_id == ETag

			if ETag_old_file_id == ETag:
				print "check ETag"

				f = open(file_name, "a+")
				f.write(the_rest)
				f.flush()

				while True:
					print "len_content", len_content
					print "content_length", content_length

					if len_content == int(content_length):
						os.remove("header_"+file_name+"_temp.txt")
						f.close()
						sock.close()
						break
					else:
						data_chunk = sock.recv(1024)
						data_body += data_chunk

						len_content += len(data_chunk)

						f.write(data_chunk)
						f.flush()

			elif last_modified_old_file == last_modified:
				print "check last modified"

				f = open(file_name, "a+")
				f.write(the_rest)
				f.flush()

				while True:

					if len_content == int(content_length):
						os.remove("header_"+file_name+"_temp.txt")
						f.close()
						sock.close()
						break
					else:
						data_chunk = sock.recv(1024)
						data_body += data_chunk

						len_content += len(data_chunk)

						f.write(data_chunk)
						f.flush()

			elif content_length == 0:
				sock.close()

				sock2 = open_socket(path, file_name, 0)

				header, the_rest = get_header(sock2)

				data_body = the_rest

				content_length = get_content_length(header)

				header_file_name = "header_"+file_name+"_temp.txt"

				fh = open(header_file_name, "a+")

				fh.write(header)
				fh.flush()

				f = open(file_name, "a+")
				f.write(the_rest)
				f.flush()

				while True:
					if content_length == 0 and len(data_chunk) == 0:
						os.remove("header_"+file_name+"_temp.txt")
						f.close()
						break
					elif len(data_body) == int(content_length):
						os.remove("header_"+file_name+"_temp.txt")
						f.close()
						sock.close()
						break
					else:
						data_chunk = sock.recv(1024)
						data_body += data_chunk

						f.write(data_chunk)
						f.flush()



	else:
		print "enter else"
		sock = open_socket(path, file_name, 0)
		# sock = open_socket_for_resume(path, file_name, 0, 117094)

		header, the_rest = get_header(sock)

		data_body = the_rest

		content_length = get_content_length(header)

		header_file_name = "header_"+file_name+"_temp.txt"

		fh = open(header_file_name, "a+")

		fh.write(header)
		fh.flush()

		f = open(file_name, "a+")
		f.write(the_rest)
		f.flush()

		while True:
			if content_length == 0 and len(data_chunk) == 0:
				os.remove("header_"+file_name+"_temp.txt")
				f.close()
				break
			elif len(data_body) == int(content_length):
				os.remove("header_"+file_name+"_temp.txt")
				f.close()
				sock.close()
				break
			else:
				data_chunk = sock.recv(1024)
				data_body += data_chunk

				f.write(data_chunk)
				f.flush()
	return data_body

srget()






