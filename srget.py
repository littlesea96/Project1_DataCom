import socket as sk

def mkDownloadRequest(serv, objName):
	return ("GET {o} HTTP/1.1\r\n"+"Host: {s}"+"\r\n\r\n").format(o=objName, s=serv)

#print "{!r}".format(mkDownloadRequest("intranet.mahidol", "/"))

# servName = "www.google.com"
servName = "cs.muic.mahidol.ac.th"
obj = "/courses/ds/hw/a1.pdf"
port = 80

## creat an empty socket
sock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)

## connect to a destination as specified by the pair
sock.connect((servName, port))

request = mkDownloadRequest(servName, obj)
sock.send(request)

while True:
    data = sock.recv(1024)

    # print data
    #print "{!r}".format(data)

    content_length_index = data.find("Content-Length:")
    end_header_index = data.find("\r\n\r\n")

    content_length_line = data[content_length_index:end_header_index]
    content_length_num_index = content_length_line.find(":") + 2
    end_cln_index = content_length_line.find("\r\n")

    content_length_num = content_length_line[content_length_num_index:end_cln_index]

    print "content lenght", content_length_num

    # end_body_index = data.find("<\HTML>")


    data_body = data[end_header_index:].lstrip()
    # data_body = data_body.
    # print data_body
    print "body len", len(data_body)

    if len(data_body) == content_length_num:
        sock.close()
        break
