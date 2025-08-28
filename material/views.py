from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User

from .models import (
    News, Level, StudentHonor, Book, Note, Record, Image,
    Material, Quiz, QuizQuestion, QuizAnswer, Question, Reply
)
from .forms import (
    MaterialForm, NewsForm, LevelForm, BookForm, NoteForm, RecordForm, ImageForm,
    QuizForm, QuizQuestionForm, QuizAnswerForm, QuestionForm, ReplyForm
)

def ensure_honor_entry(user: User):
    if not user.is_authenticated:
        return None
    obj, _ = StudentHonor.objects.get_or_create(user=user)
    return obj

def is_staff(user):
    return user.is_staff or user.is_superuser

# ── Homepage ───────────────────────────────────────────────────────────────────
def homepage(request):
    slides = News.objects.filter(is_slide=True)[:5]
    news_list = News.objects.all()[:6]
    levels = Level.objects.all()

    top_students = StudentHonor.objects.select_related("user").order_by("-score")[:8]
    ranked_students = [{"rank": i + 1, "student": s} for i, s in enumerate(top_students)]

    return render(request, "material/home.html", {
        "slides": slides,
        "news_list": news_list,
        "levels": levels,
        "top_students": ranked_students,
    })

# ── Level detail ───────────────────────────────────────────────────────────────
def level_detail(request, level_id):
    level = get_object_or_404(Level, id=level_id)
    return render(request, "material/subs.html", {
        "level": level,
        "books": level.books.all(),
        "notes": level.notes.all(),
        "records": level.records.all(),
        "images": level.images.all(),
        "quizzes": level.quizzes.all(),
        "questions": level.questions.all(),
        "news_list": level.news.all(),
    })

# ── Level CRUD ─────────────────────────────────────────────────────────────────
@login_required
@user_passes_test(is_staff)
def level_create(request):
    if request.method == "POST":
        form = LevelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Level created.")
            return redirect("material:home")
    else:
        form = LevelForm()
    return render(request, "material/simple_form.html", {"form": form, "title": "Create Level"})

@login_required
@user_passes_test(is_staff)
def level_edit(request, pk):
    level = get_object_or_404(Level, pk=pk)
    if request.method == "POST":
        form = LevelForm(request.POST, request.FILES, instance=level)
        if form.is_valid():
            form.save()
            messages.success(request, "Level updated.")
            return redirect("material:details", level_id=level.id)
    else:
        form = LevelForm(instance=level)
    return render(request, "material/simple_form.html", {"form": form, "title": "Edit Level"})

@login_required
@user_passes_test(is_staff)
def level_delete(request, pk):
    level = get_object_or_404(Level, pk=pk)
    if request.method == "POST":
        level.delete()
        messages.success(request, "Level deleted.")
        return redirect("material:home")
    return render(request, "material/confirm_delete.html", {"object": level, "title": "Delete Level"})

# ── Material / Files ───────────────────────────────────────────────────────────
@login_required
@user_passes_test(is_staff)
def material_create(request):
    if request.method == "POST":
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Material added.")
            return redirect("material:home")
    else:
        form = MaterialForm()
    return render(request, "material/simple_form.html", {"form": form, "title": "Add Material"})

@login_required
@user_passes_test(is_staff)
def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()
            messages.success(request, "Book uploaded.")
            return redirect("material:details", level_id=book.level.id)
    else:
        form = BookForm()
    return render(request, "material/simple_form.html", {"form": form, "title": "Add Book"})

@login_required
@user_passes_test(is_staff)
def note_create(request):
    if request.method == "POST":
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save()
            messages.success(request, "Note uploaded.")
            return redirect("material:details", level_id=note.level.id)
    else:
        form = NoteForm()
    return render(request, "material/simple_form.html", {"form": form, "title": "Add Note"})

@login_required
@user_passes_test(is_staff)
def record_create(request):
    if request.method == "POST":
        form = RecordForm(request.POST, request.FILES)
        if form.is_valid():
            record = form.save()
            messages.success(request, "Audio uploaded.")
            return redirect("material:details", level_id=record.level.id)
    else:
        form = RecordForm()
    return render(request, "material/simple_form.html", {"form": form, "title": "Add Audio"})

@login_required
@user_passes_test(is_staff)
def image_create(request):
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.save()
            messages.success(request, "Image added.")
            return redirect("material:details", level_id=img.level.id)
    else:
        form = ImageForm()
    return render(request, "material/simple_form.html", {"form": form, "title": "Add Image"})

# ── Quiz ───────────────────────────────────────────────────────────────────────
@login_required
@user_passes_test(is_staff)
def quiz_create(request):
    if request.method == "POST":
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save()
            messages.success(request, "Quiz created.")
            return redirect("material:details", level_id=quiz.level.id)
    else:
        form = QuizForm()
    return render(request, "material/simple_form.html", {"form": form, "title": "Create Quiz"})

@login_required
@user_passes_test(is_staff)
def quiz_add_question(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == "POST":
        q_form = QuizQuestionForm(request.POST)
        if q_form.is_valid():
            question = q_form.save(commit=False)
            question.quiz = quiz
            question.save()
            messages.success(request, "Question added. Now add answers.")
            return redirect("material:quiz_add_answers", question_id=question.id)
    else:
        q_form = QuizQuestionForm(initial={"quiz": quiz})
    return render(request, "material/simple_form.html", {"form": q_form, "title": f"Add Question to {quiz.title}"})

@login_required
@user_passes_test(is_staff)
def quiz_add_answers(request, question_id):
    question = get_object_or_404(QuizQuestion, id=question_id)
    if request.method == "POST":
        form = QuizAnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.save()
            messages.success(request, "Answer added.")
            return redirect("material:quiz_add_answers", question_id=question.id)
    else:
        form = QuizAnswerForm(initial={"question": question})
    return render(request, "material/quiz_add_answers.html", {
        "form": form,
        "question": question,
        "answers": question.answers.all(),
    })

@login_required
def quiz_submit(request, level_id):
    if request.method != "POST":
        return redirect("material:details", level_id=level_id)

    level = get_object_or_404(Level, id=level_id)
    quiz = get_object_or_404(Quiz, id=request.POST.get("quiz_id"), level=level)

    correct = 0
    total = 0
    wrong_questions = []

    for question in quiz.questions.all():
        total += 1
        answers = question.answers.all()

        if question.question_type in ["single", "truefalse"]:
            chosen_id = request.POST.get(f"question_{question.id}")
            if chosen_id:
                chosen = get_object_or_404(QuizAnswer, id=chosen_id)
                if chosen.is_correct:
                    correct += 1
                else:
                    wrong_questions.append({
                        "question": question,
                        "your_answers": [chosen],
                        "correct_answers": [a for a in answers if a.is_correct],
                    })
        elif question.question_type == "multiple":
            chosen_ids = request.POST.getlist(f"question_{question.id}")
            chosen = list(QuizAnswer.objects.filter(id__in=chosen_ids, question=question))
            correct_answers = list(answers.filter(is_correct=True))
            if set(chosen) == set(correct_answers):
                correct += 1
            else:
                wrong_questions.append({
                    "question": question,
                    "your_answers": chosen,
                    "correct_answers": correct_answers,
                })

    if total > 0:
        honor = ensure_honor_entry(request.user)
        if honor:
            honor.score += correct * 10
            honor.save()
        messages.success(request, f"You got {correct}/{total} correct. +{correct*10} points")
    else:
        messages.warning(request, "No answers submitted.")

    return render(request, "material/quiz_result.html", {
        "quiz": quiz,
        "correct": correct,
        "total": total,
        "wrong_questions": wrong_questions,
    })


@login_required
@user_passes_test(is_staff)
def quiz_builder(request, level_id=None):
    from .models import Level, Quiz, QuizQuestion, QuizAnswer

    if request.method == "POST":
        title = request.POST.get("title")
        level_id_post = request.POST.get("level") or level_id
        level = get_object_or_404(Level, id=level_id_post)

        quiz = Quiz.objects.create(title=title, level=level)

        q_count = int(request.POST.get("question_count", 0))
        for i in range(1, q_count + 1):
            q_text = request.POST.get(f"question_{i}_text")
            q_type = request.POST.get(f"question_{i}_type")
            if not q_text:
                continue
            question = QuizQuestion.objects.create(
                quiz=quiz,
                text=q_text,
                question_type=q_type or "single"
            )

            a_count = int(request.POST.get(f"question_{i}_answer_count", 0))
            for j in range(1, a_count + 1):
                a_text = request.POST.get(f"question_{i}_answer_{j}_text")
                is_correct = request.POST.get(f"question_{i}_answer_{j}_correct") == "on"
                if a_text:
                    QuizAnswer.objects.create(
                        question=question,
                        text=a_text,
                        is_correct=is_correct
                    )

        messages.success(request, "Quiz created successfully with questions & answers.")
        return redirect("material:details", level_id=level.id)

    return render(request, "material/quiz_builder.html", {
        "levels": Level.objects.all(),
        "level_id": level_id,
    })



# ── Q&A ────────────────────────────────────────────────────────────────────────
def add_question(request, level_id):
    level = get_object_or_404(Level, id=level_id)
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            q = form.save(commit=False)
            q.level = level
            if request.user.is_authenticated:
                q.author_user = request.user
                if not q.author:
                    q.author = request.user.username
            q.save()
            messages.success(request, "Question added.")
    return redirect("material:details", level_id=level_id)

def add_reply(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == "POST":
        form = ReplyForm(request.POST)
        if form.is_valid():
            r = form.save(commit=False)
            r.question = question
            if request.user.is_authenticated:
                r.author_user = request.user
                if not r.author:
                    r.author = request.user.username
            r.save()
            messages.success(request, "Reply added.")
    return redirect("material:details", level_id=question.level.id)

def upvote_reply(request, reply_id):
    reply = get_object_or_404(Reply, id=reply_id)
    reply.upvotes += 1
    reply.save()
    if reply.author_user:
        honor = ensure_honor_entry(reply.author_user)
        if honor:
            honor.score += 1
            honor.save()
    messages.success(request, "Upvoted.")
    return redirect("material:details", level_id=reply.question.level.id)
