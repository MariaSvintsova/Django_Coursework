from django import forms
from main.models import NewsLetter, Client


class NewsLetterForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea, required=False, label='Текст сообщения')

    class Meta:
        model = NewsLetter
        exclude = ('user', 'status', 'is_published')

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ('name', 'user')