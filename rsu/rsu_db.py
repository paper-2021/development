import sqlite3

db_file = 'rsu.sqlite3'

def insert_anomaly(rsu, start, end, accident_type, accident_size) :
    try :
        path = './' + rsu + '/' + db_file
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        result = cur.execute("INSERT INTO RSUState (start_rsu, end_rsu, accident_type, accident_size) VALUES (%d, %d, %d, %d);" % (start, end, accident_type, accident_size))
        conn.commit()
        conn.close()
        return True
    except Exception as e :
        print('insert_anomaly error : ', e)
        return False
    finally :
        conn.close()

def register_obu(rsu, obu_id, obu_path) :
    try :
        path = './' + rsu + '/' + db_file
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        sql = "INSERT INTO OBU VALUES (?, ?);"
        obu_id = int(obu_id)
        result = cur.execute(sql, [obu_id, obu_path])
        # print('register_obu insert result : ', result)
        conn.commit()
        conn.close()
        return True
    except Exception as e :
        print('register_obu error : ', e)
        return False
    finally :
        conn.close()

def check_anomaly(rsu, obu_path) :
    try :
        path = './' + rsu + '/' + db_file
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        print('obu path : ', obu_path)
        # obu_path = obu_path.split(',')
        # obu_path = list(map(int, obu_path))
        result = cur.execute('SELECT start_rsu, end_rsu FROM RSUState').fetchall()
        print('select RSUState result : ', result)
        for i in result :
            a_s = int(i[0])
            a_e = int(i[1])
            print(f'a_s : {a_s}, a_e : {a_e}')
            for j in range(len(obu_path) - 1) :
                if(int(obu_path[j]) == a_s and int(obu_path[j + 1]) == a_e) :
                    print(f'obu_path[j] : {obu_path[j]}, obu_path : {obu_path[j + 1]}')
                    conn.close()
                    return True
        conn.close()            
        return False
    except Exception as e :
        print('check anomaly e : ', e)
        return False
    finally :
        conn.close()

def select_near_rsu(rsu) :
    try :
        path = './' + rsu + '/' + db_file
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        result = cur.execute("SELECT rsu_id FROM NearRSU;").fetchall()
        near = [x[0] for x in result]
        conn.close()
        return near
    except Exception as e :
        print('select near rsu e : ', e)
        return False
    finally :
        conn.close()

def select_near_obu(rsu) :
    try :
        path = './' + rsu + '/' + db_file
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        result = cur.execute("SELECT obu_id, path FROM OBU WHERE obu_id = 1;").fetchall()
        print(result)
        near = [(x[0], x[1]) for x in result]
        conn.close()
        return near
    except Exception as e :
        print('select_near_obu e : ', e)
        return False
    finally :
        conn.close()

def delete_obu(rsu, obu) :
    try :
        path = './' + rsu + '/' + db_file
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        obu = int(obu)
        result = cur.execute("DELETE FROM OBU WHERE obu_id = (%d);" %(obu))
        conn.close()
        return True
    except Exception as e :
        print('delete obu e : ', e)
        return False
    finally :
        conn.close()

def update_obu_path(rsu, obu, obu_path) :
    try :
        path = './' + rsu + '/' + db_file
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        obu = int(obu)
        obu_path = list(map(str, obu_path))
        obu_path.insert(0, str(rsu))
        obu_path = ','.join(obu_path)
        print('obu_path : ', obu_path, 'type : ', type(obu_path))
        print('update obu_path : ', obu_path)
        cur.execute('DELETE FROM OBU;')
        sql = "INSERT INTO OBU VALUES (?, ?);"
        result = cur.execute(sql, [1, obu_path])
        conn.commit()
        return True
    except Exception as e :
        print('update obu path e : ', e)
        return False
    finally :
        conn.close()


def db_test(rsu) :
    try :
        path = './' + rsu + '/' + db_file
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        result = cur.execute("SELECT * FROM NearRSU;").fetchall()
        near = [x[0] for x in result]
        conn.close()
        return near
    except Exception as e :
        print('db test e : ', e)
        return False
    finally :
        conn.close()