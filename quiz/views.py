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
def delete_question(request, question_id = None):
    instance = Question.objects.get(id=question_id)
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



def quiz_home(request, quiz_id, question_id):
    quiz = Test.objects.get(id=quiz_id)
    question = Question.objects.get(quiz=quiz, id=question_id)
    # to get the primary key value of next record(question)
    next_id = question_id
    qid= int (question_id)
    for q in Question.objects.filter(quiz=quiz).order_by('-id'):
        if q.id > qid:
            next_id = q.id
    quiz.student.add(request.user)
    if request.method == "POST":

        selected_option = request.POST.get('option')
        res = Response.objects.create(question=question, selected_option=selected_option)
        res.student.add(request.user)
        qid= int (question_id)
        if qid < quiz.question_set.last().id:
            return redirect('/quiz/' + str(quiz_id) + '/' + str(next_id))
        else:
            return redirect('/quiz/' + str(quiz_id)+'/score')
    else:
        return render(request, 'quiz/quiz.html', {"title":quiz.quiz_title,'question': question})


def evaluate(request, quiz_id):
    quiz = Test.objects.get(id=quiz_id)
    questions = Question.objects.filter(quiz=quiz)
    sc = 0
    x = 0
    for question in questions:
        x = x + 1
        user_response = request.user.response_set.get(question=question)
        user_answer = str(user_response.selected_option)
        correct_answer = str(Options.objects.get(question=question, is_correct=True))
        if user_answer == correct_answer:
            sc = sc + 1
    sc = sc/x *100 
    sc = Score.objects.create(quiz=quiz, score=sc)
    sc.student.add(request.user)

    return render(request, 'quiz/quiz_finish.html', {"title": 'Finish ' +quiz.quiz_title,'score': sc})

def view_response(request, username, quiz_id):
    user = Profile.objects.get(username=username)
   

    quiz = Test.objects.get(id=quiz_id, student=user)
    question = Question.objects.filter(quiz=quiz)
    correct_answer = Options.objects.get(question=question, is_correct=True)
    response = Response.objects.filter(question__quiz=quiz, student=user)
    return render(request, 'quiz/show_response.html',
                    { "title": 'Result ' +quiz.quiz_title,'questions': question, 'responses': response })

