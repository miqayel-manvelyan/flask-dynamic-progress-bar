$(document).ready(function(){
    const socket = io.connect('http://' + document.domain + ':' + location.port + '/progress');
    const $progressBar = $('#test-progress-bar');

    socket.on('progress', function(msg) {
        let percent = msg.percent + '%'
        $progressBar.width(percent)
        $progressBar.text(percent)

        if (msg.percent >= 100) {
            $('#test-button').removeClass('d-none');
        }
    });
});
