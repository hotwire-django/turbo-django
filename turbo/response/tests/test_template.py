# Django Turbo Response
from turbo_response import (
    Action,
    render_turbo_frame_template,
    render_turbo_stream_template,
)


class TestRenderTurboStreamTemplate:
    def test_render(self):
        s = render_turbo_stream_template(
            "simple.html", {}, action=Action.UPDATE, target="test"
        )
        assert (
            s
            == '<turbo-stream action="update" target="test"><template><div>my content</div></template></turbo-stream>'
        )


class TestRenderTurboTemplate:
    def test_render(self):
        s = render_turbo_frame_template("simple.html", {}, dom_id="test")
        assert s == '<turbo-frame id="test"><div>my content</div></turbo-frame>'
