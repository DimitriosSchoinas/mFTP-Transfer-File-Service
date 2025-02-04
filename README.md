# mFTP-Transfer-File-Service


The objective of this project is to implement the client and server programs of a File Transfer Service. In
short, the client sends commands to the server using UDP datagrams, while file data is transferred
using TCP sockets. The server is sequential, handling only one client at a given time. The files that can
be downloaded (or received) or uploaded (or sent) from the client to the server are stored in the
server in a directory where the server was launched. The files are transferred in 1024 byte blocks.

Project PDF:

[TPC1_2024.pdf](https://github.com/user-attachments/files/18660897/TPC1_2024.pdf)
