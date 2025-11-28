from django import forms
from .models import Note


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["title", "content", "category", "color", "is_pinned", "is_favorite"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter note title..."
            }),
            "content": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 8,
                "placeholder": "Write your note here..."
            }),
            "category": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "e.g., Work, Personal, Ideas..."
            }),
            "color": forms.Select(attrs={"class": "form-select"}),
            "is_pinned": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_favorite": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {
            "title": "Note Title",
            "content": "Content",
            "category": "Category (Optional)",
            "color": "Note Color",
            "is_pinned": "Pin this note to top",
            "is_favorite": "Mark as favorite",
        }
