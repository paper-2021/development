import sqlite3

db_file = 'rsu.sqlite3'

def create() :
    try:
        conn = sqlite3.connect('rsu.db')
        cur = conn.cursor()
        cur.execute("CREATE TABLE RSU(rsu_id INTEGER PRIMARY KEY, rsu_ip TEXT, traffic INTEGER);")
        cur.execute("CREATE TABLE NearRSU(rsu_id INTEGER PRIMARY KEY, FOREIGN KEY(rsu_id) REFERENCES RSU(rsu_id));")
        cur.execute("CREATE TABLE RSUState(state_id INTEGER PRIMARY KEY AUTOINCREMENT, rsu_id INTEGER, accident_type INTEGER, accident_size INTEGER, FOREIGN KEY(rsu_id) REFERENCES RSU(rsu_id));")
        cur.execute("CREATE TABLE OBU(obu_id INTEGER PRIMARY KEY, path TEXT);")
        cur.close()
        conn.close() 
    except sqlite3.OperationalError:
        print('Table already exist')

def insert_anomaly(rsu_id, accident_type, accident_size) :
    try :
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        sql = "INSERT INTO RSUState (rsu_id, accident_type, accident_size) VALUES (?, ?, ?);"
        result = cur.execute(sql, [rsu_id, accident_type, accident_size])
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e :
        print('insert_anomaly error : ', e)
        return False

def register_obu(obu_id, path) :
    try :
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        sql = "INSERT INTO OBU VALUES (?, ?);"
        result = cur.execute(sql, [obu_id, path])
        # print('register_obu insert result : ', result)
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e :
        print('register_obu error : ', e)
        return False

def check_anomaly(path) :
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    result = cur.execute("SELECT rsu_id FROM RSUState WHERE rsu_id in (%s);" %(path)).fetchall()
    if(len(result) > 0) :
        cur.close()
        conn.close()
        return True
    cur.close()
    conn.close()
    return False

def select_near_rsu() :
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    result = cur.execute("SELECT rsu_id FROM NearRSU;").fetchall()
    near = [x[0] for x in result]
    cur.close()
    conn.close()
    return near
