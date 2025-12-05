from django import forms
from .models import Topic, Note

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': ''}

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}

class SearchForm(forms.Form):
    query = forms.CharField(
        label='Поиск заметок',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите ключевые слова...',
            'class': 'form-control'
        })
    )