var map, marker;

function initTmap(){
    var map = new Tmapv2.Map("map_div",  
    {
        center: new Tmapv2.LatLng(37.261851,127.031121), // 수원시청을 중심으로
        width: "1500px", 
        height: "700px",
        zoom: 16
    });
    // 마커 생성, 마커 이미지 유진이랑 상의하고 바꾸기
    var rsu = new Tmapv2.Marker({
        position: new Tmapv2.LatLng(37.261851,127.031121), //Marker의 중심좌표 설정, rsu_ip 가 들어가도록 하게 하기
        map: map //Marker가 표시될 Map 설정..
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

    document.getElementById("u4_img").src = 'images/page_1/u4_div.png';

} 