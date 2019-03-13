import socket
import threading
import sys
from chatdb import *

class Server:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                                    # tcp 소켓을 만듬
    connections = []                                                                            # 소켓을 저장함
    already = 0                                                                                 # 연결을 원하는 유저가 있는지 확인하는 변수
    chat_with = []                                                                              # 같이 채팅하기 원하는 유저의 소켓번호 저장

    def __init__(self):
        self.sock.bind(('', 10000))                                                             # 서버 포트번호를 소켓과 연결시킴
        self.sock.listen(1)                                                                     # 서버가 클라이언트 연결을 듣게함

    def handler(self, csocket, addr):
        while True:
            csocket.sendall(bytes('반갑습니다\n', 'utf-8'))
            csocket.sendall(bytes('회원가입을 아직 하지 않으셨으면 1번을 입력하시고 아이디가 있으시면 2번을 입력해주세요', 'utf-8'))
            check = csocket.recv(4).decode('utf-8')                                             # 소켓에서 데이터 받아옴

            # 회원가입을 해야할 경우
            if check == '1':
                csocket.sendall(bytes('생성하길 원하는 아이디를 입력하세요\n', 'utf-8'))
                csocket.sendall(bytes('아이디는 최대 12자까지 입력 가능합니다', 'utf-8'))

                # 아이디 중복검사 / 회원정보 비밀번호 저장
                while True:
                    id = csocket.recv(48).decode('utf-8')                                       # 소켓에서 설정하기 원하는 아이디 받아옴
                    use = find_same_id(id)                                                      # 같은 아이디가 있으면 use 변수에 1 할당

                    # 만들기 원하는 아이디가 이미 있을 경우
                    if use == 1:
                        csocket.sendall(bytes('해당 아이디는 사용중인 아이디입니다\n', 'utf-8'))
                        csocket.sendall(bytes('다른 아이디를 입력해 주세요', 'utf-8'))
                        use = 0
                    # 아이디 생성이 가능할 경우
                    else:
                        csocket.sendall(bytes('생성할 패스워드를 입력해주세요\n', 'utf-8'))
                        csocket.sendall(bytes('패스워드는 최대 30자까지 입력 가능합니다', 'utf-8'))
                        password = csocket.recv(120).decode('utf-8')                            # 소켓에서 설정하기를 원하는 비밀번호 받아옴
                        save_id(id, password)                                                   # 아이디와 비밀번호 db에 저장
                        csocket.sendall(bytes('가입이 완료되었습니다', 'utf-8'))
                        break

            # 회원 가입이 끝나거나 이미 회원가입을 했을 경우
            while True:
                csocket.sendall(bytes('아이디를 입력해주세요', 'utf-8'))
                id = csocket.recv(48).decode('utf-8')                                           # 소켓에서 아이디 받아옴
                use = find_same_id(id)                                                          # 같은 아이디가 있으면 use 변수에 1 할당

                # 같은 아이디가 없을 경우(아이디를 잘못 입력했을 경우)
                if use == 0:
                    csocket.sendall(bytes('잘못된 아이디입니다. 다시 입력해주세요', 'utf-8'))
                # 아이디를 올바르게 입력했을 경우
                else:
                    csocket.sendall(bytes('비밀번호를 입력해주세요', 'utf-8'))
                    # 올바른 아이디 입력 후 비밀번호 입력 받는 무한루프
                    while True:
                        password = csocket.recv(120).decode('utf-8')                            # 소켓에서 비밀번호 받아옴
                        use = find_same_password(id, password)                                  # 같은 패스워드가 있는지 확인함
                        if use == 0:
                            csocket.sendall(bytes('잘못된 비밀번호입니다. 다시 입력해주세요', 'utf-8'))
                        else:
                            csocket.sendall(bytes('접속에 성공하였습니다.', 'utf-8'))
                            self.connections.append(id)                                         # 유저 아이디를 소켓들 목록에 넣어줌
                            csocket.sendall(bytes('''귓속말 기능을 사용하려면 '유저명 + >' 를 입력하세요 ''', 'utf-8'))
                            break

                if use == 1:
                    break
            if use == 1:
                break

        # 특정 유저와 접속을 원할 경우
        while True:
            data = csocket.recv(1024).decode('utf-8')                                              # 소켓에서 데이터 받아옴

            num = len(data)

            if data[num-1] != '>' :                                                             # 대화를 원하는 유저가 없을 경우
                break

            else :
                Want_chat = data[0 : num - 1]                                                   # 대화 원하는 유저명 뽑아옴
                
                # 유저가 연결을 원하는 유저가 있는 소켓을 찾아 연결
                i = 1
                for connection in self.connections :
                    if connection != Want_chat:
                        if i == len(self.connections) :
                            self.already = 1
                            be = find_same_id(Want_chat)                                        # 현재 접속 중이 아니지만 연결을 원하는 아이디가 있는지 검사
                            if be == 1:                                                         # 연결을 원하는 아이디가 있을 경우
                                csocket.sendall(bytes('%s 님이 접속중이 아닙니다.' % Want_chat, 'utf-8'))
                            else :
                                csocket.sendall(bytes('아이디 %s 는 존재하지 않는 아이디 입니다.' % Want_chat, 'utf-8'))
                        continue
                    else :                                                                      # 대화를 원하는 유저가 접속중일 경우
                        self.chat_with.append(csocket)
                        self.chat_with.append(id)
                        self.chat_with.append(self.connections[i - 1])
                        self.chat_with.append(Want_chat)
                        self.already = 1
                        csocket.sendall(bytes('%s 님과 연결이 완료되었습니다.' % Want_chat, 'utf-8'))
                        csocket.sendall(bytes('보내고 싶은 내용을 입력하세요\n' , 'utf-8'))
                        csocket.sendall(bytes('''대화 상대를 추가하고 싶다면 '유저명 + >' 를 입력하세요\n''', 'utf-8'))
                        csocket.sendall(bytes('''유저와 연결을 끊고 싶다면 '유저명 + <' 를 입력하세요\n''', 'utf-8'))
                        break

            while True:
                data = csocket.recv(1024).decode('utf-8')                                       # 소켓에서 데이터 받아옴
                num = len(data)

                if data[num-1] == '<':
                    self.already = 0
                    self.chat_with.remove(csocket)
                    self.chat_with.remove(id)
                    break

                i = 0
                for connection in self.chat_with :                                              # 연결된 소켓들에게 해당 내용 보내줌
                    if i == 0 or i % 2 == 0:
                        if connection != csocket:
                            user_name = id + ' - '                     # 메세지 보내는 유저 이름
                            connection.send((user_name + data).encode('utf-8'))
                    i = i + 1

                if not data :                                                                   # 더이상 소켓안에 데이터가 없으면
                    print(str(addr[0]) + ':' + str(addr[1]), "disconnected")
                    self.chat_with.remove(csocket)                                              # 리스트에 저장된 소켓 지움
                    self.chat_with.remove(id)
                    self.connections.remove(csocket)
                    self.connections.remove(id)
                    csocket.close()                                                             # 클라이언트 연결 끊음


        # 연결을 원하는 유저가 없을 경우 불특정 다수와 통신
        first = 0
        while True:
            data = csocket.recv(1024).decode('utf-8')
            num = len(data)

            if data[num - 1] == '>':
                self.already = 0
                break

            i = 0
            for connection in self.connections:                                                 # 연결된 소켓들에게 해당 내용 보내줌
                if i==0 or i%2 ==0:
                    if connection == csocket:
                        i = i + 1
                        continue
                    user_name = id + ' - '                                                      # 메세지 보내는 유저 이름
                    connection.send((user_name + data).encode('utf-8'))
                i = i+1
            if not data :                                                                       # 더이상 소켓안에 데이터가 없으면
                print(str(addr[0]) + ':' + str(addr[1]), "disconnected")
                self.connections.remove(csocket)                                                # 소켓에 있는 데이터 지움
                csocket.close()                                                                 # 클라이언트 연결 끊음

    def run(self):
        while True:
            csocket, addr = self.sock.accept()                                                  # 서버에 c소켓 만듬
            cThread = threading.Thread(target= self.handler, args=(csocket, addr))              # handler를 쓰레드에 넣음
            cThread.daemon = True                                                               # 데몬쓰레드로 설정, 메인 쓰레드 종료시 자동종료
            cThread.start()                                                                     # 쓰레드 실행
            self.connections.append(csocket)                                                    # c소켓을 소켓들 목록에 넣어줌
            print(str(addr[0]) + ':' + str(addr[1]), "connected")                               # 어떤 클라이언트가 연결되었는지 보여줌

class Client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # tcp 소켓을 만듬

    def sendMsg(self):
        while True:
            self.sock.send(bytes(input(""), 'utf-8'))                                           # 입력받은 문자열을 클라이언트 소켓을 통해 tcp연결로 보냄

    def __init__(self, address):
        self.sock.connect((address, 10000))                                                     # 클라이언트와 서버간의 tcp연결을 시작함

        iThread = threading.Thread(target=self.sendMsg)                                         # sendMsg를 쓰레드에 넣음
        iThread.daemon = True                                                                   # 데몬쓰레드로 설정, 메인 쓰레드 종료시 자동종료
        iThread.start()                                                                         # 쓰레드 실행

        while True:
            data = self.sock.recv(1024).decode('utf-8')                                         # 소켓이 서버로부터 받은 내용을 data로 옮겨옴

            if not data :
                break                                                                           # 데이터가 없을경우 빠져나옴
            print(data)                                                                         # 받은 data를 프린트 해줌



if (len(sys.argv) > 1):
    client = Client(sys.argv[1])
else:
    server = Server()
    server.run()