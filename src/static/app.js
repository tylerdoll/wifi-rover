const DIRECTIONS = {
    w: 'forward',
    a: 'left',
    s: 'backward',
    d: 'right',
};

let driving = false;
let ws = null;

function connect() {
    const WEBSOCKET_ROUTE = "/ws";

    if (window.location.protocol == "http:") {
        var ws = new WebSocket("ws://" + window.location.host + WEBSOCKET_ROUTE);
    } else if (window.location.protocol == "https:") {
        var ws = new WebSocket("wss://" + window.location.host + WEBSOCKET_ROUTE);
    }

    ws.onopen = () =>$("#ws-status").html("Connected");
    ws.onmessage = e => {}
    ws.onclose = () => $("#ws-status").html("Disconnected");

    return ws
}

$(document).ready(() => {
    ws = connect()

    // Keyboard commands
    $(document).keydown(e => {
        if (e.key in DIRECTIONS && !driving) {
            ws.send(DIRECTIONS[e.key]);
            driving = true;
        }
    });
    $(document).keyup(() => {
        if (driving) {
            ws.send('stop');
            driving = false;
        }
    });

    // Status buttons
    $('#connect').click(() => ws = connect());
    $('#shutdown').click(() => {
        let conf = confirm("Are you sure you want to shutdown the rover?");
        if (conf) ws.send("shutdown");
    });

    // Settings update button
    $('#rover-settings').submit(e => {
        e.preventDefault();
        ws.send('speed-right=' + $('#speed-right').val());
        ws.send('speed-left=' + $('#speed-left').val());
        ws.send('pwm-freq-right=' + $('#pwm-freq-right').val());
        ws.send('pwm-freq-left=' + $('#pwm-freq-left').val());
    });

    // Controller buttons
    $('#rover-forward').bind("mousedown touchstart", () => ws.send(DIRECTIONS['w']));
    $('#rover-left').bind("mousedown touchstart", () => ws.send(DIRECTIONS['a']));
    $('#rover-right').bind("mousedown touchstart", () => ws.send(DIRECTIONS['d']));
    $('#rover-backward').bind("mousedown touchstart", () => ws.send(DIRECTIONS['s']));
    $('#rover-forward,#rover-left,#rover-right,#rover-backward').bind("mouseup touchend", () => ws.send('stop'));
});
