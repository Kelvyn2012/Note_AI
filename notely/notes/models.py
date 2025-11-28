from django.db import models

# Create your models here.


class Note(models.Model):
    COLOR_CHOICES = [
        ('default', 'Default'),
        ('primary', 'Blue'),
        ('success', 'Green'),
        ('warning', 'Yellow'),
        ('danger', 'Red'),
        ('info', 'Cyan'),
        ('purple', 'Purple'),
    ]

    title = models.CharField(max_length=255)
    content = models.TextField()
    summary = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, default='default')
    is_pinned = models.BooleanField(default=False)
    is_favorite = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_pinned', '-created_at']

    def __str__(self):
        return self.title
