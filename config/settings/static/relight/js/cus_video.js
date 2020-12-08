var localStream = null;
var peer = null;
var existingCall = null;
var conn;  

const localVideo = document.getElementById('my-video');
const ChatVideo = document.getElementById('their-video');

localVideo.muted = true; // 自分の音声を自分のスピーカーから聞こえなくする。相手には届く。
localVideo.playsInline = true;
localVideo.autoplay = true;

ChatVideo.muted = true; // Debug用同じデバイスでやるとハウリングするため自分の音声を自分のスピーカーから聞こえなくする。相手には届く。
ChatVideo.playsInline = true;
ChatVideo.autoplay = true;

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
    var name = ($('#callto-id').text()).split("_");
    $("#messages").append($("<p>").text(name[0] + ": " + data).css("font-weight", "bold"));
}

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
    $('#my-id').text(peer.id);
});

peer.on('error', function (err) {
    alert(err.message);
});

peer.on('close', function () {});

peer.on('disconnected', function () {
    console.log("disconnect")
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

$('#make-call').submit(function (e) {
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

        var name = (peer.id).split('_');
 
        // 自分の画面に表示
        $("#messages").append($("<p>").html(name[0] + ": " + message));
 
        // 送信テキストボックスをクリア
        $("#message").val("");
    });

$('#end-call').click(function () {
    existingCall.close();
    conn.close();
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