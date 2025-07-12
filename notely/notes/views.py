from django.shortcuts import render, redirect
from .models import Note
from .forms import NoteForm
from .utils import summarize_text  # (we'll create this in step 4)
from django.contrib.auth.decorators import login_required


def home(request):
    notes = Note.objects.order_by("-created_at")
    return render(request, "notes/home.html", {"notes": notes})


def add_note(request):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.summary = "Test summary"  # <-- hardcoded to isolate issue
            note.save()
            return redirect("home")
    else:
        form = NoteForm()
    return render(request, "notes/add_note.html", {"form": form})
