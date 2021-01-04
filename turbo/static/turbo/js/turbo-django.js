(function () {
  "use strict";
  let protocol = location.protocol.match("https:") ? "wss" : "ws";
  let port = location.port ? ":" + location.port : "";
  const socket = new ReconnectingWebSocket(
    `${protocol}://${location.hostname}${port}/ws/`
  );

  class TurboChannelsStreamSource extends HTMLElement {
    static counter = 0;
    request_id;

    constructor() {
      super();
      this.request_id = TurboChannelsStreamSource.counter++;
    }

    async connectedCallback() {
      Turbo.connectStreamSource(this);

      // If connection is already open, just send the subscription
      if (socket.readyState === ReconnectingWebSocket.OPEN) {
        this.sendSubscription();
      }

      // We also register a Listener to subscripe whenever the stream opens (e.g. after a reconnect
      // or if its not connected at first
      socket.addEventListener("open", (e) => {
        this.sendSubscription();
      });


      socket.addEventListener("message", (e) => {
        const broadcast = JSON.parse(e.data);
        if (broadcast.request_id === this.request_id) {
          this.dispatchMessageEvent(broadcast.data);
        }
      });
    }

    // Send subscription to the right types of message(s)
    sendSubscription() {
      socket.send(
          JSON.stringify({request_id: this.request_id, type: "subscribe", ...this.subscription})
      );
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
