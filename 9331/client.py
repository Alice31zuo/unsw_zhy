import sys
import socket
import threading
import pickle
import time
import random

class Client():
    def __init__(self,server_IP,server_port):
        self.server_address = (server_IP,server_port)
        #get the address
        self.Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = 0
        #set the port to 0 so get the ramdom port
        self.client_address = ('localhost', self.port)
        self.Socket.bind(self.client_address)
        self.Socket.connect(self.server_address)
        self.login = 0
        #set the login state to 0
        while True:
            self.user_name = input('please input your user name : ')
            self.password = input('please input your password : ')
            login_mess = pickle.dumps((self.user_name,self.password))
            self.Socket.send(login_mess)
            #send the login mess to server
            feedback = pickle.loads(self.Socket.recv(1024))
            print(feedback)
            #print the welcom sentences
            if feedback == 'you are login successful , thank you !':
                self.login = 1
                #chaneg the state to 1
                if self.login == 1 :
                    #start the command and listen threading
                    command = threading.Thread(target=self.commond(), args=())
                    command.start()
                    listen = threading.Thread(target=self.listening(), args=())
                    listen.start()
                    #after part is not work
                    private = threading.Thread(target=self.privatechat(), args=(address,))
                    private.start()
                    #after part is not work
                    p_connection, p_address = self.Socket.accept()
                    cp_connection = threading.Thread(target=self.privatechat_send(), args=(p_connection,))
                    cp_connection.start()



    def commond(self):
        while self.login :
            #when the  state is 1
            client_command = input()
            #get the command
            client_command_main = client_command.split(' ')
            if client_command_main[0] == 'message':
                #according the first word to select the fun
                receiver = client_command_main[1]
                for i in range(2):
                    client_command_main.pop(0)
                message = ' '.join(client_command_main)
                #get the message
                self.Socket.send(pickle.dumps(('message',self.user_name,receiver, message)))
                #send the message
                message = pickle.loads(self.Socket.recv(1024))
                #
                if message == 1 :
                    continue
                else:
                    print(message)

            elif client_command_main[0] == 'broadcast':
                message = ' '.join(client_command_main[1:])
                #get the message
                self.Socket.send(pickle.dumps(('broadcast',message,self.user_name)))
                #send the message

            elif client_command_main[0] == 'whoelse':
                self.Socket.send(pickle.dumps('whoelse'))
                message = pickle.loads(self.Socket.recv(1024))
                #get the list and print
                print(message)

            elif client_command_main[0] == 'whoelsesince':
                time = client_command_main[1]
                #get the time
                self.Socket.send(pickle.dumps(('whoelsesince',time)))
                #get the message list and print
                message = pickle.loads(self.Socket.recv(1024))
                print(message)

            elif client_command_main[0] == 'block':
                block_user_name = client_command_main[1]
                #get the user name would be blocked
                self.Socket.send(pickle.dumps(('block', self.user_name,block_user_name)))
                message = pickle.loads(self.Socket.recv(1024))
                print(message)

            elif client_command_main[0] == 'unblock':
                unblock_user_name = client_command_main[1]
                #get the user name would be unblocked
                self.Socket.send(pickle.dumps(('unblock', self.user_name, unblock_user_name)))
                message = pickle.loads(self.Socket.recv(1024))
                print(message)

            elif client_command_main[0] == 'logout':
                self.Socket.send(pickle.dumps('logout'))
                message = pickle.loads(self.Socket.recv(1024))
                print(message)
                self.logout()

            elif client_command_main[0] == 'startprivate':
                #this place is not working
                chater = client_command_main[1]
                self.Socket.send(pickle.dumps(('startprivate',chater)))
                message = pickle.loads(self.Socket.recv(1024))
                if type(message) == str:
                    print(message)
                else:
                    address = message[0]
                    #address_user = message[1]
                    self.privatechat(address)

            else:
                print('the command is not right ,please insert again')



    def listening(self):
        while self.login == 1:
            self.Socket.listen()
            message = pickle.loads(self.Socket.recv(1024))
            if (type(message)==tuple)and(message[0] == 'private_aqurie'):
                # this place is not working
                self.privatechat_send(message[1])
            else:
                print(message)




    def privatechat(self,address):
        # this place is not working
        self.Socket_p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Socket_p.bind(self.client_address)
        self.Socket_p.connect(address)
        private_listen = threading.Thread(target=self.private_listen(), args=(self.Socket_p,))
        private_listen.start()
        while True:
            send_message = input()
            send_message = send_message.split(' ')
            if send_message[0] == 'stopprivate':
                self.Socket_p.close()
                self.commond()
            send_message[1] = self.user_name
            send_message = ' '.join(send_message)
            self.Socket_p.send(pickle.dumps(send_message))


    def private_listen(self,Socket_P):
        # this place is not working
        while True:
            Socket_P.listen()
            message = pickle.loads(self.Socket.recv(1024))
            print(message)



    def privatechat_send(self,connection):
        # this place is not working
        self.Socket_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Socket_s.bind(self.client_address)
        while True:
            send_message = input()
            send_message = send_message.split(' ')
            if send_message[0] == 'stopprivate' :
                connection.close()
                self.commond()
            send_message[1] = self.user_name
            send_message = ' '.join(send_message)
            connection.send(pickle.dumps(send_message))


    def logout(self):
        self.login = 0
        self.Socket.close()
        print('you are log out success')


if len(sys.argv)!= 3:
    print('please insert the right arg')
else:
    client = Client(sys.argv[1],int(sys.argv[2]))


#Client('127.0.0.1',5000)



















