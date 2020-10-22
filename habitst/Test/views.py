from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import *
from django.db.models import F
import operator


# 메인화면 & tester 입력 받기
def main(request):
    if request.GET:
        tester = Tester()
        tester.name = request.user
        tester.save()
        return redirect("Test:test", tester.id)

    return render(request, "Test/main.html")


# 테스트페이지 // 3번, 4번 6번
def test_page(request, pk):
    tester = get_object_or_404(Tester, pk=pk)
    global num
    num = 1

    if request.POST:
        num = int(request.POST['question_id'])
        score = request.POST.get('score')
        # Question1
        if num == 1:
            if request.POST.get('answer1'):
                tester.Music += int(score)
                
            elif request.POST.get('answer2'):
                tester.Travel += int(score)
              
            elif request.POST.get('answer3'):
                tester.Cooking += int(score)
           
            elif request.POST.get('answer4'):
                tester.Photos += int(score)
               
            tester.save()

        # Question2
        if num == 2:
            if request.POST.get('answer1'):
                tester.Reading += int(score)
              
            elif request.POST.get('answer2'):
                tester.Control += int(score)
              
            elif request.POST.get('answer3'):
                tester.Exercise += int(score)
              
            elif request.POST.get('answer4'):
                tester.Travel += int(score)
        
            tester.save()

        # Question3
        if num == 3:
            if request.POST.get('answer1'):
                tester.Reading += int(score)
              
            elif request.POST.get('answer2'):
                tester.Collect += int(score)
              
            elif request.POST.get('answer3'):
                tester.Leisure += int(score)
            
            elif request.POST.get('answer4'):
                tester.Cooking += int(score)
        
            tester.save()

        # Question4
        if num == 4:
            if request.POST.get('answer1'):
                tester.Control += int(score)
         
            elif request.POST.get('answer2'):
                tester.Leisure += int(score)

            elif request.POST.get('answer3'):
                tester.Control += int(score)

            elif request.POST.get('answer4'):
                tester.Making += int(score)
              
            tester.save()

        # Question5
        if num == 5:
            if request.POST.get('answer1'):
                tester.Collect += int(score)
              

            elif request.POST.get('answer2'):
                tester.Cooking += int(score)

            elif request.POST.get('answer3'):
                tester.Control += int(score)

            elif request.POST.get('answer4'):
                tester.Leisure += int(score)
              
            tester.save()

        # Question6
        if num == 6:
            if request.POST.get('answer1'):
                tester.Exercise += int(score)
             
            elif request.POST.get('answer2'):
                tester.Music += int(score)
           
            elif request.POST.get('answer3'):
                tester.Cooking += int(score)
               
            elif request.POST.get('answer4'):
                tester.Making += int(score)
               
          
            tester.save()

        # Question7
        if num == 7:
            if request.POST.get('answer1'):
                tester.Exercise += int(score)
            
            elif request.POST.get('answer2'):
                tester.Making += int(score)
             
            elif request.POST.get('answer3'):
                tester.Collect += int(score)
              
            elif request.POST.get('answer4'):
                tester.Photos += int(score)
             
            tester.save()

        # Question8
        if num == 8:
            if request.POST.get('answer1'):
                tester.Reading += int(score)
          
            elif request.POST.get('answer2'):
                tester.Making += int(score)

            elif request.POST.get('answer3'):
                tester.Photos += int(score)

            elif request.POST.get('answer4'):
                tester.Travel += int(score)
              
            tester.save()

         # Question9
        if num == 9:
            if request.POST.get('answer1'):
                tester.Reading += int(score)
          
            elif request.POST.get('answer2'):
                tester.Collect += int(score)

            elif request.POST.get('answer3'):
                tester.Travel += int(score)

            elif request.POST.get('answer4'):
                tester.Leisure += int(score)
              
            tester.save()
        
         # Question10
        if num == 10:
            if request.POST.get('answer1'):
                tester.Photos += int(score)
          
            elif request.POST.get('answer2'):
                tester.Exercise += int(score)

            elif request.POST.get('answer3'):
                tester.Control += int(score)

            elif request.POST.get('answer4'):
                tester.Music += int(score)
              
            tester.save()

        # 다음 문제로 넘어가는 로직
        num = int(request.POST['question_id']) + 1

        # 만약 10번까지 다 입력하면 결과창 넘어감
        if num > 10:
            return redirect("Test:loading", pk)

    question = get_object_or_404(Question, id=num)
    return render(request, "Test/testpage.html", {'question': question, 'bar':10*num})


def loading(request, pk):
    tester = get_object_or_404(Tester, pk=pk)
    tester_score = [tester.Leisure, tester.Control, tester.Photos, tester.Cooking, tester.Making,
                    tester.Collect, tester.Reading, tester.Music, tester.Exercise, tester.Travel]

    best_book = max(tester_score)

    for index, ts in enumerate(tester_score):
        if ts == best_book:
            book = Book.objects.get(id=index+1)
            

    return render(request, "Test/loading.html", {'book': book, 'tester':tester})

# 결과도출화면01
def result_01(request, pk):
    tester = get_object_or_404(Tester, pk=pk)
    tester_score = [tester.Leisure, tester.Control, tester.Photos, tester.Cooking, tester.Making,
                    tester.Collect, tester.Reading, tester.Music, tester.Exercise, tester.Travel]

    best_book = max(tester_score)

    for index, ts in enumerate(tester_score):
        if ts == best_book:
            book = Book.objects.get(id=index+1)
            tester.result = book
            tester.save()
    
    return render(request, "Test/result1.html", {'book': book, 'tester':tester})