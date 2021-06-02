var map, marker;
document.getElementById("u4_img").src = "http://3.35.184.173:8000/upload/3/20210507212215_3_accident.jpg";
function initTmap(){
    var map = new Tmapv2.Map("map_div",  
    {
        center: new Tmapv2.LatLng(37.495, 127.021), 
        width: "1500px", 
        height: "700px",
        zoom: 14
    });
    
    var polyline = new Tmapv2.Polyline({
        path: [new Tmapv2.LatLng(37.518, 127.050),
            new Tmapv2.LatLng(37.513, 127.053)
        ],
        strokeColor: "#dd00dd",
		strokeWeight: 6,
		draggable: true, 
		strokeStyle:'dot', 
		outline: true,
		outlineColor:'#ffffff',
		map: map 
    });

    var car = new Tmapv2.Marker({
        position: new Tmapv2.LatLng('37.518, 127.050'),
        icon: "images/page_1/car.png", 
        map: map 
    });
} 

