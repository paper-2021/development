import sqlite3

db_name = 'OBU_ver3.sqlite3'

links = [(1, 2, '37.524', '127.053', '37.519', '127.056'),
(2, 3, '37.519', '127.056', '37.514', '127.060'),
(3, 4, '37.514', '127.060', '37.508', '127.062'),
(4, 5, '37.508', '127.062', '37.505', '127.064'),
(5, 6, '37.505', '127.064', '37.501', '127.067'),
(6, 7, '37.501', '127.067', '37.496', '127.069'),
(1, 8, '37.524', '127.053', '37.524', '127.047'),
(2, 9, '37.519', '127.056', '37.518', '127.050'),
(3, 10, '37.514', '127.060', '37.513', '127.053'),
(4, 11, '37.508', '127.062', '37.506', '127.056'),
(5, 12, '37.505', '127.064', '37.503', '127.058'),
(6, 13, '37.501', '127.067', '37.198', '127.061'),
(7, 14, '37.496', '127.069', '37.494', '127.063'),
(8, 9, '37.524', '127.047', '37.518', '127.050'),
(9, 10, '37.518', '127.050', '37.513', '127.053'),
(10, 11, '37.513', '127.053', '37.506', '127.056'),
(11, 12, '37.506', '127.056', '37.503', '127.058'),
(12, 13, '37.503', '127.058', '37.198', '127.061'),
(13, 14, '37.198', '127.061', '37.494', '127.063'),
(8, 15, '37.524', '127.047', '37.523', '127.039'),
(9, 16, '37.518', '127.050', '37.517', '127.041'),
(10, 17, '37.513', '127.053', '37.510', '127.043'),
(11, 18, '37.506', '127.056', '37.504', '127.048'),
(12, 19, '37.503', '127.058', '37.500', '127.050'),
(13, 20, '37.198', '127.061', '37.496', '127.052'),
(14, 21, '37.494', '127.063', '37.490', '127.055'),
(15, 16, '37.523', '127.039', '37.517', '127.041'),
(16, 17, '37.517', '127.041', '37.510', '127.043'),
(17, 18, '37.510', '127.043', '37.504', '127.048'),
(18, 19, '37.504', '127.048', '37.500', '127.050'),
(19, 20, '37.500', '127.050', '37.496', '127.052'),
(20, 21, '37.496', '127.052', '37.490', '127.055'),
(15, 22, '37.523', '127.039', '37.521', '127.033'),
(16, 23, '37.517', '127.041', '37.515', '127.035'),
(17, 24, '37.510', '127.043', '37.508', '127.038'),
(18, 25, '37.504', '127.048', '37.502', '127.042'),
(19, 26, '37.500', '127.050', '37.498', '127.044'),
(20, 27, '37.496', '127.052', '37.494', '127.046'),
(21, 28, '37.490', '127.055', '37.488', '127.049'),
(22, 23, '37.521', '127.033', '37.508', '127.038'),
(23, 24, '37.508', '127.038', '37.508', '127.038'),
(24, 25, '37.508', '127.038', '37.502', '127.042'),
(25, 26, '37.502', '127.042', '37.498', '127.044'),
(26, 27, '37.498', '127.044', '37.494', '127.046'),
(27, 28, '37.494', '127.046', '37.488', '127.049'),
(22, 29, '37.521', '127.033', '37.519', '127.028'),
(23, 30, '37.508', '127.038', '37.514', '127.030'),
(24, 31, '37.508', '127.038', '37.507', '127.033'),
(25, 32, '37.502', '127.042', '37.500', '127.036'),
(26, 33, '37.498', '127.044', '37.495', '127.039'),
(27, 34, '37.494', '127.046', '37.492', '127.040'),
(28, 35, '37.488', '127.049', '37.485', '127.041'),
(29, 30, '37.519', '127.028', '37.514', '127.030'),
(30, 31, '37.514', '127.030', '37.507', '127.033'),
(31, 32, '37.507', '127.033', '37.500', '127.036'),
(32, 33, '37.500', '127.036', '37.495', '127.039'),
(33, 34, '37.495', '127.039', '37.492', '127.040'),
(34, 35, '37.492', '127.040', '37.485', '127.041'),
(29, 38, '37.519', '127.028', '37.517', '127.023'),
(38, 36, '37.517', '127.023', '37.516', '127.019'),
(30, 37, '37.514', '127.030', '37.511', '127.021'),
(31, 39, '37.507', '127.033', '37.504', '127.024'),
(32, 40, '37.500', '127.036', '37.498', '127.031'),
(40, 43, '37.498', '127.031', '37.497', '127.027'),
(33, 41, '37.495', '127.039', '37.494', '127.033'),
(41, 44, '37.494', '127.033', '37.492', '127.029'),
(34, 42, '37.492', '127.040', '37.490', '127.035'),
(42, 45, '37.490', '127.035', '37.489', '127.031'),
(35, 46, '37.485', '127.041', '37.484', '127.034'),
(40, 41, '37.498', '127.031', '37.494', '127.033'),
(41, 42, '37.494', '127.033', '37.490', '127.035'),
(36, 37, '37.516', '127.019', '37.511', '127.021'),
(37, 39, '37.511', '127.021', '37.504', '127.024'),
(39, 43, '37.504', '127.024', '37.497', '127.027'),
(43, 44, '37.497', '127.027', '37.492', '127.029'),
(44, 45, '37.492', '127.029', '37.489', '127.031'),
(45, 46, '37.489', '127.031', '37.484', '127.034'),
(39, 49, '37.504', '127.024', '37.503', '127.021'),
(43, 50, '37.497', '127.027', '37.496', '127.024'),
(44, 51, '37.492', '127.029', '37.492', '127.026'),
(45, 52, '37.489', '127.031', '37.488', '127.028'),
(46, 53, '37.484', '127.034', '37.483', '127.029'),
(49, 50, '37.503', '127.021', '37.496', '127.024'),
(50, 51, '37.496', '127.024', '37.492', '127.026'),
(51, 52, '37.492', '127.026', '37.488', '127.028'),
(52, 53, '37.488', '127.028', '37.483', '127.029'),
(49, 54, '37.503', '127.021', '37.502', '127.018'),
(50, 55, '37.496', '127.024', '37.495', '127.021'),
(51, 56, '37.492', '127.026', '37.490', '127.023'),
(52, 57, '37.488', '127.028', '37.487', '127.024'),
(53, 58, '37.483', '127.029', '37.483', '127.025'),
(36, 47, '37.516', '127.019', '37.514', '127.015'),
(37, 48, '37.511', '127.021', '37.509', '127.016'),
(47, 48, '37.514', '127.015', '37.509', '127.016'),
(48, 54, '37.509', '127.016', '37.502', '127.018'),
(54, 55, '37.502', '127.018', '37.495', '127.021'),
(55, 56, '37.495', '127.021', '37.490', '127.023'),
(56, 57, '37.490', '127.023', '37.487', '127.024'),
(57, 58, '37.487', '127.024', '37.483', '127.025'),
(48, 60, "37.509", "127.016", "37.508", "127.011"), 
(59, 60, "37.514", "127.007", "37.508", "127.011"), 
(60, 62, "37.508", "127.011", "37.507", "127.008"), 
(61, 62, '37.512', '127.006', '37.507', '127.008'), 
(62, 63, '37.507', '127.008', '37.504', '127.010'), 
(62, 70, '37.507', '127.008', '37.505', '127.004'), 
(61, 69, '37.512', '127.006', '37.509', '127.002'), 
(69, 70, '37.509', '127.002', '37.505', '127.004'),
(70, 71, '37.505', '127.004','37.505', '127.000'), 
(71, 72, '37.505', '127.000', '37.501', '127.003'), 
(63, 72, '37.504', '127.010', '37.501', '127.003'), 
(63, 64, '37.504', '127.010', '37.495', '127.012'), 
(72, 80, '37.501', '127.003', '37.499', '126.998'), 
(71, 85, '37.505', '127.000', '37.501', '126.956'), 
(85, 86, '37.501', '126.956', '37.499', '126.985'), 
(64, 65, '37.495', '127.012', '37.493', '127.013'),
(55, 65, '37.495', '127.021', '37.493', '127.013'), 
( 65, 66, '37.493', '127.013', '37.488', '127.014'), 
(65, 74, '37.493', '127.013', '37.492', '127.011'), 
(64, 73, '37.504', '127.010','37.494', '127.010'), 
(56, 66, '37.490', '127.023', '37.488', '127.014'), 
(66, 67, '37.488', '127.014', '37.484', '127.016'), 
(66, 77, '37.488', '127.014', '37.486', '127.009'), 
(57, 67, '37.487', '127.024', '37.484', '127.016'), 
(67, 68, '37.484', '127.016', '37.482', '127.018'), 
(58, 68, '37.483', '127.025', '37.482', '127.018'), 
(68, 79, '37.482', '127.018', '37.480', '127.012'), 
(67, 78, '37.484', '127.016', '37.484', '127.011'),
(77, 78,'37.486', '127.009', '37.484', '127.011'), 
(78, 79, '37.484', '127.011', '37.480', '127.012'), 
(73, 75, '37.494', '127.010', '37.495', '127.006'), 
(75, 76, '37.495', '127.006', '37.491','127.007'), 
(73, 74, '37.494', '127.010','37.492', '127.011'), 
(74, 76, '37.492', '127.011', '37.491','127.007'), 
(76, 77,'37.491','127.007', '37.486', '127.009'), 
(83, 84, '37.482', '127.004','37.477', '127.006'),
(78, 83, '37.484', '127.011', '37.482', '127.004'), 
(82, 83,'37.490', '127.004','37.482', '127.004'), 
(82, 90, '127.004','37.482', '37.487', '126.993'), 
(79, 84, '37.480', '127.012', '37.477', '127.006'),
(84, 92,'37.477', '127.006', '37.474','127.001'), 
(91, 92, '37.481',' 126.997', '37.474','127.001'), 
(83, 91, '37.482', '127.004', '37.474','127.001'), 
(81, 82, '37.494', '126.997','37.490', '127.004'),
(80, 81, '37.499', '126.998','37.482', '127.004'), 
(80, 87, '37.499', '126.998', '37.498', '126.987'), 
(87, 86, '37.498', '126.987', '37.499', '126.985'), 
(87, 89, '37.498', '126.987', '37.487', '126.993'), 
(86,93, '37.499', '126.985', '37.487', '126.993'), 
(86, 96, '37.487', '126.993', '37.485', '126.982'), 
(81, 89, '37.482', '127.004', '37.487', '126.993'), 
(89, 90, '37.487', '126.993', '37.487', '126.993'),
(89, 93, '37.487', '126.993', '37.487', '126.993'), 
(93, 94, '37.487', '126.993', '37.489', '126.987'), 
(93, 96, '37.489', '126.987', '37.485', '126.982'), 
(94, 95, '37.489', '126.987', '37.486', '126.989'),
(94, 88, '37.489', '126.987', '37.488', '126.985'), 
(90, 95, '37.487', '126.993', '37.486', '126.989'), 
(95, 98, '37.486', '126.989', '37.480', '126.993'), 
(90, 95, '37.487', '126.993','37.480',' 126.993'),
(90, 91, '37.487', '126.993','37.481',' 126.997'), 
(91, 98, '37.481',' 126.997', '37.480', '126.993'), 
(98, 99, '37.480', '126.993', '37.478', '126.989'), 
(80, 97, '37.499', '126.998', '37.485', '126.986'),
(80, 100, '37.499', '126.998', '37.485', '126.983'), 
(95, 97, '37.486', '126.989', '37.485', '126.986'), 
(97, 99, '37.485', '126.986', '37.478', '126.989'), 
(99, 103, '37.478', '126.989', '37.475', '126.985'),
(92, 103, '37.474','127.001', '37.475', '126.985'), 
(103, 102, '37.476','126.981', '37.475', '126.985'),
(96, 101, '37.485', '126.982', '37.485', '126.981'), 
(100, 101, '37.485', '126.983','37.485', '126.981'),
(101, 102, '37.485', '126.981', '37.475', '126.985')
]

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

import sqlite3

def create_db() :
    try :
        con = sqlite3.connect(db_name)
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS RSU (link_id INTEGER PRIMARY KEY AUTOINCREMENT, start INTEGER, end INTEGER, start_latitude TEXT, start_longitude TEXT, end_latitude TEXT, end_longitude TEXT)")
        # Create NearRSU table
        cur.execute("CREATE TABLE IF NOT EXISTS NearRSU (rsu_id INTEGER PRIMARY KEY, near_rsu TEXT)")
        # Create RSUState table
        cur.execute("CREATE TABLE IF NOT EXISTS RSUState (state_id INTEGER PRIMARY KEY AUTOINCREMENT, start_rsu INTEGER, end_rsu INTEGER, accident_type INTEGER, accident_size INTEGER)")
        # Create OBU table
        cur.execute("CREATE TABLE IF NOT EXISTS OBU (obu_id INTEGER PRIMARY KEY, path TEXT)")
        print('Create_db success================')
    except Exception as e :
        print(e)
        print('Create_db failed================')
    finally :
        con.close()

def insert_RSU(links) :# TEST
    global near
    try :
        con = sqlite3.connect(db_name)
        cur = con.cursor()
        # insert obu db part
        cur.executemany("INSERT INTO RSU (start, end, start_latitude, start_longitude, end_latitude, end_longitude) VALUES (?, ?, ?, ?, ?, ?);", links)
        # inset rsu db part
        near_rsu = near.keys
        for i in near_rsu:
            rsu = near[i][1:-1] # 앞과 뒤에 []를 제거
            cur.execute(f'INSERT INTO NearRSU (rsu_id, near_rsu) VALUES (?, ?);', (i, rsu)) 
        con.commit()
        print('insert_OBU success================')
    except Exception as e :
        print(e)
        print('insert_OBU failed================')
    finally :
        con.close()

create_db()
insert_RSU(links)