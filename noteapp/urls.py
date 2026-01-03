from django.urls import path,include
from . import views

urlpatterns = [
    path("notes/",views.notes, name="notes"),
    path("notes/<slug:slug>/",views.note_detail, name="note-detail"),
    path("api/auth/register/",views.register, name="register")
]

