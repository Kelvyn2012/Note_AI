from django.shortcuts import get_object_or_404, render, redirect
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
            note.summary = summarize_text(note.content)
            note.save()
            return redirect("home")
    else:
        form = NoteForm()
    return render(request, "notes/add_note.html", {"form": form})

def edit_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            updated_note = form.save(commit=False)
            updated_note.summary = summarize_text(updated_note.content)
            updated_note.save()
            return redirect('home')
    else:
        form = NoteForm(instance=note)
    return render(request, 'notes/edit_note.html', {'form': form})

def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    note.delete()
    return redirect('home')
