# Django
from django import forms

# Third Party Libraries
import pytest

# Django Turbo Response
from turbo_response import Action
from turbo_response.tests.testapp.forms import TodoForm
from turbo_response.tests.testapp.models import TodoItem
from turbo_response.views import (
    TurboFrameTemplateView,
    TurboFrameView,
    TurboStreamCreateView,
    TurboStreamDeleteView,
    TurboStreamFormView,
    TurboStreamTemplateView,
    TurboStreamUpdateView,
    TurboStreamView,
)

pytestmark = pytest.mark.django_db


@pytest.fixture
def todo():
    return TodoItem.objects.create(description="test")


class MyForm(forms.Form):
    description = forms.CharField()


class TestTurboStreamView:
    def test_get(self, rf):
        class MyView(TurboStreamView):
            def get_response_content(self):
                return "hello"

        req = rf.get("/")
        resp = MyView.as_view(
            turbo_stream_target="test", turbo_stream_action=Action.REPLACE
        )(req)
        assert resp.status_code == 200
        assert "text/html; turbo-stream;" in resp["Content-Type"]
        assert resp.content.startswith(
            b'<turbo-stream action="replace" target="test"><template>hello'
        )


class TestTurboStreamTemplateView:
    def test_get(self, rf):
        class MyView(TurboStreamTemplateView):
            template_name = "simple.html"

        req = rf.get("/")
        resp = MyView.as_view(
            turbo_stream_target="test", turbo_stream_action=Action.REPLACE
        )(req)

        assert resp.status_code == 200
        assert "text/html; turbo-stream;" in resp["Content-Type"]
        assert "is_turbo_stream" in resp.context_data
        assert resp.template_name == ["simple.html"]
        assert resp.render().content.startswith(
            b'<turbo-stream action="replace" target="test"><template><div>my content'
        )


class TestTurboStreamCreateView:
    class MyView(TurboStreamCreateView):
        form_class = TodoForm
        model = TodoItem
        success_url = "/done/"

    def test_get(self, rf):
        req = rf.get("/")
        resp = self.MyView.as_view()(req)
        assert resp.status_code == 200
        assert resp["Content-Type"] == "text/html; charset=utf-8"
        assert "is_turbo_stream" not in resp.context_data
        assert "form" in resp.context_data
        assert resp.context_data["turbo_stream_target"] == "testapp-todoitem-form"
        assert resp.template_name == ["testapp/todoitem_form.html"]

    def test_get_with_explicit_target(self, rf):
        req = rf.get("/")
        resp = self.MyView.as_view(turbo_stream_target="my-form")(req)
        assert resp.status_code == 200
        assert resp["Content-Type"] == "text/html; charset=utf-8"
        assert "is_turbo_stream" not in resp.context_data
        assert "form" in resp.context_data
        assert resp.context_data["turbo_stream_target"] == "my-form"
        assert resp.template_name == ["testapp/todoitem_form.html"]

    def test_post_with_validation_errors(self, rf):
        req = rf.post("/", {})
        resp = self.MyView.as_view()(req)
        assert resp.status_code == 200
        assert resp["Content-Type"] == "text/html; turbo-stream; charset=utf-8"
        assert resp.context_data["is_turbo_stream"]
        assert resp.context_data["turbo_stream_action"] == "replace"
        assert resp.context_data["turbo_stream_target"] == "testapp-todoitem-form"
        assert resp.template_name == ["testapp/_todoitem_form.html"]
        assert resp.render().content.startswith(b"<turbo-stream")

    def test_post_with_validation_errors_with_explicit_target(self, rf):
        req = rf.post("/", {})
        resp = self.MyView.as_view(turbo_stream_target="my-form")(req)
        assert resp.status_code == 200
        assert resp["Content-Type"] == "text/html; turbo-stream; charset=utf-8"
        assert resp.context_data["is_turbo_stream"]
        assert resp.context_data["turbo_stream_action"] == "replace"
        assert resp.context_data["turbo_stream_target"] == "my-form"
        assert resp.template_name == ["testapp/_todoitem_form.html"]
        assert resp.render().content.startswith(b"<turbo-stream")

    def test_post_success(self, rf):
        req = rf.post("/", {"description": "ok"})
        resp = self.MyView.as_view()(req)
        assert resp.url == "/done/"
        assert TodoItem.objects.count() == 1


class TestTurboStreamUpdateView:
    class MyView(TurboStreamUpdateView):
        form_class = TodoForm
        model = TodoItem
        success_url = "/done/"

    def test_get(self, rf, todo):
        req = rf.get("/")
        resp = self.MyView.as_view()(req, pk=todo.pk)
        assert resp.status_code == 200
        assert resp["Content-Type"] == "text/html; charset=utf-8"
        assert "is_turbo_stream" not in resp.context_data
        assert "form" in resp.context_data
        assert (
            resp.context_data["turbo_stream_target"]
            == f"testapp-todoitem-{todo.id}-form"
        )
        assert resp.template_name == ["testapp/todoitem_form.html"]

    def test_get_with_explicit_target(self, rf, todo):
        req = rf.get("/")
        resp = self.MyView.as_view(turbo_stream_target="my-form")(req, pk=todo.pk)
        assert resp.status_code == 200
        assert resp["Content-Type"] == "text/html; charset=utf-8"
        assert "is_turbo_stream" not in resp.context_data
        assert "form" in resp.context_data
        assert resp.context_data["turbo_stream_target"] == "my-form"
        assert resp.template_name == ["testapp/todoitem_form.html"]

    def test_post_with_validation_errors(self, rf, todo):
        req = rf.post("/", {})
        resp = self.MyView.as_view()(req, pk=todo.pk)
        assert resp.status_code == 200
        assert resp["Content-Type"] == "text/html; turbo-stream; charset=utf-8"
        assert resp.context_data["is_turbo_stream"]
        assert resp.context_data["turbo_stream_action"] == "replace"
        assert (
            resp.context_data["turbo_stream_target"]
            == f"testapp-todoitem-{todo.id}-form"
        )
        assert resp.template_name == ["testapp/_todoitem_form.html"]
        assert resp.render().content.startswith(b"<turbo-stream")

    def test_post_with_validation_errors_with_explicit_target(self, rf, todo):
        req = rf.post("/", {})
        resp = self.MyView.as_view(turbo_stream_target="my-form")(req, pk=todo.pk)
        assert resp.status_code == 200
        assert resp["Content-Type"] == "text/html; turbo-stream; charset=utf-8"
        assert resp.context_data["is_turbo_stream"]
        assert resp.context_data["turbo_stream_action"] == "replace"
        assert resp.context_data["turbo_stream_target"] == "my-form"
        assert resp.template_name == ["testapp/_todoitem_form.html"]
        assert resp.render().content.startswith(b"<turbo-stream")

    def test_post_success(self, rf, todo):
        req = rf.post("/", {"description": "updated!"})
        resp = self.MyView.as_view()(req, pk=todo.pk)
        assert resp.url == "/done/"
        todo.refresh_from_db()
        assert todo.description == "updated!"


class TestTurboStreamFormView:
    class MyView(TurboStreamFormView):
        form_class = MyForm
        template_name = "my_form.html"
        turbo_stream_target = "my-form"
        success_url = "/done/"

    def test_get(self, rf):
        req = rf.get("/")
        resp = self.MyView.as_view()(req)
        assert resp.status_code == 200
        assert resp["Content-Type"] == "text/html; charset=utf-8"
        assert "is_turbo_stream" not in resp.context_data
        assert "form" in resp.context_data
        assert resp.template_name == ["my_form.html"]

    def test_post_with_validation_errors(self, rf):
        req = rf.post("/", {})
        resp = self.MyView.as_view()(req)
        assert resp.status_code == 200
        assert resp["Content-Type"] == "text/html; turbo-stream; charset=utf-8"
        assert resp.context_data["is_turbo_stream"]
        assert resp.context_data["turbo_stream_action"] == "replace"
        assert resp.context_data["turbo_stream_target"] == "my-form"
        assert resp.template_name == ["_my_form.html"]
        assert resp.render().content.startswith(b"<turbo-stream")

    def test_post_success(self, rf):
        req = rf.post("/", {"description": "ok"})
        resp = self.MyView.as_view()(req)
        assert resp.url == "/done/"


class TestTurboStreamDeleteView:
    class MyView(TurboStreamDeleteView):
        template_name = "simple.html"
        turbo_stream_target = "item"
        model = TodoItem

    def test_post(self, rf, todo):
        req = rf.post("/")
        resp = self.MyView.as_view()(req, pk=todo.pk)
        assert resp.status_code == 200
        assert resp["Content-Type"] == "text/html; turbo-stream; charset=utf-8"
        assert TodoItem.objects.count() == 0


class TestTurboFrameView:
    class MyView(TurboFrameView):
        turbo_frame_dom_id = "test"

        def get_response_content(self):
            return "done"

    def test_get(self, rf):
        req = rf.get("/")
        resp = self.MyView.as_view()(req)
        assert resp.status_code == 200
        assert resp["Content-Type"] == "text/html; charset=utf-8"
        assert resp.content == b'<turbo-frame id="test">done</turbo-frame>'


class TestTurboFrameTemplateView:
    class MyView(TurboFrameTemplateView):
        turbo_frame_dom_id = "test"
        template_name = "simple.html"

        def get_response_content(self):
            return "done"

    def test_get(self, rf):
        req = rf.get("/")
        resp = self.MyView.as_view()(req)
        assert resp.status_code == 200
        assert resp["Content-Type"] == "text/html; charset=utf-8"
        assert (
            resp.render().content
            == b'<turbo-frame id="test"><div>my content</div></turbo-frame>'
        )
