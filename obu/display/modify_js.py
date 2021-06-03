route = ""
# modify_ html 으로 바꾸기
def modify_js(situation, data):
    """
    data
    situation : false -> [obu_loc, start_loc, end_loc]
    situation : true  -> [obu_loc, start_loc, end_loc, imagename]
    """
    js_file = ''
    global route
    route += """new Tmapv2.LatLng("""+data[1]+ """),
            new Tmapv2.LatLng(""" + data[2] + """),"""
    if(situation):
        js_file = """var map, marker;

function initTmap(){
    var map = new Tmapv2.Map("map_div",  
    {
        center: new Tmapv2.LatLng(37.495, 127.021), 
        width: "1500px", 
        height: "700px",
        zoom: 14
    });
    var rsu = new Tmapv2.Marker({
        position: new Tmapv2.LatLng(""" + data[2]+ """),
        map: map
    });
    var polyline = new Tmapv2.Polyline({
        path: [ """ + route + """        ],
        strokeColor: "#dd00dd",
		strokeWeight: 6,
		draggable: true, 
		strokeStyle:'dot', 
		outline: true,
		outlineColor:'#ffffff',
		map: map 
    });

    var car = new Tmapv2.Marker({
        position: new Tmapv2.LatLng("""+data[0]+"""),
        icon: "images/page_1/car.png", 
        map: map 
    });
    document.getElementById("u4_png").src = " """+ data[3]+ """ ";
} 



        """
    else:
        js_file = """
var map, marker;
function initTmap(){
    var map = new Tmapv2.Map("map_div",  
    {
        center: new Tmapv2.LatLng(37.495, 127.021), 
        width: "1500px", 
        height: "700px",
        zoom: 14
    });
    
    var polyline = new Tmapv2.Polyline({
        path: ["""+ route + """],
        strokeColor: "#dd00dd",
		strokeWeight: 6,
		draggable: true, 
		strokeStyle:'dot', 
		outline: true,
		outlineColor:'#ffffff',
		map: map 
    });

    var car = new Tmapv2.Marker({
        position: new Tmapv2.LatLng(" """+data[0]+""" "),
        icon: "images/page_1/car.png", 
        map: map 
    });
} 
"""
    return js_file

def init_map():
    route = ""