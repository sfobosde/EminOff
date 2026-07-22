function connectWebSocket() {

    const protocol =
        window.location.protocol === "https:"
            ? "wss://"
            : "ws://";

    const socket = new WebSocket(
        protocol +
        window.location.host +
        "/ws"
    );

    socket.onmessage = function (event) {

        const message = JSON.parse(event.data);

        switch (message.kind) {

            case "image":
                window.Gallery.reload();
                break;

            case "event":
                window.EventPanel.add(message.event);
                break;

        }

    };

    socket.onclose = function () {
        setTimeout(connectWebSocket, 2000);
    };

}