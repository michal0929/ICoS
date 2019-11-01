from django.shortcuts import render, redirect
from .models import Test, Question, Options, Score, Response
from users.models import UserProfile as Profile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import HttpResponseRedirect

@login_required
def quizhome(request):
    if request.user.is_authenticated:
        all_quiz = Test.objects.all()
        
        context = {
        "title": "Quiz",
        "all_quiz": all_quiz,
    }
      
    return render(request, 'quiz/quizhome.html', context)

@login_required   
def add_question(request, quiz_title):

    quiz = Test.objects.get(quiz_title=quiz_title)
    question = Question.objects.filter(quiz=quiz)
    if request.method == "POST":
            question_text = request.POST.get('question_text')
            option1 = request.POST.get('option1')
            option2 = request.POST.get('option2')
            option3 = request.POST.get('option3')
            option4 = request.POST.get('option4')
            correct_ans = request.POST.get('correct_ans')
            ques = Question.objects.create(quiz=quiz, question_text=question_text)
            Options.objects.create(question=ques, option_text=option1)
            Options.objects.create(question=ques, option_text=option2)
            Options.objects.create(question=ques, option_text=option3)
            Options.objects.create(question=ques, option_text=option4)
            ca = Options.objects.get(question=ques, option_text=correct_ans)
            ca.is_correct = True
            ca.save()
            return render(request, 'quiz/add_question.html', {"title":quiz.quiz_title,'questions': question, 'quiz': quiz})

    else:
            return render(request, 'quiz/add_question.html', {"title":quiz.quiz_title,'questions': question, 'quiz': quiz})

@user_passes_test(lambda user: user.is_professor)
def delete_question(request, question_text):
    instance = Question.objects.get(question_text=question_text)
    instance.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def view_result(request, quiz_title):
    quiz = Test.objects.get(quiz_title=quiz_title)
    all_students = quiz.student.all()
    dict = {}
    for t in all_students:
        q = Test.objects.get(quiz_title=quiz_title, student=t)
        dict[t] = t.score_set.get(quiz=q)

    context = {
        "title": "Result " + quiz_title,
        "dict": dict, 
        "current_quiz": quiz
    }    

    return render(request, 'quiz/view_result.html', context)




