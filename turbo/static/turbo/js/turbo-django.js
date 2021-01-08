(function () {
  "use strict";
  let protocol = location.protocol.match("https:") ? "wss" : "ws";
  let port = location.port ? ":" + location.port : "";
  const socket = new ReconnectingWebSocket(
    `${protocol}://${location.hostname}${port}/ws/`
  );
  let counter = 0;

  class TurboChannelsStreamSource extends HTMLElement {
    constructor() {
      super();
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
        if (broadcast.signed_channel_name === this.channelName) {
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
