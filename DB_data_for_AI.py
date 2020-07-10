import pymysql
import numpy as np

"""
사용법
import DB_data_for_AI as DB -> 라이브러리 임포트

DB.DB_data('12:0')

DB.Iwant(tbale,parm) -> 특정 컬럼만 출력

**table과 parm은 문자열.
**마지막에 리턴되는 타입은 numpy.ndarray

ex) Feed_avr을 원할때
    Feed_avr = DB.Iwant('Feed', 'avr')
"""

"""
2차원 3x3배열을 원할때
DB.Uwant(table) -> 특정 table 출력
->[[avr1,avr2,avr3]
    [min1,min2,min3]
    [max1,max2,max3]]
"""

class MysqlController:
    def __init__(self, host, port, id, pw, db_name):
        self.conn = pymysql.connect(host=host, port= port, user= id, password=pw, db=db_name,charset='utf8')
        self.curs = self.conn.cursor()
    
    def select(self,sql):
        self.curs.execute(sql)
        self.conn.commit()
        result = self.curs.fetchall()
        return result

# DB 정보 입력
host = "175.121.249.37"
port = 8138

db = "fish_db"
mysql = MysqlController(host, port, 'root','kangnam',db)



# 데이터 문자열 처리 ( ((1,2)(1,2)) -> 1,2 / 1,2)
def strip(data):
    data = str(data)
    data = data.strip("((,)(,)")
    return data


def DB_data(time):
    time = "'%"+time+"%'"
    parm_list = ['avr','max','min']
    table_list = ['Feed', 'Oxygen', 'Temp']
    data_list = list()
    for table in table_list:
        for parm in parm_list:
        #SQL의 SELECT함수로 필요한 table의 필요한 column값 불러오기
            sql = "SELECT %s_%s FROM %s WHERE %s_time LIKE " %(table,parm,table,table) + time
            data = mysql.select(sql)

            data = strip(data)
            data_list.append(data)
    return data_list






# DB값 출력
def Iwant(table,parm):
    #SQL의 SELECT함수로 필요한 table의 필요한 column값 불러오기
    sql = "SELECT %s_%s FROM %s" %(table,parm,table)
    data = mysql.select(sql)
    # 데이터 행별로 리스트 화
    data = str(data).split(" ")

    # 리스트의 길이 측정
    n = len(data) 

    #리스트의 길이만큼 strip 명령 반복
    for i in range(n):
        data[i] = strip(data[i])

    # 데이터 배열화
    data_np = np.array(data)
    return data_np


def Uwant(table):
    parm_list = ['avr','min','max']
    data_list = list()
    for parm in parm_list:
    #SQL의 SELECT함수로 필요한 table의 필요한 column값 불러오기
        sql = "SELECT %s_%s FROM %s" %(table,parm,table)
        data = mysql.select(sql)
        # 데이터 행별로 리스트 화
        data = str(data).split(" ")

        # 리스트의 길이 측정
        n = len(data) 

        #리스트의 길이만큼 strip 명령 반복
        for i in range(n):
            data[i] = strip(data[i])
        
        data_list.append(data)



    # 데이터 배열화
    data_np = np.array(data_list)
    return data_np

