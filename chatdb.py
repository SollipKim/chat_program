import pymysql

def find_same_id(id):
    try :
        conn = pymysql.connect(host='localhost', user='root', password='fprhw523-als', db='mysql', charset='utf8mb4')
        # host = DB주소(localhost 또는 ip주소), user = DB id, password = DB password, db = DB명
        curs = conn.cursor()

        sql = "SELECT Name FROM chat_user WHERE Name = %s"                   # db에 예비아이디와 같은 아이디가 있는지 확인

        curs.execute(sql, (id))                                                   # 쿼리문 실행

        rows = curs.fetchone()                                              # 데이터 가져옴

        if rows is None :                                                   # 동일한 아이디가 없을 경우
            result = 0                                                      # 결과값 0으로 넘겨줌

        else:                                                               # 동일한 아이디가 있을 경우
            result = 1                                                      # 결과값 1로 넘겨줌

    finally :
        conn.close()                                                        # db 연결 종료

    return result

def find_same_password(id, password):
    try :
        conn = pymysql.connect(host='localhost', user='root', password='fprhw523-als', db='mysql', charset='utf8mb4')
        # host = DB주소(localhost 또는 ip주소), user = DB id, password = DB password, db = DB명
        curs = conn.cursor()

        sql = "SELECT Password FROM chat_user WHERE Name = %s and Password = %s"                   # db에 패스워드와 같은 패스워드가 있는지 확인

        curs.execute(sql, (id, password))                                                   # 쿼리문 실행

        rows = curs.fetchone()                                              # 데이터 가져옴

        if rows is None :                                                   # 동일한 패스워드가 없을 경우
            result = 0                                                      # 결과값 0으로 넘겨줌

        else:                                                               # 동일한 패스워드가 있을 경우
            result = 1                                                      # 결과값 1로 넘겨줌

    finally :
        conn.close()                                                        # db 연결 종료

    return result

def save_id(id, password):
    try :
        conn = pymysql.connect(host='localhost', user='root', password='fprhw523-als', db='mysql', charset='utf8mb4')
        # host = DB주소(localhost 또는 ip주소), user = DB id, password = DB password, db = DB명
        curs = conn.cursor()

        sql = "INSERT INTO chat_user (Name, Password) VALUES (%s, %s)"                  # id와 비밀번호를 db에 업데이트 함

        curs.execute(sql, (id, password))                                                   # 쿼리문 실행
        conn.commit()                                                        # 데이터 업데이트 내용 저장

    finally :
        conn.close()                                                        # db 연결 종료