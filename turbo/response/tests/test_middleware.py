# Django
from django.http import HttpResponse

# Third Party Libraries
import pytest

# Django Turbo Response
from turbo_response.middleware import TurboStreamMiddleware


@pytest.fixture
def get_response():
    return lambda req: HttpResponse()


class TestTurboStreamMiddeware:
    def test_accept_header_not_found(self, rf, get_response):
        req = rf.get("/", HTTP_ACCEPT="text/html")
        TurboStreamMiddleware(get_response)(req)
        assert not req.accept_turbo_stream

    def test_accept_header_found(self, rf, get_response):
        req = rf.get("/", HTTP_ACCEPT="text/html; turbo-stream")
        TurboStreamMiddleware(get_response)(req)
        assert req.accept_turbo_stream
