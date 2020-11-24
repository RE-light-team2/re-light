var localStream = null;
var peer = null;
var existingCall = null;

const localVideo = document.getElementById('my-video');
const ChatVideo = document.getElementById('their-video');

localVideo.muted = true; // 自分の音声を自分のスピーカーから聞こえなくする。相手には届く。
localVideo.playsInline = true;
localVideo.autoplay = true;

ChatVideo.playsInline = true;
ChatVideo.autoplay = true;

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
    

peer.on('open', function(){
    $('#my-id').text(peer.id);
});

peer.on('error', function(err){
    alert(err.message);
});

peer.on('close', function(){
});

peer.on('disconnected', function(){
    console.log("disconnect")
});

function addVideo(call,stream){
    $('#their-video').get(0).srcObject = stream;
}

function removeVideo(peerId){
    $('#' + peerId).remove();
}

function setupCallEventHandlers(call){
    if (existingCall) {
        existingCall.close();
    };
    
    existingCall = call;
    call.on('stream', function(stream){
        addVideo(call,stream);
        setupEndCallUI();
        $('#their-id').text(call.remoteId);        
    });

    call.on('close', function(){
        removeVideo(call.remoteId);
        setupMakeCallUI();
    });
}

peer.on('call', function(call){
    call.answer(localStream);
    setupCallEventHandlers(call);
});

$('#end-call').click(function(){
    existingCall.close();
});

function setupMakeCallUI(){
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

