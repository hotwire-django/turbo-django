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

      socket.addEventListener("open", (e) => {
        socket.send(
          JSON.stringify({ request_id: this.request_id, ...this.subscription })
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
      Turbo.disconnectStreamSource(this);
    }

    dispatchMessageEvent(data) {
      const event = new MessageEvent("message", { data });
      return this.dispatchEvent(event);
    }

    get subscription() {
      const model = this.getAttribute("model");
      const pk = this.getAttribute("pk");
      const list_target = this.getAttribute("list-target");
      const element_prefix = this.getAttribute("element-prefix");

      return { model, pk, list_target, element_prefix };
    }
  }

  customElements.define(
    "turbo-channels-stream-source",
    TurboChannelsStreamSource
  );
})();
