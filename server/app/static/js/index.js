const socket = new WebSocket(
    "ws://" + window.location.host + "/ws"
);

socket.onmessage = function (event) {

    const message = JSON.parse(event.data);

    switch (message.kind) {

        case "image":
            location.reload();
            break;

        case "event":
            addEvent(message.event);
            break;
    }

};


function addEvent(event) {

    const div = document.createElement("div");

    div.className = "event";

    div.style.borderLeft =
        "6px solid " + event.color;

    div.style.background =
        event.background;


    div.innerHTML = `

        <div>

            <b>

                ${event.icon}
                ${event.title}

            </b>

        </div>

        <div>

            ${event.message}

        </div>

        <small>

            ${event.time}

        </small>

    `;


    document
        .getElementById("event-list")
        .prepend(div);

}