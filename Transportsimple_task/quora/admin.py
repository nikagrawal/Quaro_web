from django.contrib import admin
from .models import Question, Answer, Liked

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_on', 'author', 'uquest_id')
    search_fields = ('question', 'author__username', 'uquest_id')
    list_filter = ('created_on', 'author')

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'ans', 'created_on', 'author', 'uans_id')
    search_fields = ('question__question', 'author__username', 'uans_id')
    list_filter = ('created_on', 'author')

@admin.register(Liked)
class LikedAdmin(admin.ModelAdmin):
    list_display = ('answer', 'user')
