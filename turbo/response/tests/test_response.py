# Django Turbo Response
from turbo_response import (
    Action,
    TurboFrameResponse,
    TurboFrameTemplateResponse,
    TurboStreamResponse,
    TurboStreamStreamingResponse,
    TurboStreamTemplateResponse,
)
from turbo_response.renderers import render_turbo_stream


class TestTurboStreamResponse:
    def test_render(self):
        resp = TurboStreamResponse("OK", action=Action.REMOVE, target="test")
        assert resp.status_code == 200
        assert resp["Content-Type"] == "text/html; turbo-stream; charset=utf-8"
        assert resp.content.startswith(
            b'<turbo-stream action="remove" target="test"><template>OK'
        )


class TestTurboFrameResponse:
    def test_render(self):
        resp = TurboFrameResponse("OK", dom_id="test")
        assert resp.status_code == 200
        assert resp["Content-Type"] == "text/html; charset=utf-8"
        assert resp.content.startswith(b'<turbo-frame id="test">OK')


class TestTurboStreamTemplateResponse:
    def test_render(self, rf):
        req = rf.get("/")
        resp = TurboStreamTemplateResponse(
            req, "simple.html", {"testvar": 1}, action=Action.UPDATE, target="test"
        )
        assert resp.status_code == 200
        assert resp["Content-Type"] == "text/html; turbo-stream; charset=utf-8"
        assert resp.context_data["is_turbo_stream"]
        assert resp.context_data["turbo_stream_action"] == "update"
        assert resp.context_data["turbo_stream_target"] == "test"
        assert resp.context_data["testvar"] == 1
        content = resp.render().content
        assert content.startswith(b'<turbo-stream action="update" target="test"')
        assert b"my content" in content


class TestTurboFrameTemplateResponse:
    def test_render(self, rf):
        req = rf.get("/")
        resp = TurboFrameTemplateResponse(
            req, "simple.html", {"testvar": 1}, dom_id="test"
        )
        assert resp.status_code == 200
        assert resp["Content-Type"] == "text/html; charset=utf-8"
        assert resp.context_data["is_turbo_frame"]
        assert resp.context_data["turbo_frame_dom_id"] == "test"
        assert resp.context_data["testvar"] == 1
        content = resp.render().content
        assert content.startswith(b'<turbo-frame id="test"')
        assert b"my content" in content


class TestTurboStreamStreamingResponse:
    def test_render(self):
        def render():
            yield render_turbo_stream(
                content="test 1", action=Action.REPLACE, target="test_1"
            )
            yield render_turbo_stream(
                content="test 2", action=Action.REPLACE, target="test_2"
            )
            yield render_turbo_stream(
                content="test 3", action=Action.REPLACE, target="test_3"
            )

        resp = TurboStreamStreamingResponse(render())
        assert resp["Content-Type"] == "text/html; turbo-stream; charset=utf-8"
        stream = b"".join(resp.streaming_content)
        assert (
            b'<turbo-stream action="replace" target="test_1"><template>test 1' in stream
        )
        assert (
            b'<turbo-stream action="replace" target="test_2"><template>test 2' in stream
        )
        assert (
            b'<turbo-stream action="replace" target="test_3"><template>test 3' in stream
        )
