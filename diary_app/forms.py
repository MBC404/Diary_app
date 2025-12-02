from django import forms
from django.contrib.auth.models import User
from .models import DiaryEntry

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password')
        p2 = cleaned.get('confirm_password')
        if p1 != p2:
            raise forms.ValidationError("Passwords do not match")
        return cleaned


class PinForm(forms.Form):
    pin = forms.CharField(
        max_length=4,
        widget=forms.PasswordInput,
        help_text="Enter 4-digit PIN"
    )

    def clean_pin(self):
        p = self.cleaned_data['pin']
        if not p.isdigit() or len(p) != 4:
            raise forms.ValidationError("PIN must be 4 digits")
        return p


class DiaryEntryForm(forms.ModelForm):
    class Meta:
        model = DiaryEntry
        fields = ['title', 'content']
