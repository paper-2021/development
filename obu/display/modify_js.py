route = ""

def init_map():
    route = ""

def modify_html(situation, data):
    """ # NOTE
    data
    situation : false -> [obu_loc, start_loc, end_loc, end_next_loc]
    situation : true  -> [obu_loc, start_loc, end_loc, , end_next_loc, imagename]
    """
    js_file = ''
    global route
    route += """new Tmapv2.LatLng("""+data[1]+ """),
            new Tmapv2.LatLng(""" + data[2] + """),
            """
    next_route = """new Tmapv2.LatLng(""" + data[3] + """),"""
    if(situation):
        js_file = """var map, marker;

function initTmap(){
    var map = new Tmapv2.Map("map_div",  
    {
        center: new Tmapv2.LatLng(37.510, 127.043), 
        width: "800px", 
        height: "500px",
        zoom: 13
    });
    var rsu = new Tmapv2.Marker({
        position: new Tmapv2.LatLng(""" + data[2]+ """),
        icon: "images/page_1/rsu.png", 
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
    document.getElementById("u4_png").src = " """+ data[4]+ """ ";
} 
        """
        html_file = """<!DOCTYPE html>
<html>
  <head>
    <title>simpleMap</title>
    <meta http-equiv="X-UA-Compatible" content="IE=edge"/>
    <meta http-equiv="content-type" content="text/html; charset=utf-8"/>
    <link href="css/axure_rp_page.css" type="text/css" rel="stylesheet"/>
    <link href="css/styles.css" type="text/css" rel="stylesheet"/>
    <script src="https://apis.openapi.sk.com/tmap/jsv2?version=1&appKey=l7xxd8dfb80c3b8d4c70ba275b4615276f7b"></script>
    <script>"""+js_file+"""	</script>
  </head>
  <body onload="initTmap()">
    <div id="base" class="">
      <!-- Unnamed (Rectangle) -->
      <div id="u0" class="ax_default box_1">
        <div id="u0_div" class=""></div>
        <div id="map_div"></div> 
        <div id="u0_text" class="text " style="display:none; visibility: hidden">
          <p></p>
        </div>
      </div>

      <!-- Notification (Group) -->
      <div id="u1" class="ax_default" data-label="Notification" data-left="1117" data-top="17" data-width="351" data-height="293">

        <!-- Back (Rectangle) -->
        <div id="u2" class="ax_default shape" data-label="Back">
          <img id="u2_img" class="img " src="display/images/page_1/back_u2.svg"/>
          <div id="u2_text" class="text " style="display:none; visibility: hidden">
            <p></p>
          </div>
        </div>

        <!-- Background (Rectangle) -->
        <div id="u3" class="ax_default shape" data-label="Background">
          <div id="u3_div" class=""></div>
          <div id="u3_text" class="text " style="display:none; visibility: hidden">
            <p></p>
          </div>
        </div>
        <!-- Big Picture (Rectangle) -->
        <div id="u4" class="ax_default shape" data-label="Big Picture">
          <img id="u4_png" src="display/images/page_1/u4_div.png" width="323" height="218"/>
          <div id="u4_div" class=""></div>
          <div id="u4_text" class="text " style="display:none; visibility: hidden">
            <p></p>
          </div>
        </div>
        <!-- Title (Rectangle) -->
        <div id="u5" class="ax_default shape" data-label="Title">
          <div id="u5_div" class=""></div>
          <div id="u5_text" class="text ">
            <p><span >RSU</span></p>
          </div>
        </div>
      </div>
    </div>
  </body>
</html>


"""
    else:
        js_file = """
var map, marker;
function initTmap(){
    var map = new Tmapv2.Map("map_div",  
    {
        center: new Tmapv2.LatLng(37.510, 127.043), 
        width: "800px", 
        height: "500px",
        zoom: 13
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
        position: new Tmapv2.LatLng("""+data[0]+""" ),
        icon: "display/images/page_1/car.png", 
        map: map 
    });
}
"""
        html_file = """<!DOCTYPE html>
<html>
  <head>
    <title>simpleMap</title>
    <meta http-equiv="X-UA-Compatible" content="IE=edge"/>
    <meta http-equiv="content-type" content="text/html; charset=utf-8"/>
    <link href="css/axure_rp_page.css" type="text/css" rel="stylesheet"/>
    <link href="css/styles.css" type="text/css" rel="stylesheet"/>
    <script src="https://apis.openapi.sk.com/tmap/jsv2?version=1&appKey=l7xxd8dfb80c3b8d4c70ba275b4615276f7b"></script>
    <script>"""+js_file+	"""</script>
  </head>
  <body onload="initTmap()">
    <div id="base" class="">
      <!-- Unnamed (Rectangle) -->
      <div id="u0" class="ax_default box_1">
        <div id="u0_div" class=""></div>
        <div id="map_div"></div> 
        <div id="u0_text" class="text " style="display:none; visibility: hidden">
          <p></p>
        </div>
      </div>
    </div>
  </body>
</html>

"""
    return html_file
