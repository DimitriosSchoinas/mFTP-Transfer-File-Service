from socket import *
import socket
import os
import sys

serverIP = None
UDP_SPort = None
TCP_CPort = None
socketBuffer = 1024  # socket Buffer size

def copy_file(filename):
    tcp_socket = socket.socket(family=AF_INET, type=SOCK_STREAM)
    tcp_socket.connect((serverIP, TCP_CPort))
    f = open(filename, "wb")
    data = tcp_socket.recv(socketBuffer)
    while True:
        f.write(data)
        data = tcp_socket.recv(socketBuffer)
        if not data:
            break
    f.close()
    tcp_socket.close()

def send_file(filename):
    tcp_socket = socket.socket(family=AF_INET, type=SOCK_STREAM)
    tcp_socket.connect((serverIP, TCP_CPort))
    with open(filename, "rb") as f:
        data = f.read(socketBuffer)
        while data:
            tcp_socket.send(data)
            data = f.read(socketBuffer)
    f.close()
    tcp_socket.close()
    
def exec_commands_from_file(command_file, udp_socket):
    # Check if the file exists
    if not os.path.exists(command_file):
        print("the indicated file does not exist on the client")
        return

    # Open the file and read commands line by line
    with open(command_file, "r") as file:
        for line in file:
            command = line.strip()
            if not command:
                continue 
            cmd_parts = command.split()

            match cmd_parts[0]:
                case "dir":
                    udp_socket.sendto(command.encode(), (serverIP, UDP_SPort))
                    msgFromServer, _ = udp_socket.recvfrom(socketBuffer)
                    msgSplit = msgFromServer.decode().split(":")
                    for i in msgSplit:
                        print(i)

                case "get":
                    if len(cmd_parts) != 3:
                        print("invalid number of arguments")
                        continue
                    elif os.path.exists(cmd_parts[-1]):
                        print("a file with the indicated name already exists on the client")
                        continue
                    toSend = cmd_parts[0] + " " + str(TCP_CPort) + " " + cmd_parts[1]
                    udp_socket.sendto(toSend.encode(), (serverIP, UDP_SPort))
                    msgFromServer, _ = udp_socket.recvfrom(socketBuffer)
                    if msgFromServer.decode() == "nack":
                        print("the indicated file does not exist on the server")
                        continue
                    copy_file(cmd_parts[-1])

                case "put":
                    if len(cmd_parts) != 3:
                        print("invalid number of arguments")
                        continue
                    elif not os.path.exists(cmd_parts[1]):
                        print("the indicated file does not exist on the client")
                        continue
                    toSend = cmd_parts[0] + " " + str(TCP_CPort) + " " + cmd_parts[-1]
                    udp_socket.sendto(toSend.encode(), (serverIP, UDP_SPort))
                    msgFromServer, _ = udp_socket.recvfrom(socketBuffer)
                    if msgFromServer.decode() == "nack":
                        print("a file with the indicated name already exists on the server")
                        continue
                    send_file(cmd_parts[1])

                case _:
                    print("invalid command")


def main():
    global serverIP, UDP_SPort, TCP_CPort

    if len(sys.argv) != 4:
        print("Usage: python mftp-client.py <server_addr> <UDP_SPort> <TCP_CPort>")
        sys.exit(1)

    serverIP = sys.argv[1]
    UDP_SPort = int(sys.argv[2])
    TCP_CPort = int(sys.argv[3])

    # Create a UDP socket
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    while True:
        sentence = input("What command do you wish to execute? ")
        match sentence.split()[0]:
            case "dir":
                UDPClientSocket.sendto(sentence.encode(), (serverIP, UDP_SPort))
                msgFromServer, _ = UDPClientSocket.recvfrom(socketBuffer)
                msgSplit = msgFromServer.decode().split(":")
                for i in msgSplit:
                    print(i)

            case "quit":
                UDPClientSocket.sendto(sentence.encode(), (serverIP, UDP_SPort))
                break

            case "get":
                if len(sentence.split()) != 3:
                    print("invalid number of arguments")
                    continue
                elif os.path.exists(sentence.split()[-1]):
                    print("a file with the indicated name already exists on the client")
                    continue
                toSend = sentence.split()[0] + " " + str(TCP_CPort) + " " + sentence.split()[1]
                UDPClientSocket.sendto(toSend.encode(), (serverIP, UDP_SPort))
                msgFromServer, _ = UDPClientSocket.recvfrom(socketBuffer)
                if msgFromServer.decode() == "nack":
                    print("the indicated file does not exist on the server")
                    continue
                copy_file(sentence.split()[-1])

            case "put":
                if len(sentence.split()) != 3:
                    print("invalid number of arguments")
                    continue
                elif not os.path.exists(sentence.split()[1]):
                    print("the indicated file does not exist on the client")
                    continue
                toSend = sentence.split()[0] + " " + str(TCP_CPort) + " " + sentence.split()[-1]
                UDPClientSocket.sendto(toSend.encode(), (serverIP, UDP_SPort))
                msgFromServer, _ = UDPClientSocket.recvfrom(socketBuffer)
                if msgFromServer.decode() == "nack":
                    print("a file with the indicated name already exists on the server")
                    continue
                send_file(sentence.split()[1])

            case "exec":
                if len(sentence.split()) != 2:
                    print("invalid number of arguments")
                    continue
                command_file = sentence.split()[1]
                exec_commands_from_file(command_file, UDPClientSocket)

            case _:
                print("Nonexistent command, try: 'dir', 'get', 'put', 'exec'")

if __name__ == "__main__":
    main()
	
    		
    #clientTCPSocket = socket(family=AF_INET, type=SOCK_STREAM)

    # open TCP connection
    #clientTCPSocket.connect((serverIP,serverPort))
    
    
    # send user's sentence over TCP connection
    #clientTCPSocket.send(sentence.encode())
    #splitS = sentence.split(":")
    # read bytes received from server
    #sentenceRecv = clientTCPSocket.recv(socketBuffer).decode()
    #splitRecv = sentenceRecv.split(":")
    #print(splitS[0], splitRecv[0])
    #sum = int(splitS[1]) + int(splitRecv[1])
    #print(splitS[1], splitRecv[1], sum)
    
    
    # close TCP connection
    #clientTCPSocket.close()

