(function () {
  "use strict";
  let protocol = location.protocol.match("https:") ? "wss" : "ws";
  let port = location.port ? ":" + location.port : "";
  const socket = new ReconnectingWebSocket(
    `${protocol}://${location.hostname}${port}/ws/`
  );

  class TurboChannelsStreamSource extends HTMLElement {
    constructor() {
      super();
    }

    async connectedCallback() {
      Turbo.connectStreamSource(this);
      if (socket.readyState !== WebSocket.OPEN) {
        socket.addEventListener("open", (e) => {
          this.subscribe();
        });
      } else {
        this.subscribe();
      }

      socket.addEventListener("message", (e) => {
        const broadcast = JSON.parse(e.data);
        if (broadcast.signed_channel_name === this.channelName) {
          this.dispatchMessageEvent(broadcast.data);
        }
      });
    }

    disconnectedCallback() {
      Turbo.disconnectStreamSource(this);
      socket.send(
        JSON.stringify({ ...this.subscription, type: "unsubscribe" })
      );
    }

    dispatchMessageEvent(data) {
      const event = new MessageEvent("message", { data });
      return this.dispatchEvent(event);
    }

    get channelName() {
      return this.getAttribute("signed-channel-name");
    }

    get subscription() {
      return { signed_channel_name: this.channelName };
    }

    subscribe() {
      socket.send(JSON.stringify({ type: "subscribe", ...this.subscription }));
    }
  }

  customElements.define(
    "turbo-channels-stream-source",
    TurboChannelsStreamSource
  );
})();
