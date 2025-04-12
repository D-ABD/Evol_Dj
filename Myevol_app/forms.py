from django import forms
from .models import JournalEntry, Objective

class JournalEntryForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        fields = ['content', 'mood', 'category']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': "Décris ton accomplissement..."
            }),
            'mood': forms.NumberInput(attrs={
                'type': 'range',
                'min': 1,
                'max': 10,
                'class': 'form-range',
                'oninput': "updateEmoji(this.value)"
            }),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ObjectiveForm(forms.ModelForm):
    class Meta:
        model = Objective
        fields = ['title', 'category', 'target_date', 'done']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'target_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'done': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
