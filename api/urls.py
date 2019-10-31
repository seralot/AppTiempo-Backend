from django.urls import path

from api.views import MyView

urlpatterns = [
    path('data/', MyView.as_view(), name="my-view")
]