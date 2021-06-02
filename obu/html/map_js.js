
var map, marker;
function initTmap(){
    var map = new Tmapv2.Map("map_div",  
    {
        center: new Tmapv2.LatLng(37.261851,127.031121), // ������û�� �߽�����
        width: "1500px", 
        height: "700px",
        zoom: 16
    });
    //��� �׷��ֱ�, ȭ��ǥ����� �������� �غ��� 45����
    var polyline = new Tmapv2.Polyline({
        path: [
            new Tmapv2.LatLng(37.262338, 127.029050),            
            new Tmapv2.LatLng(37.261621, 127.031807),
        ],
        strokeColor: "#dd00dd", // ���� ����
		strokeWeight: 6, // ���� �β�
		draggable: true, //�巡�� ����
		strokeStyle:'dot', // ���� ���� soild, dash,
		outline: true, // �ܰ� ���� ����
		outlineColor:'#ffffff', // �ܰ� �� ����
		map: map // ���� ��ü
    });
} 
        