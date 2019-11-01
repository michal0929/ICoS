from django.conf.urls import url
from quiz import views as quiz_views


urlpatterns = [
    url(r'^$', quiz_views.quizhome, name='quizhome'),
    url(r'^result/(?P<quiz_title>[\w ]+)', quiz_views.view_result, name='result_quiz'),
    url(r'^professor/add_question/(?P<quiz_title>[\w ]+)', quiz_views.add_question, name='add_question'),
    url(r'^professor/delete/(?P<question_text>[\w ]+)', quiz_views.delete_question, name='delete_question'),
]