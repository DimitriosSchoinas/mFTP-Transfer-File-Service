from socket import *
import getDirFiles
import os
import socket
import sys

socketBuffer = 1024
serverIP = None
UDP_Sport = None

def exec_get_cmd(addr, port, filename, udp_socket):
    if not os.path.exists(filename):
        udp_socket.sendto("nack".encode(), (addr))
    else:
        tcp_socket = socket.socket(family=AF_INET, type=SOCK_STREAM)
        tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcp_socket.bind((serverIP, port))
        tcp_socket.listen(1)
        udp_socket.sendto("ack".encode(), addr)
        connSocket, _ = tcp_socket.accept()
        with open(filename, "rb") as f:
            data = f.read(socketBuffer)
            while data:
                connSocket.send(data)
                data = f.read(socketBuffer)
        connSocket.close()
        tcp_socket.close()
        
def exec_put_cmd(addr, port, filename, udp_socket):
    if os.path.exists(filename):
        udp_socket.sendto("nack".encode(), (addr))
    else:
        tcp_socket = socket.socket(family=AF_INET, type=SOCK_STREAM)
        tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcp_socket.bind((serverIP, port))
        tcp_socket.listen(1)
        udp_socket.sendto("ack".encode(), addr)
        connSocket, _ = tcp_socket.accept()
        f = open(filename, "wb")
        data = connSocket.recv(socketBuffer)
        while True:
            f.write(data)
            data = connSocket.recv(socketBuffer)
            if not data:
                break
        f.close()
        connSocket.close()
        tcp_socket.close()

def main():
    # Create a UDP socket
    global serverIP, UDP_Sport
    
    if len(sys.argv) != 3:
        print("Usage: python mftp-server.py <server_addr> <UDP_SPort>")
        sys.exit(1)
    serverIP = sys.argv[1]
    UDP_Sport = int(sys.argv[2])
    
    udp_server_socket = socket.socket(family=AF_INET, type=SOCK_DGRAM)
    udp_server_socket.bind((serverIP, UDP_Sport))
    
    print("UDP server up and listening on", serverIP, UDP_Sport)

    while True:
        # Waits for incoming request
        sentence, addr = udp_server_socket.recvfrom(socketBuffer)  # Receiving client address and data
        decoded_sentence = sentence.decode()  # Decode the byte string to get the actual message

        match decoded_sentence.split()[0]:
            case "dir":
                toSend = getDirFiles.listDir()
                udp_server_socket.sendto(toSend.encode(), addr)  # Sending to the correct client address
            case "quit":
                print("Server shutting down.")
                udp_server_socket.close()  # Close the server socket
                break  # Exit the loop if the command is "quit"
            case "get":
                _, tcp_client_port, filename = decoded_sentence.split()
                tcp_client_port = int(tcp_client_port)
                exec_get_cmd(addr, tcp_client_port, filename, udp_server_socket)
            case "put":
                _, tcp_client_port, filename = decoded_sentence.split()
                tcp_client_port = int(tcp_client_port)
                exec_put_cmd(addr, tcp_client_port, filename, udp_server_socket)
            case "exec":
                # Add your handling code for "exec" here
                pass
            case _:
                print("Unknown command received.")

if __name__ == "__main__":
    main()



        #print("Connected by: ",str(addr))
        # read bytes received from client
        #sentence = connSocket.recv(socketBuffer).decode()
        #splitS = sentence.split(":")
        #print(splitS[0], serverName)
        #sum = int(splitS[1]) + serverNumber
        #print(splitS[1], serverNumber, sum)
        
        #sentenceToSend = serverName + ":" + str(serverNumber)
        # send modified sentence over the TCP connection
        #connSocket.send(sentenceToSend.encode())

        #connSocket.close()
        #if(int(splitS[1]) < 1 or int(splitS[1]) > 100):
        #	break;

