import sqlite3

db_name = 'rsu.sqlite3'
near = { 
  1 : [2, 8],
  2 : [1, 3, 9],
  3 : [2, 4, 10],
  4 : [3, 5, 11],
  5 : [4, 6, 12],
  6 : [5, 7, 13],
  7 : [6, 14],
  8 : [1, 9, 15],
  9 : [2, 8, 10, 16],
  10 : [3, 9, 11, 17],
  11 : [4, 10, 12, 18],
  12 : [5, 11, 13, 19], 
  13 : [6, 12, 14, 20],
  14 : [7, 13, 21],
  15 : [8, 16, 22],
  16 : [9, 15, 17, 23], 
  17 : [10, 16, 18, 24],
  18 : [11, 17, 19, 25],
  19 : [12, 18, 20, 26],
  20 : [13, 19, 21, 27],
  21 : [14, 20, 28], 
  22 : [15, 23, 29],
  23 : [16, 22, 24, 30], 
  24 : [17, 23, 25, 31],
  25 : [18, 24, 26, 32],
  26 : [19, 25, 27, 33],
  27 : [20, 26, 28, 34],
  28 : [21, 27, 35],
  29 : [22, 30, 38],
  30 : [23, 29, 31, 37],
  31 : [24, 30, 32, 39],
  32 : [25, 31, 33, 40],
  33 : [26, 32, 34, 41],
  34 : [27, 33, 35, 42],
  35 : [28, 34, 46],
  36 : [37, 38, 47], 
  37 : [30, 36, 39, 48],
  38 : [29, 36],
  39 : [31, 37, 43, 49], 
  40 : [32, 41, 43],
  41 : [33, 40, 42, 44],
  42 : [34, 41, 45], 
  43 : [39, 40, 44, 50], 
  44 : [41, 43, 45, 51], 
  45 : [42, 44, 46, 52], 
  46 : [35, 45, 53], 
  47 : [36, 48], 
  48 : [37, 47, 54, 60], 
  49 : [39, 50, 54],
  50 : [43, 49, 51, 55],
  51 : [44, 50, 52, 56],
  52 : [45, 51, 53, 57], 
  53 : [46, 52, 58], 
  54 : [48, 49, 55, 63],
  55 : [50, 54, 56, 65],
  56 : [51, 55, 57, 66],
  57 : [52, 56, 58, 67],
  58 : [53, 57, 68],
  59 : [60, 61],
  60 : [48, 59, 62],
  61 : [59, 62, 69], 
  62 : [60, 61, 63, 70], 
  63 : [54, 62, 64, 72], 
  64 : [63, 65, 73], 
  65 : [55, 64, 66, 74], 
  66 : [56, 65, 67, 77],
  67 : [57, 66, 68, 78], 
  68 : [58, 67, 79], 
  69 : [61, 70],  
  70 : [62, 69, 71], 
  71 : [70, 72, 85],
  72 : [63, 71, 80], 
  73 : [64, 74, 75], 
  74 : [65, 73, 76], 
  75 : [73, 76], 
  76 : [74, 75, 77, 82], 
  77 : [66, 76, 78], 
  78 : [67, 77, 79, 83], 
  79 : [68, 78, 84], 
  80 : [72, 81, 87], 
  81 : [80, 82, 89], 
  82 : [76, 81, 83, 90], 
  83 : [78, 82, 84, 91],
  84 : [79, 83, 92],
  85 : [71, 86], 
  86 : [85, 87, 96], 
  87 : [80, 86, 87], 
  88 : [94, 97, 100], 
  89 : [81, 87, 90, 93], 
  90 : [82, 89, 91, 95], 
  91 : [83, 90, 92, 98], 
  92 : [84, 91, 102], 
  93 : [89, 94, 96], 
  94 : [93, 95, 88],
  95 : [90, 94, 97, 98],
  96 : [86, 93, 101], 
  97 : [88, 95, 99, 100], 
  98 : [91, 95, 99], 
  99 : [97, 98, 103], 
  100 : [93, 97, 101, 102], 
  101 : [96, 100, 102], 
  102 : [92, 100, 101, 103], 
  103 : [99, 102]
}

def create_db(rsu_id) :
    try :
        db_path = './' + rsu_id + '/' + db_name
        con = sqlite3.connect(db_path)
        cur = con.cursor()

        # Create NearRSU table
        cur.execute("CREATE TABLE IF NOT EXISTS NearRSU (rsu_id INTEGER PRIMARY KEY)")

        # Create RSUState table
        cur.execute("CREATE TABLE IF NOT EXISTS RSUState (state_id INTEGER PRIMARY KEY AUTOINCREMENT, start_rsu INTEGER, end_rsu INTEGER, accident_type INTEGER, accident_size INTEGER)")

        # Create OBU table
        cur.execute("CREATE TABLE IF NOT EXISTS OBU (obu_id INTEGER PRIMARY KEY, path TEXT)")

        print('create_db success')
    except Exception as e :
        print('create db e : ', e)
        print('create_db failed')
    finally :
        con.close()

def insert_NearRSU(rsu_id) :
    try :
        db_path = './' + rsu_id + '/' + db_name
        print('rsu_id : ', rsu_id)
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        global near
        near_rsu_id = near[int(rsu_id)]
        print('near_rsu_id array : ', near_rsu_id)
        for _ in near_rsu_id :
            print(_)
            cur.execute(f'INSERT INTO NearRSU VALUES ({_});')
        con.commit()
        print('insert_NearRSU success')
    except Exception as e :
        print('insert NearRSU e : ', e)
        print('insert_NearRSU failed')

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--thing", action="store", required=True, dest="thingName")
args = parser.parse_args()

create_db(args.thingName)
insert_NearRSU(args.thingName)


