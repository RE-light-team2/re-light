var localStream = null;
var peer = null;
var existingCall = null;
var conn;
let cus_cnt_set = 0;
let shop_cnt_set = 0;
let pinned_cnt = 0;

const localVideo = document.getElementById('my-video');
const ChatVideo = document.getElementById('their-video');
//マイク・カメラOFF・ON切り替えボタン用スクリプト
const toggleCamera = document.getElementById('js-toggle-camera');
const toggleMicrophone = document.getElementById('js-toggle-microphone');
const cameraStatus = document.getElementById('camera-status');
const microphoneStatus = document.getElementById('microphone-status');

localVideo.muted = true; // 自分の音声を自分のスピーカーから聞こえなくする。相手には届く。
localVideo.playsInline = true;
localVideo.autoplay = true;

ChatVideo.playsInline = true;
ChatVideo.autoplay = true;

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function pageout() {
    var csrf_token = getCookie("csrftoken");
    $.ajax({
        type: "POST", //post data
        data: { 'data': "end" }, //if you want to send any data to view
        url: document.form1.action, // your url that u write in action in form tag
        scriptCharset: 'utf-8',
        contentType: "application/json",
        beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrf_token);
                }
        },
    });
}

function pagein() {
    var call = "call"
    var csrf_token = getCookie("csrftoken");
    $.ajax({
        type:"POST", //post data
        data:{'data': call }, //if you want to send any data to view
        contentType: "application/json",
        url: document.form1.action, // your url that u write in action in form tag   
        beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrf_token);
                }
        },
    })
}

$(document).ready(function () {
    $('#end-call').hide();

    $("#chat-message-submit").click(function() {
        // 送信テキストの取得
        var message = $("#chat-message-input").val();
 
        // 送信
        conn.send(message);

        var event = $('#event_name').text(); 
        var name = (peer.id).replace(event,"");

        var cnt = Number(shop_cnt_set);
        var html = '<div id="shop_message'+ cnt +'">' + name + ": " + message + '<button type="button" value="pin'+cnt+'" class="pin-btn-shop">ピン</button></div>';
        shop_cnt_set += 1;
        $("#your_messages").prepend(html);
 
        // 送信テキストボックスをクリア
        $("#chat-message-input").val("");
    });

    $(document).on('click', '.pin-btn-shop', function () {
        var tmp = $(this).val();
        var num = tmp.replace('pin', '');
        var sent = "#shop_message" + num;
        var mess = $(sent).text();
        var message  = mess.slice(0, -2);
        var cnt = Number(pinned_cnt);
        pinned_cnt += 1;
        var html = '<div id="pinned'+ cnt +'">' + message + '<button type="button" value="rm'+cnt+'" class="pin-rm">ピンから削除</button></div>';   
        $("#pinned_messages").prepend(html);
    });

    $(document).on("click", "#end-call", function () {
        existingCall.close();
        conn.close();
    });

    toggleCamera.addEventListener('click', () => {
        const videoTracks = localStream.getVideoTracks()[0];
        videoTracks.enabled = !videoTracks.enabled;
        var color = `${videoTracks.enabled ? 'white' : 'red'}`;
        $('#js-toggle-camera').css({'background-color':color});
    });

    toggleMicrophone.addEventListener('click', () => {
        const audioTracks = localStream.getAudioTracks()[0];
        audioTracks.enabled = !audioTracks.enabled;
        var color = `${audioTracks.enabled ? 'white' : 'red'}`;
        $('#js-toggle-microphone').css({'background-color':color});
    });
});

navigator.mediaDevices.getUserMedia({video: true, audio: true})
    .then(function (stream) {
        // Success
        $('#my-video').get(0).srcObject = stream;
        localStream = stream;
    }).catch(function (error) {
        // Error
        console.error('mediaDevice.getUserMedia() error:', error);
        return;
});

peer = new Peer($('#my-id').text(),{
    key: '0dd47d22-8623-4292-84b2-8a7b3b800889',
    debug: 3
});

peer.on('connection', function(connection){
    conn = connection;
    // メッセージ受信イベントの設定
    conn.on("open", function() {
        // 相手のIDを表示する
        // - 相手のIDはconnectionオブジェクトのidプロパティに存在する
        console.log("Connection_id :" + conn.id);
    });
    conn.on("data", onRecvMessage);
});

function onRecvMessage(data) {
    // 画面に受信したメッセージを表示
    var cnt = Number(cus_cnt_set);
    var event = $('#event_name').text(); 
    var name = (existingCall.remoteId).replace(event, "");
    var html = '<div id="cus_message'+ cnt +'">' + name + ": " + data + '<button type="button" value="pin'+cnt+'" class="pin-btn-cus">ピン</button></div>';
    cus_cnt_set += 1;
    $("#other_messages").prepend(html);
} 

$(document).on('click', '.pin-rm', function () {
        var tmp = $(this).val();
        var num = tmp.replace('rm', '');
        var sent = "#pinned" + num;
        $(sent).remove();
        $(this).remove();
    });

$(document).on('click', '.pin-btn-cus', function () {
    var tmp = $(this).val();
    var num = tmp.replace('pin', '');
    var sent = "#cus_message" + num;
    var mess = $(sent).text();
    var message  = mess.slice(0, -2);
    var cnt = Number(pinned_cnt);
    pinned_cnt += 1;
    var html = '<div id="pinned'+ cnt +'">' + message + '<button type="button" value="rm'+cnt+'" class="pin-rm">ピンから削除</button></div>';   
    $("#pinned_messages").prepend(html);
});

peer.on('open', function(){
    $('#my-id').val(peer.id);
});

peer.on('error', function (err) {
    alert(err.message);
});

peer.on('close', function(){
    pageout();
});

peer.on('disconnected', function () {
    console.log("disconnect")
});

function addVideo(call,stream){
    $('#their-video').get(0).srcObject = stream;
}

function removeVideo(peerId) {
    $('#' + peerId).remove();
}

function setupCallEventHandlers(call){
    if (existingCall) {
        existingCall.close();
    };
    
    existingCall = call;
    var event = $('#event_name').text(); 
    var name = (existingCall.remoteId).replace(event, "");
    var urls = "/ajax/" + name; 
    $.ajax({
        type: "GET", // GETメソッドで通信 
        url: urls, // 取得先のURL 
        cache: false, // キャッシュしないで読み込み 
        // 通信成功時に呼び出されるコールバック
        success: function (data) {
            $('#cus_profile').html(data); 
        },
        // 通信エラー時に呼び出されるコールバック
        error: function () {
            alert("Ajax通信エラー");
        }
    });
    call.on('stream', function(stream){
        addVideo(call, stream);
        pagein();
        $('#cus_profile').show();
        $('#end-call').show(); 
        $('#my-video').css({'width':'150px','float':'right'});
        $('#their-video').css({'width':'800px','float':'left','border':'2px solid black','border-radius': '10px'});
        $('#cus_profile').css({ 'width': '400px', 'float': 'right', 'border': '2px solid yellow', 'border-radius': '10px', 'text-align': 'center' });   
    });

    call.on('close', function(){
        removeVideo(call.remoteId);
        $('#cus_profile').hide();
    });
}

peer.on('call', function(call){
    call.answer(localStream);
    setupCallEventHandlers(call);
});
$('#detail_cus').hide();
$('#cus_profile').hover(
    function() {        
        //マウスカーソルが重なった時の処理
        $('#detail_cus').show();
        $('#cus_profile').css('background-color', 'white');      
    },
    function() {       
        //マウスカーソルが離れた時の処理
        $('#detail_cus').hide();
        $('#cus_profile').css('background-color', '');     
    }
);