from django.db import models
from django import forms



# 0. 들어갈 책들의 데이터
# 이 책들의 Score가 쌓이는 형식(유저 name참조)으로 views를 짜야함
# 책은 pk id번호 (1~16)로 분류될 것
class Book(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    img = models.URLField()
    content = models.TextField() #시구절
    def __str__(self):
        return self.name

# 1. 테스트를 진행하는 유저
class Tester(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    #score
    Leisure = models.IntegerField(default=0)
    Control = models.IntegerField(default=0)
    Photos = models.IntegerField(default=0)
    Cooking = models.IntegerField(default=0)
    Making = models.IntegerField(default=0)
    Collect = models.IntegerField(default=0)
    Reading = models.IntegerField(default=0)
    Music = models.IntegerField(default=0)
    Exercise = models.IntegerField(default=0)
    Travel = models.IntegerField(default=0)
    result = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.name


# 2. 질문 데이터
class Question(models.Model):
    title = models.TextField()
    score = models.IntegerField()
    opt1 = models.TextField()
    opt2 = models.TextField()
    opt3 = models.TextField()
    opt4 = models.TextField()
    def __str__(self):
        return self.title


#result 모델 굳이 필요 없이 views에서 max구하는 함수짜서, Max를 출력해주면 될 듯.
