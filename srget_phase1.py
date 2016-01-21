#create socket
#bind socket
#connect socket
#send request



#open file

#get each piece of info from socket

#write each piece of info into file

#when done

#   readfile and cut off header

import socket as sk
import os

def mkDownloadRequest(serv, objName):
	return ("GET {o} HTTP/1.1\r\n"+"Host: {s}"+"\r\n\r\n").format(o=objName, s=serv)

#print "{!r}".format(mkDownloadRequest("intranet.mahidol", "/"))

servName = "www.google.com"
obj = "/"
# servName = "cs.muic.mahidol.ac.th"
# obj = "/courses/ds/hw/a1.pdf"
port = 80

## creat an empty socket
sock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)

## connect to a destination as specified by the pair
sock.connect((servName, port))

request = mkDownloadRequest(servName, obj)
sock.send(request)

# data_body = None
# content_length_num = None
def get_header(sock_):
	while True:
		data = sock.recv(1024)
		if "\r\n\r\n" in data:
			end_header_index = data.find("\r\n\r\n")
			header = data[:end_header_index]
			the_rest = data[end_header_index+4:] # +4 for \r\n\r\n
			break


	return header, the_rest


# print get_header(sock)


def get_content_length(sock_):

	header = get_header(sock_)[0]

	content_length_index = header.find("Content-Length:")
	end_header_index = header.find("\r\n\r\n")
	content_length_line = header[content_length_index:end_header_index]

	end_content_length_line_index = content_length_line.find("\r\n")
	colon_index = content_length_line.find(":")

	content_length_num = content_length_line[colon_index+2:end_content_length_line_index]


	return content_length_num

print get_content_length(sock)


def srget(sock_):
	

# if not os.path.exist

# f = open("data", 'w')

# while True:
# 	data = sock.recv(1024)
# 	f.write(data)


# 	# f.close
# 	# sock.close()
# 	break



# file_info = r.read()
# print file_info




















