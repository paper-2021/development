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
        result = cur.execute("SELECT rsu_id FROM RSUState WHERE rsu_id in (%s);" %(obu_path)).fetchall()
        if(len(result) > 0) :
            cur.close()
            conn.close()
            return True
        conn.close()
    except Exception as e :
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
        return False
    finally :
        conn.close()