from django import forms
from .models import (
    Material, News, Level, Book, Note, Record, Image,
    Quiz, QuizQuestion, QuizAnswer, Question, Reply
)

common_input = {"class": "form-control"}
common_file = {"class": "form-control"}
common_textarea = {"class": "form-control", "rows": 3}

class LevelForm(forms.ModelForm):
    class Meta:
        model = Level
        fields = ["name", "description", "image"]
        widgets = {
            "name": forms.TextInput(attrs=common_input),
            "description": forms.Textarea(attrs=common_textarea),
        }

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ["title", "description", "file"]
        widgets = {
            "title": forms.TextInput(attrs=common_input),
            "description": forms.Textarea(attrs=common_textarea),
            "file": forms.ClearableFileInput(attrs=common_file),
        }

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ["title", "content", "image", "is_slide", "level"]
        widgets = {
            "title": forms.TextInput(attrs=common_input),
            "content": forms.Textarea(attrs={**common_textarea, "rows": 5}),
            "image": forms.ClearableFileInput(attrs=common_file),
            "level": forms.Select(attrs={"class": "form-select"}),
        }

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["level", "title", "description", "file"]
        widgets = {
            "level": forms.Select(attrs={"class": "form-select"}),
            "title": forms.TextInput(attrs=common_input),
            "description": forms.Textarea(attrs=common_textarea),
            "file": forms.ClearableFileInput(attrs=common_file),
        }

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["level", "title", "file"]
        widgets = {
            "level": forms.Select(attrs={"class": "form-select"}),
            "title": forms.TextInput(attrs=common_input),
            "file": forms.ClearableFileInput(attrs=common_file),
        }

class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ["level", "title", "file"]
        widgets = {
            "level": forms.Select(attrs={"class": "form-select"}),
            "title": forms.TextInput(attrs=common_input),
            "file": forms.ClearableFileInput(attrs=common_file),
        }

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ["level", "title", "image"]
        widgets = {
            "level": forms.Select(attrs={"class": "form-select"}),
            "title": forms.TextInput(attrs=common_input),
            "image": forms.ClearableFileInput(attrs=common_file),
        }

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ["title", "level"]
        widgets = {
            "title": forms.TextInput(attrs=common_input),
            "level": forms.Select(attrs={"class": "form-select"}),
        }

class QuizQuestionForm(forms.ModelForm):
    class Meta:
        model = QuizQuestion
        fields = ["quiz", "text", "question_type"]
        widgets = {
            "quiz": forms.Select(attrs={"class": "form-select"}),
            "text": forms.TextInput(attrs=common_input),
            "question_type": forms.Select(attrs={"class": "form-select"}),
        }

class QuizAnswerForm(forms.ModelForm):
    class Meta:
        model = QuizAnswer
        fields = ["question", "text", "is_correct"]
        widgets = {
            "question": forms.Select(attrs={"class": "form-select"}),
            "text": forms.TextInput(attrs=common_input),
            "is_correct": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["content", "author"]
        widgets = {
            "content": forms.Textarea(attrs={**common_textarea, "placeholder": "Ask your question..."}),
            "author": forms.TextInput(attrs={**common_input, "placeholder": "Your name (optional if logged in)"}),
        }

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ["content", "author"]
        widgets = {
            "content": forms.Textarea(attrs={**common_textarea, "placeholder": "Write a helpful reply..."}),
            "author": forms.TextInput(attrs={**common_input, "placeholder": "Your name (optional if logged in)"}),
        }
