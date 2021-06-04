import sqlite3

db_file = 'rsu.sqlite3'

def insert_anomaly(rsu, accident_type, accident_size) :
    try :
        path = './' + rsu + '/' + db_file
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        sql = "INSERT INTO RSUState (rsu_id, accident_type, accident_size) VALUES (?, ?, ?);"
        result = cur.execute(sql, [rsu, accident_type, accident_size])
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
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        print('obu path : ', obu_path)
        obu_path = obu_path.split(',')
        result = cur.execute("SELECT rsu_id FROM RSUState WHERE rsu_id in (%s);" %(obu_path)).fetchall()
        if(len(result) > 0) :
            cur.close()
            conn.close()
            return True
        return False
        conn.close()
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
        result = cur.execute("SELECT obu_id, path FROM OBU;").fetchall()
        near = [(x[0], x[1]) for x in result]
        conn.close()
        return near
    except Exception as e :
        print('select_near_obu e : ', e)
        return False
    finally :
        conn.close()

def db_test(rsu) :
    try :
        path = './' + rsu + '/' + db_file
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        result = cur.execute("SELECT rsu_id FROM NearRSU;").fetchall()
        near = [x[0] for x in result]
        conn.close()
        return near
    except Exception as e :
        print('db test e : ', e)
        return False
    finally :
        conn.close()