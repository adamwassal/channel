from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("episode/<int:episode_id>/", views.episode_detail, name="episode-detail"),
    path(
        "episode/<int:episode_id>/add-question/",
        views.add_question,
        name="add-question",
    ),
    path(
        "episode/<int:episode_id>/add-section/",
        views.add_section,
        name="add-section",
    ),
    path(
        "episode/<int:episode_id>/question/<int:question_id>/update/",
        views.update_question,
        name="update-question",
    ),
    path(
        "episode/<int:episode_id>/update-script/",
        views.update_script,
        name="update-script",
    ),
]
