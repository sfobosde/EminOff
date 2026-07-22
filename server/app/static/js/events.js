window.EventPanel = {

    add(event) {

        const div = document.createElement("div");

        div.className = "event";

        div.style.borderLeft =
            `6px solid ${event.color}`;

        div.style.background =
            event.background;

        div.innerHTML = `
            <div>
                <b>${event.icon} ${event.title}</b>
            </div>

            <div>${event.message}</div>

            <small>${event.time}</small>
        `;

        document
            .getElementById("event-list")
            .prepend(div);

    }

};