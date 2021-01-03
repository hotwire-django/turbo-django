# Django Turbo Response
from turbo_response import Action, render_turbo_frame, render_turbo_stream


class TestRenderTurboStream:
    def test_render_empty_stream(self):
        s = render_turbo_stream(action=Action.REMOVE, target="test")
        assert (
            s
            == '<turbo-stream action="remove" target="test"><template></template></turbo-stream>'
        )

    def test_render_content(self):
        s = render_turbo_stream(
            action=Action.REPLACE, target="test", content="<div>my content</div>",
        )
        assert (
            s
            == '<turbo-stream action="replace" target="test"><template><div>my content</div></template></turbo-stream>'
        )


class TestRenderTurboFrame:
    def test_render_empty_frame(self):
        s = render_turbo_frame("test")
        assert s == '<turbo-frame id="test"></turbo-frame>'

    def test_render_content(self):
        s = render_turbo_frame(dom_id="test", content="<div>my content</div>",)
        assert s == '<turbo-frame id="test"><div>my content</div></turbo-frame>'
