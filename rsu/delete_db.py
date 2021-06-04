import sqlite3
db_name = 'rsu.sqlite3'

def delete_obu(rsu) :
    try :
        path = './'+ str(rsu) + '/' + db_name
        con = sqlite3.connect(path)
        cur = con.cursor
        cur.execute("DELETE FROM OBU")
        print('delete obu success')
    except Exception as e :
        print(e)
        print('delete db failed')
    finally :
        con.close()

def delete_rsustate(rsu) :
    try :
        path = './'+ str(rsu) + '/' + db_name
        con = sqlite3.connect(path)
        cur = con.cursor
        cur.execute("DELETE FROM RSUState")
        print('delete rsustate success')
    except Exception as e :
        print(e)
        print('delete db failed')
    finally :
        con.close()

rsu = ''
delete_obu()
delete_rsustate()