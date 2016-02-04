# srget [Project1_DataCom]

This program is written in python 

This program is for downloading file by getting file path from user 

# How to run this program
1. open the terminal in linux or mac os
2. Type in "srget -o <output file> [-c [<numConn>]] http://someurl.domain[:port]/path/to/file" 
    where <output file> is your desired name with the extension, [<numConn>] is number of simultaneous connection.
3. Press enter

# Library that used in this program
1. asyncore 
2. logging
3. cStringIO
4. sys
5. os
6. urlparse
7. socket
