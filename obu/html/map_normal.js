var map, marker;

function initTmap(){
    var map = new Tmapv2.Map("map_div",  
    {
        center: new Tmapv2.LatLng(37.261851,127.031121), // 수원시청을 중심으로
        width: "1500px", 
        height: "700px",
        zoom: 16
    });

    //경로 그려주기, 화살표만들기 가능한지 해보기 45도로
    var polyline = new Tmapv2.Polyline({
        path: [
            new Tmapv2.LatLng(37.262338, 127.029050), // 선의 꼭짓점 좌표
            new Tmapv2.LatLng(37.261621, 127.031807), // 선의 꼭짓점 좌표
        ],
        strokeColor: "#dd00dd", // 라인 색상
		strokeWeight: 6, // 라인 두께
		draggable: true, //드래그 여부
		strokeStyle:'dot', // 선의 종류 soild, dash,
		outline: true, // 외각 선을 설정
		outlineColor:'#ffffff', // 외각 선 색상
		map: map // 지도 객체
    });
} 