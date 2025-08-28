from django.urls import path
from . import views

app_name = "material"

urlpatterns = [
    path("", views.homepage, name="home"),
    path("home/", views.homepage, name="home"),

    # Levels
    path("levels/add/", views.level_create, name="level_create"),
    path("levels/<int:pk>/edit/", views.level_edit, name="level_edit"),
    path("levels/<int:pk>/delete/", views.level_delete, name="level_delete"),
    path("levels/<int:level_id>/", views.level_detail, name="details"),

    # Material & Assets
    path("materials/add/", views.material_create, name="material_create"),
    path("books/add/", views.book_create, name="book_create"),
    path("notes/add/", views.note_create, name="note_create"),
    path("records/add/", views.record_create, name="record_create"),
    path("images/add/", views.image_create, name="image_create"),

    # Quizzes
    path("levels/<int:level_id>/quiz/builder/", views.quiz_builder, name="quiz_builder"),
    path("quizzes/add/", views.quiz_create, name="quiz_create"),
    path("quizzes/<int:quiz_id>/question/add/", views.quiz_add_question, name="quiz_add_question"),
    path("questions/<int:question_id>/answers/add/", views.quiz_add_answers, name="quiz_add_answers"),
    path("levels/<int:level_id>/quiz/submit/", views.quiz_submit, name="quiz_submit"),

    # Q&A
    path("levels/<int:level_id>/question/add/", views.add_question, name="add_question"),
    path("questions/<int:question_id>/reply/add/", views.add_reply, name="add_reply"),
    path("replies/<int:reply_id>/upvote/", views.upvote_reply, name="upvote_reply"),
]
