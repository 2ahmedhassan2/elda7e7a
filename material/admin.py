from django.contrib import admin
from .models import (
    Level, StudentHonor, Book, Note, Record, Image,
    Material, News, Quiz, QuizQuestion, QuizAnswer, Question, Reply
)

@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "is_slide", "created_at", "level")
    list_filter = ("is_slide", "created_at")
    search_fields = ("title", "content")

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created_at")
    search_fields = ("title", "description")

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "level")

admin.site.register(StudentHonor)
admin.site.register(Book)
admin.site.register(Note)
admin.site.register(Record)
admin.site.register(Image)
admin.site.register(QuizQuestion)
admin.site.register(QuizAnswer)
admin.site.register(Question)
admin.site.register(Reply)
