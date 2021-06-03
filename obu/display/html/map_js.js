
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
        path: [new Tmapv2.LatLng(37.499, 126.998),
            new Tmapv2.LatLng(37.494, 126.997),],
        strokeColor: "#dd00dd",
		strokeWeight: 6,
		draggable: true, 
		strokeStyle:'dot', 
		outline: true,
		outlineColor:'#ffffff',
		map: map 
    });

    var car = new Tmapv2.Marker({
        position: new Tmapv2.LatLng(" 37.518, 127.050 "),
        icon: "images/page_1/car.png", 
        map: map 
    });
} 
