(function () {
  "use strict";
  let protocol = location.protocol.match("https:") ? "wss" : "ws";
  let port = location.port ? ":" + location.port : "";
  const socket = new ReconnectingWebSocket(
    `${protocol}://${location.hostname}${port}/ws/`
  );
  let counter = 0;

  class TurboChannelsStreamSource extends HTMLElement {
    request_id;

    constructor() {
      super();
      this.request_id = counter++;
    }

    async connectedCallback() {
      Turbo.connectStreamSource(this);

      socket.addEventListener("open", (e) => {
        socket.send(
          JSON.stringify({ request_id: this.request_id, type: "subscribe", ...this.subscription })
        );
      });

      socket.addEventListener("message", (e) => {
        const broadcast = JSON.parse(e.data);
        if (broadcast.request_id === this.request_id) {
          this.dispatchMessageEvent(broadcast.data);
        }
      });
    }

    disconnectedCallback() {
      socket.send(JSON.stringify({ request_id: this.request_id, type: "unsubscribe" }))
      Turbo.disconnectStreamSource(this);
    }

    dispatchMessageEvent(data) {
      const event = new MessageEvent("message", { data });
      return this.dispatchEvent(event);
    }

    get subscription() {
      const signed_channel_name = this.getAttribute("signed-channel-name")
      return { signed_channel_name };
    }
  }

  customElements.define(
    "turbo-channels-stream-source",
    TurboChannelsStreamSource
  );
})();
