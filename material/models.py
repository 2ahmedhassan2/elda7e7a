from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

class Level(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="level_images/", blank=True, null=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name


class StudentHonor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username if self.user else 'NoUser'} ({self.score})"


class Book(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name="books")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to="books/")

    def __str__(self):
        return self.title


class Note(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name="notes")
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to="notes/")

    def __str__(self):
        return self.title


class Record(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name="records")
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to="records/")

    def __str__(self):
        return self.title


class Image(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name="images")
    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to="images/")

    def __str__(self):
        return self.title or f"Image #{self.pk}"


class Material(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to="materials/", blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to="news_images/", blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_slide = models.BooleanField(default=False)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name="news", null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("material:news_detail", args=[self.id])


# ── Quiz System ────────────────────────────────────────────────────────────────
class Quiz(models.Model):
    title = models.CharField(max_length=200, default="Untitled Quiz")
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name="quizzes")

    def __str__(self):
        return self.title


class QuizQuestion(models.Model):
    QUESTION_TYPES = [
        ("single", "Single Choice"),      # only one correct
        ("multiple", "Multiple Choice"),  # select all correct
        ("truefalse", "True / False"),    # simple True/False
    ]
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    text = models.CharField(max_length=500)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, default="single")

    def __str__(self):
        return f"{self.text} [{self.get_question_type_display()}]"


class QuizAnswer(models.Model):
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, related_name="answers")
    text = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text} ({'Correct' if self.is_correct else 'Wrong'})"


# ── Q&A ────────────────────────────────────────────────────────────────────────
class Question(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name="questions")
    author = models.CharField(max_length=100, blank=True)
    author_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Q by {self.author or (self.author_user.username if self.author_user else 'Anon')}: {self.content[:20]}..."


class Reply(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="replies")
    author = models.CharField(max_length=100, blank=True)
    author_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    upvotes = models.IntegerField(default=0)

    class Meta:
        ordering = ["-upvotes", "-created_at"]

    def __str__(self):
        return f"Reply by {self.author or (self.author_user.username if self.author_user else 'Anon')}"
