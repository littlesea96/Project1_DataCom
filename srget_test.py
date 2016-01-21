import socket as sk

def mkDownloadRequest(serv, objName):
	return ("GET {o} HTTP/1.1\r\n"+"Host: {s}"+"\r\n\r\n").format(o=objName, s=serv)

#print "{!r}".format(mkDownloadRequest("intranet.mahidol", "/"))

servName = "www.google.com"
port = 80

## creat an empty socket
sock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)

## connect to a destination as specified by the pair
sock.connect((servName, port))

request = mkDownloadRequest(servName, "/")
sock.send(request)

while True:
    data = sock.recv(1024)
    content_length_index = data.find("Content-Length:") +1
    end_header = data.find("\r\n\r\n")

    content_length_line = data[content_length_index:end_content_lengt_index]
    content_length_num_index = content_length_line.find(":") + 2
    end_cln_index = content_length_line.find("\r\n")

    content_length_num = content_length_line[content_length_num_index:end_cln_index]

    print "content length"
    print content_length_num
	body_data = data[:end_header]
	print "len data",len(body_data)



    sock.close()
    break
