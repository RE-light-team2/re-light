var localStream = null;
var peer = null;
var existingCall = null;
var conn;  
let cus_cnt_set = 0;
let shop_cnt_set = 0;

const localVideo = document.getElementById('my-video');
const ChatVideo = document.getElementById('their-video');

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

$(document).ready(function () {
    window.addEventListener("unload", function () {
        var csrf_token = getCookie("csrftoken");
        var formData = new FormData();
        formData.append("data", "end");
        formData.append('csrfmiddlewaretoken', csrf_token);
        navigator.sendBeacon(document.form1.action, formData);
    });

    $(document).on("click", "#make-call", function (e) {   
        e.preventDefault();
        const call = peer.call($('#callto-id').text(), localStream);
        conn = peer.connect($('#callto-id').text());
        conn.on("data", onRecvMessage);
        setupCallEventHandlers(call);
    });

    $("#chat-message-submit").click(function() {
        // 送信テキストの取得
        var message = $("#chat-message-input").val();
 
        // 送信
        conn.send(message);

        var event = $('#event_name').text(); 
        var name = (peer.id).replace(event,"");
 
        var cnt = Number(cus_cnt_set);
        var html = '<div id="your_message'+ cnt +'">' + name + ": " + message + '</div><button type="button" value="pin'+cnt+'" class="pin-btn-cus">ピン</button>';
        cus_cnt_set += 1;
        $("#shop_messages").append(html);
 
        // 送信テキストボックスをクリア
        $("#chat-message-input").val("");
    });

    $(document).on('click', '.pin-btn-cus', function () {
        var tmp = $(this).val();
        var num = tmp.replace('ピン', '');
        var sent = "#your_message" + num;
        var mess = $(sent).text();
        $("#pinned_messages").append($("<p>").html(mess).css("font-weight", "bold"));
    });


    $(document).on("click", "#end-call", function () {
        pageout();
        existingCall.close();
        conn.close();
    });

    toggleCamera.addEventListener('click', () => {
        const videoTracks = localStream.getVideoTracks()[0];
        videoTracks.enabled = !videoTracks.enabled;
        cameraStatus.textContent = `カメラ${videoTracks.enabled ? 'ON' : 'OFF'}`;
    });

    toggleMicrophone.addEventListener('click', () => {
        const audioTracks = localStream.getAudioTracks()[0];
        audioTracks.enabled = !audioTracks.enabled;
        microphoneStatus.textContent = `マイク${audioTracks.enabled ? 'ON' : 'OFF'}`;
    });
});


navigator.mediaDevices.getUserMedia({
        video: true,
        audio: true
    })
    .then(function (stream) {
        // Success
        $('#my-video').get(0).srcObject = stream;
        localStream = stream;
    }).catch(function (error) {
        // Error
        console.error('mediaDevice.getUserMedia() error:', error);
        return;
    });

peer = new Peer($('#my-id').text(), {
    key: '0dd47d22-8623-4292-84b2-8a7b3b800889',
    debug: 3
});

function onRecvMessage(data) {
    // 画面に受信したメッセージを表示
    var cnt = Number(shop_cnt_set);
    var event = $('#event_name').text(); 
    var name = (existingCall.remoteId).replace(event, "");
    var html = '<div id="other_message'+ cnt +'">' + name + ": " + data + '</div><button type="button" value="pin'+cnt+'" class="pin-btn-shop">ピン'+cnt+'</button>';
    shop_cnt_set += 1;
    $("#shop_messages").append(html);
}

$(document).on('click', '.pin-btn-shop', function () {
    var tmp = $(this).text();
    var num = tmp.replace('ピン', '');
    var sent = "#other_message" + num;
    var mess = $(sent).text();
    $("#pinned_messages").append($("<p>").html(mess).css("font-weight", "bold"));
});

peer.on('connection', function(connection){
    // データ通信用に connectionオブジェクトを保存しておく
    conn = connection;
    conn.on("open", function() {
        // 相手のIDを表示する
        // - 相手のIDはconnectionオブジェクトのidプロパティに存在する
        console.log("Connection_id :" + conn.id);
    });

    // メッセージ受信イベントの設定
    conn.on("data", onRecvMessage);
});



peer.on('open', function () {
    $('#my-id').val(peer.id);
});

peer.on('error', function (err) {
    alert(err.message);
});

peer.on('close', function () {
    console.log("close");
});

peer.on('disconnected', function () {
    console.log("disconnect");
});

function addVideo(call, stream) {
    $('#their-video').get(0).srcObject = stream;
}

function removeVideo(peerId) {
    $('#' + peerId).remove();
}

function setupCallEventHandlers(call) {
    if (existingCall) {
        existingCall.close();
    };

    existingCall = call;
    call.on('stream', function (stream) {
        addVideo(call, stream);
        setupEndCallUI();
    });

    call.on('close', function () {
        removeVideo(call.remoteId);
        setupMakeCallUI();
    });
}

peer.on('call', function (call) {
    call.answer(localStream);
    setupCallEventHandlers(call);
});

function setupMakeCallUI() {
    $('#make-call').show();
    $('#end-call').hide();
}

function setupEndCallUI() {
    $('#make-call').hide();
    $('#end-call').show();
}
//マイク・カメラOFF・ON切り替えボタン用スクリプト
const toggleCamera = document.getElementById('js-toggle-camera');
const toggleMicrophone = document.getElementById('js-toggle-microphone');
const cameraStatus = document.getElementById('camera-status');
const microphoneStatus = document.getElementById('microphone-status');

