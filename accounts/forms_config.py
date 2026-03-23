from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import PasswordChangeForm

User = get_user_model()


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['full_name', 'email']  # Remova o campo 'image'
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Seu nome completo'}),
            'email': forms.EmailInput(attrs={'placeholder': 'seuemail@exemplo.com'}),
        }



class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs['placeholder'] = 'Senha atual'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'Nova senha'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirme a nova senha'
