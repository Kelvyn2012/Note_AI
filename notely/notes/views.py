from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Note
from .forms import NoteForm
from .utils import summarize_text
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


def home(request):
    # Get all notes with ordering (pinned first, then by creation date)
    notes_list = Note.objects.all()

    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        notes_list = notes_list.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(category__icontains=search_query)
        )

    # Category filter
    category_filter = request.GET.get('category', '')
    if category_filter:
        notes_list = notes_list.filter(category=category_filter)

    # Color filter
    color_filter = request.GET.get('color', '')
    if color_filter:
        notes_list = notes_list.filter(color=color_filter)

    # Favorites filter
    if request.GET.get('favorites') == 'true':
        notes_list = notes_list.filter(is_favorite=True)

    # Get unique categories for filter dropdown
    categories = Note.objects.values_list('category', flat=True).distinct().exclude(category__isnull=True).exclude(category='')

    # Pagination
    paginator = Paginator(notes_list, 12)  # Show 12 notes per page
    page_number = request.GET.get('page')
    notes = paginator.get_page(page_number)

    context = {
        'notes': notes,
        'categories': categories,
        'search_query': search_query,
        'category_filter': category_filter,
        'color_filter': color_filter,
        'total_notes': notes_list.count(),
    }
    return render(request, "notes/home.html", context)


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

def toggle_pin(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    note.is_pinned = not note.is_pinned
    note.save()
    return redirect('home')

def toggle_favorite(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    note.is_favorite = not note.is_favorite
    note.save()
    return redirect('home')
