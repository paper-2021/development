from .Astar import Node

def change_branch(start, end, traffic) :
    try :
        start.changeBranch(traffic, end)
        return True
    except Exception as e :
        print(e) 
        return False

def find_path(start, end) :
    result = start.aStar(start, end)
    return start.printPath(result)

def call_astar() :
    n1 = Node(37.524, 127.053)
    n2 = Node(37.519, 127.056)
    n3 = Node(37.514, 127.060)
    n4 = Node(37.508, 127.062)
    n5 = Node(37.505, 127.064)
    n6 = Node(37.501, 127.067)
    n7 = Node(37.496, 127.069)
    n8 = Node(37.524, 127.047)
    n9 = Node(37.518, 127.050)
    n10 = Node(37.513, 127.053)
    n11 = Node(37.506, 127.056)
    n12 = Node(37.503, 127.058)
    n13 = Node(37.198, 127.061)
    n14 = Node(37.494, 127.063)
    n15 = Node(37.523, 127.039)
    n16 = Node(37.517, 127.041)
    n17 = Node(37.510, 127.043)
    n18 = Node(37.504, 127.048)
    n19 = Node(37.500, 127.050)
    n20 = Node(37.496, 127.052)
    n21 = Node(37.490, 127.055)
    n22 = Node(37.521, 127.033)
    n23 = Node(37.515, 127.035)
    n24 = Node(37.508, 127.038)
    n25 = Node(37.502, 127.042)
    n26 = Node(37.498, 127.044)
    n27 = Node(37.494, 127.046)
    n28 = Node(37.488, 127.049)
    n29 = Node(37.519, 127.028)
    n30 = Node(37.514, 127.030)
    n31 = Node(37.507, 127.033)
    n32 = Node(37.500, 127.036)
    n33 = Node(37.495, 127.039)
    n34 = Node(37.492, 127.040)
    n35 = Node(37.485, 127.041)
    n36 = Node(37.516, 127.019)
    n37 = Node(37.511, 127.021)
    n38 = Node(37.517, 127.023)
    n39 = Node(37.504, 127.024)
    n40 = Node(37.498, 127.031)
    n41 = Node(37.494, 127.033)
    n42 = Node(37.490, 127.035)
    n43 = Node(37.497, 127.027)
    n44 = Node(37.492, 127.029)
    n45 = Node(37.489, 127.031)
    n46 = Node(37.484, 127.034)
    n47 = Node(37.514, 127.015)
    n48 = Node(37.509, 127.016)
    n49 = Node(37.503, 127.021)
    n50 = Node(37.496, 127.024)
    n51 = Node(37.492, 127.026)
    n52 = Node(37.488, 127.028)
    n53 = Node(37.483, 127.029)
    n54 = Node(37.502, 127.018)
    n55 = Node(37.495, 127.021)
    n56 = Node(37.490, 127.023)
    n57 = Node(37.487, 127.024)
    n58 = Node(37.483, 127.025)
    n59 = Node(37.514, 127.007)
    n60 = Node(37.508, 127.011)
    n61 = Node(37.512, 127.006)
    n62 = Node(37.507, 127.008)
    n63 = Node(37.504, 127.010)
    n64 = Node(37.495, 127.012)
    n65 = Node(37.493, 127.013)
    n66 = Node(37.488, 127.014)
    n67 = Node(37.484, 127.016)
    n68 = Node(37.482, 127.018)
    n69 = Node(37.509, 127.002)
    n70 = Node(37.505, 127.004)
    n71 = Node(37.505, 127.000)
    n72 = Node(37.501, 127.003)
    n73 = Node(37.494, 127.010)
    n74 = Node(37.492, 127.011)
    n75 = Node(37.495, 127.006)
    n76 = Node(37.491, 127.007)
    n77 = Node(37.486, 127.009)
    n78 = Node(37.484, 127.011)
    n79 = Node(37.480, 127.012)
    n80 = Node(37.499, 126.998)
    n81 = Node(37.494, 126.997)
    n82 = Node(37.490, 127.004)
    n83 = Node(37.482, 127.004)
    n84 = Node(37.477, 127.006)
    n85 = Node(37.501, 126.956)
    n86 = Node(37.499, 126.985)
    n87 = Node(37.498, 126.987)
    n88 = Node(37.488, 126.985)
    n89 = Node(37.487, 126.993)
    n90 = Node(37.487, 126.993)
    n91 = Node(37.481, 126.997)
    n92 = Node(37.474, 127.001)
    n93 = Node(37.487, 126.993)
    n94 = Node(37.489, 126.987)
    n95 = Node(37.486, 126.989)
    n96 = Node(37.485, 126.982)
    n97 = Node(37.485, 126.986)
    n98 = Node(37.480, 126.993)
    n99 = Node(37.478, 126.989)
    n100 = Node(37.485, 126.983)
    n101 = Node(37.485, 126.981)
    n102 = Node(37.476, 126.981)
    n103 = Node(37.475, 126.985)

    n1.addBranch(578, 60, n2)
    n1.addBranch(629, 60, n8)

    n2.addBranch(578, 60, n1)
    n2.addBranch(678, 60, n3)
    n2.addBranch(539, 60, n9)

    n3.addBranch(678, 60, n2)
    n3.addBranch(687, 60, n4)
    n3.addBranch(570, 60, n10)

    n4.addBranch(687, 60, n3)
    n4.addBranch(421, 60, n5)
    n4.addBranch(617, 60, n11)

    n5.addBranch(421, 60, n4)
    n5.addBranch(535, 60, n6)
    n5.addBranch(591, 60, n12)

    n6.addBranch(535, 60, n5)
    n6.addBranch(528, 60, n7)
    n6.addBranch(592, 60, n13)

    n7.addBranch(528, 60, n6)
    n7.addBranch(614, 60, n14)

    n8.addBranch(629, 60, n1)
    n8.addBranch(618, 60, n9)
    n8.addBranch(759, 60, n15)

    n9.addBranch(539, 60, n2)
    n9.addBranch(618, 60, n8)
    n9.addBranch(667, 60, n10)
    n9.addBranch(775, 60, n16)

    n10.addBranch(570, 60, n3)
    n10.addBranch(667, 60, n9)
    n10.addBranch(705, 60, n11)
    n10.addBranch(840, 60, n17)

    n11.addBranch(617, 60, n4)
    n11.addBranch(705, 60, n10)
    n11.addBranch(421, 60, n12)
    n11.addBranch(687, 60, n18)

    n12.addBranch(591, 60, n5)
    n12.addBranch(421, 60, n11)
    n12.addBranch(481, 60, n13)
    n12.addBranch(733, 60, n19)

    n13.addBranch(592, 60, n6)
    n13.addBranch(481, 60, n12)
    n13.addBranch(553, 60, n14)
    n13.addBranch(736, 60, n20)

    n14.addBranch(614, 60, n7)
    n14.addBranch(553, 60, n13)
    n14.addBranch(801, 60, n21)

    n15.addBranch(759, 10, n8)
    n15.addBranch(707, 60, n16)
    n15.addBranch(548, 60, n22)

    n16.addBranch(775, 60, n9)
    n16.addBranch(707, 60, n15)
    n16.addBranch(817, 60, n17)
    n16.addBranch(509, 60, n23)

    n17.addBranch(840, 60, n10)
    n17.addBranch(817, 60, n16)
    n17.addBranch(850, 60, n18)
    n17.addBranch(463, 60, n24)

    n18.addBranch(687, 60, n11)
    n18.addBranch(850, 60, n17)
    n18.addBranch(467, 60, n19)
    n18.addBranch(556, 60, n25)

    n19.addBranch(733, 60, n12)
    n19.addBranch(467, 60, n18)
    n19.addBranch(568, 60, n26)
    n19.addBranch(492, 60, n20)

    n20.addBranch(736, 60, n13)
    n20.addBranch(492, 60, n19)
    n20.addBranch(576, 60, n21)
    n20.addBranch(570, 60, n27)

    n21.addBranch(801, 60, n14)
    n21.addBranch(576, 60, n20)
    n21.addBranch(559, 60, n28)

    n22.addBranch(548, 60, n15)
    n22.addBranch(644, 60, n23)
    n22.addBranch(589, 60, n29)

    n23.addBranch(509, 60, n16)
    n23.addBranch(644, 60, n22)
    n23.addBranch(793, 60, n24)
    n23.addBranch(409, 60, n30)

    n24.addBranch(463, 60, n17)
    n24.addBranch(793, 60, n23)
    n24.addBranch(739, 60, n25)
    n24.addBranch(393, 60, n31)

    n25.addBranch(556, 60, n18)
    n25.addBranch(739, 60, n24)
    n25.addBranch(433, 60, n26)
    n25.addBranch(517, 60, n32)

    n26.addBranch(568, 60, n19)
    n26.addBranch(433, 60, n25)
    n26.addBranch(473, 60, n27)
    n26.addBranch(553, 60, n33)

    n27.addBranch(570, 60, n20)
    n27.addBranch(473, 60, n26)
    n27.addBranch(656, 60, n28)
    n27.addBranch(509, 60, n34)

    n28.addBranch(559, 60, n21)
    n28.addBranch(656, 60, n27)
    n28.addBranch(789, 60, n35)

    n29.addBranch(589, 60, n22)
    n29.addBranch(650, 60, n30)
    n29.addBranch(421, 60, n38)

    n30.addBranch(409, 60, n23)
    n30.addBranch(650, 60, n29)
    n30.addBranch(808, 60, n31)
    n30.addBranch(843, 60, n37)

    n31.addBranch(393, 60, n24)
    n31.addBranch(808, 60, n30)
    n31.addBranch(731, 60, n32)
    n31.addBranch(833, 60, n39)

    n32.addBranch(517, 60, n25)
    n32.addBranch(731, 60, n31)
    n32.addBranch(585, 60, n33)
    n32.addBranch(544, 60, n40)

    n33.addBranch(553, 60, n26)
    n33.addBranch(585, 60, n32)
    n33.addBranch(377, 60, n34)
    n33.addBranch(555, 60, n41)

    n34.addBranch(509, 60, n27)
    n34.addBranch(377, 60, n33)
    n34.addBranch(789, 60, n35)
    n34.addBranch(521, 60, n42)

    n35.addBranch(789, 60, n28)
    n35.addBranch(789, 60, n34)
    n35.addBranch(720, 60, n46)

    n36.addBranch(553, 60, n37)
    n36.addBranch(335, 60, n38)
    n36.addBranch(332, 60, n47)

    n37.addBranch(843, 60, n30)
    n37.addBranch(553, 60, n36)
    n37.addBranch(756, 60, n39)
    n37.addBranch(447, 60, n48)

    n38.addBranch(421, 60, n29)
    n38.addBranch(335, 60, n36)

    n39.addBranch(833, 60, n31)
    n39.addBranch(756, 60, n37)
    n39.addBranch(703, 60, n43)
    n39.addBranch(327, 60, n49)

    n40.addBranch(547, 60, n41)
    n40.addBranch(275, 60, n43)
    n40.addBranch(544, 60, n32)

    n41.addBranch(555, 60, n33)
    n41.addBranch(547, 60, n40)
    n41.addBranch(372, 60, n42)
    n41.addBranch(281, 60, n44)

    n42.addBranch(521, 60, n34)
    n42.addBranch(372, 60, n41)
    n42.addBranch(273, 60, n45)

    n43.addBranch(703, 60, n39)
    n43.addBranch(275, 60, n40)
    n43.addBranch(604, 60, n44)
    n43.addBranch(272, 60, n50)

    n44.addBranch(281, 60, n41)
    n44.addBranch(604, 60, n43)
    n44.addBranch(374, 60, n45)
    n44.addBranch(297, 60, n51)

    n45.addBranch(273, 60, n42)
    n45.addBranch(374, 60, n44)
    n45.addBranch(579, 60, n46)
    n45.addBranch(288, 60, n52)

    n46.addBranch(720, 60, n35)
    n46.addBranch(579, 60, n45)
    n46.addBranch(350, 60, n53)

    n47.addBranch(332, 60, n36)
    n47.addBranch(545, 60, n48)

    n48.addBranch(447, 60, n37)
    n48.addBranch(545, 60, n47)
    n48.addBranch(712, 60, n54)
    n48.addBranch(418, 60, n60)

    n49.addBranch(327, 60, n39)
    n49.addBranch(233, 60, n54)
    n49.addBranch(768, 60, n50)

    n50.addBranch(272, 60, n43)
    n50.addBranch(768, 60, n49)
    n50.addBranch(568, 60, n51)
    n50.addBranch(669, 60, n55)

    n51.addBranch(297, 60, n44)
    n51.addBranch(568, 60, n50)
    n51.addBranch(387, 60, n52)
    n51.addBranch(358, 60, n56)

    n52.addBranch(288, 60, n45)
    n52.addBranch(387, 60, n51)
    n52.addBranch(505, 60, n53)
    n52.addBranch(404, 60, n57)

    n53.addBranch(350, 60, n46)
    n53.addBranch(505, 60, n52)
    n53.addBranch(406, 60, n58)

    n54.addBranch(712, 60, n48)
    n54.addBranch(233, 60, n49)
    n54.addBranch(1000, 60, n55)
    n54.addBranch(908, 60, n63)

    n55.addBranch(669, 60, n50)
    n55.addBranch(1000, 60, n54)
    n55.addBranch(704, 60, n56)
    n55.addBranch(778, 60, n65)

    n56.addBranch(358, 60, n51)
    n56.addBranch(704, 60, n55)
    n56.addBranch(1100, 60, n57)
    n56.addBranch(846, 60, n66)

    n57.addBranch(404, 60, n52)
    n57.addBranch(1100, 60, n56)
    n57.addBranch(704, 60, n58)
    n57.addBranch(807, 60, n67)

    n58.addBranch(406, 60, n53)
    n58.addBranch(704, 60, n57)
    n58.addBranch(748, 60, n68)

    n59.addBranch(529, 60, n60)
    n59.addBranch(294, 60, n61)

    n60.addBranch(418, 60, n48)
    n60.addBranch(529, 60, n59)
    n60.addBranch(316, 60, n62)

    n61.addBranch(294, 60, n59)
    n61.addBranch(612, 60, n62)
    n61.addBranch(489, 60, n69)

    n62.addBranch(316, 60, n60)
    n62.addBranch(612, 60, n61)
    n62.addBranch(394, 60, n63)
    n62.addBranch(566, 60, n70)

    n63.addBranch(394, 60, n62)
    n63.addBranch(1100, 60, n64)
    n63.addBranch(792, 60, n72) 
    n63.addBranch(908, 60, n54)

    n64.addBranch(1100, 60, n63)
    n64.addBranch(354, 60, n65)
    n64.addBranch(303, 60, n73)

    n65.addBranch(778, 60, n55)
    n65.addBranch(354, 60, n64)
    n65.addBranch(606, 60, n66)
    n65.addBranch(305, 60, n74)

    n66.addBranch(846, 60, n56)
    n66.addBranch(606, 60, n65)
    n66.addBranch(438, 60, n67)
    n66.addBranch(499, 60, n77)

    n67.addBranch(807, 60, n57)
    n67.addBranch(438, 60, n66)
    n67.addBranch(457, 60, n68)
    n67.addBranch(469, 60, n78)

    n68.addBranch(748, 60, n58)
    n68.addBranch(457, 60, n67)
    n68.addBranch(516, 60, n79)

    n69.addBranch(489, 60, n61)
    n69.addBranch(323, 60, n70)

    n70.addBranch(566, 60, n62)
    n70.addBranch(323, 60, n69)
    n70.addBranch(335, 60, n71)

    n71.addBranch(1300, 60, n85)
    n71.addBranch(335, 60, n70)
    n71.addBranch(527, 60, n72)

    n72.addBranch(792, 60, n63)
    n72.addBranch(527, 60, n71)
    n72.addBranch(817, 60, n80)

    n73.addBranch(303, 60, n64)
    n73.addBranch(420, 60, n74)
    n73.addBranch(482, 60, n75)

    n74.addBranch(305, 60, n65)
    n74.addBranch(420, 60, n73)
    n74.addBranch(380, 60, n76)

    n75.addBranch(482, 60, n73)
    n75.addBranch(257, 60, n76)

    n76.addBranch(380, 60, n74)
    n76.addBranch(257, 60, n75)
    n76.addBranch(644, 60, n77)
    n76.addBranch(328, 60, n82)

    n77.addBranch(499, 60, n66)
    n77.addBranch(644, 60, n76)
    n77.addBranch(357, 60, n78)

    n78.addBranch(469, 60, n67)
    n78.addBranch(357, 60, n77)
    n78.addBranch(526, 60, n79)
    n78.addBranch(680, 60, n83)

    n79.addBranch(516, 60, n68)
    n79.addBranch(526, 60, n78)
    n79.addBranch(741, 60, n84)

    n80.addBranch(817, 60, n72)
    n80.addBranch(545, 60, n81)
    n80.addBranch(894, 60, n87)

    n81.addBranch(545, 60, n80)
    n81.addBranch(856, 60, n82)
    n81.addBranch(783, 60, n89)

    n82.addBranch(328, 60, n76)
    n82.addBranch(856, 60, n81)
    n82.addBranch(948, 60, n83)
    n82.addBranch(1100, 60, n90)

    n83.addBranch(680, 60, n78)
    n83.addBranch(948, 60, n82)
    n83.addBranch(669, 60, n84)
    n83.addBranch(713, 60, n91)

    n84.addBranch(741, 60, n79)
    n84.addBranch(669, 60, n83)
    n84.addBranch(584, 60, n92)

    n85.addBranch(1300, 60, n71)
    n85.addBranch(162, 60, n86)

    n86.addBranch(162, 60, n85)
    n86.addBranch(240, 60, n87)
    n86.addBranch(804, 60, n96)

    n87.addBranch(894, 60, n80)
    n87.addBranch(240, 60, n86)
    n87.addBranch(785, 60, n87)

    n88.addBranch(114, 60, n94)
    n88.addBranch(240, 60, n97)
    n88.addBranch(367, 60, n100)

    n89.addBranch(783, 60, n81)
    n89.addBranch(785, 60, n87)
    n89.addBranch(664, 60, n90)
    n89.addBranch(353, 60, n93)

    n90.addBranch(1100, 60, n82)
    n90.addBranch(664, 60, n89)
    n90.addBranch(825, 60, n91)
    n90.addBranch(411, 60, n95)

    n91.addBranch(713, 60, n83)
    n91.addBranch(825, 60, n90)
    n91.addBranch(853, 60, n92)
    n91.addBranch(453, 60, n98)

    n92.addBranch(586, 60, n84)
    n92.addBranch(853, 60, n91)
    n92.addBranch(1600, 60, n102)

    n93.addBranch(353, 60, n89)
    n93.addBranch(224, 60, n94)
    n93.addBranch(472, 60, n96)

    n94.addBranch(224, 60, n93)
    n94.addBranch(378, 60, n95)
    n94.addBranch(114, 60, n88)

    n95.addBranch(411, 60, n90)
    n95.addBranch(378, 60, n94)
    n95.addBranch(355, 60, n97)
    n95.addBranch(781, 60, n98)

    n96.addBranch(804, 60, n86)
    n96.addBranch(472, 60, n93)
    n96.addBranch(654, 60, n101)

    n97.addBranch(240, 60, n88)
    n97.addBranch(355, 60, n95)
    n97.addBranch(1000, 60, n99)
    n97.addBranch(271, 60, n100)

    n98.addBranch(453, 60, n91)
    n98.addBranch(781, 60, n95)
    n98.addBranch(420, 60, n99)

    n99.addBranch(1000, 60, n97)
    n99.addBranch(420, 60, n98)
    n99.addBranch(496, 60, n103)

    n100.addBranch(367, 60, n93)
    n100.addBranch(281, 60, n97)
    n100.addBranch(236, 60, n101)
    n100.addBranch(1400, 60, n102)

    n101.addBranch(654, 60, n96)
    n101.addBranch(236, 60, n100)
    n101.addBranch(1100, 60, n102)

    n102.addBranch(1600, 60, n92)
    n102.addBranch(1400, 60, n100)
    n102.addBranch(1100, 60, n101)
    n102.addBranch(446, 60, n103)

    n103.addBranch(496, 60, n99)
    n103.addBranch(446, 60, n102)

    nodes = [n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, 
    n11, n12, n13, n14, n15, n16, n17, n18, n19, n20, 
    n21, n22, n23, n24, n25, n26, n27, n28, n29, n30, 
    n31, n32, n33, n34, n35, n36, n37, n38, n39, n40, 
    n41, n42, n43, n44, n45, n46, n47, n48, n49, n50, 
    n51, n52, n53, n54, n55, n56, n57, n58, n59, n60, 
    n61, n62, n63, n64, n65, n66, n67, n68, n69, n70, 
    n71, n72, n73, n74, n75, n76, n77, n78, n79, n80, 
    n81, n82, n83, n84, n85, n86, n87, n88, n89, n90, 
    n91, n92, n93, n94, n95, n96, n97, n98, n99, n100, 
    n101, n102, n103]

    return nodes