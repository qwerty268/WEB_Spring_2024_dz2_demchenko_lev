from PIL import Image
from django import forms
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile


from app.models import Profile
from askme_demchenko.settings import MEDIA_ROOT


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}))
    repeat_password = forms.CharField(label='Repeat password',
                                      widget=forms.PasswordInput(attrs={'placeholder': 'Repeat your password'}))
    avatar = forms.ImageField(label='Avatar', required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'repeat_password', 'avatar']  # Добавить поле 'avatar' в форму

    def save(self, commit=True):
        user = super().save(commit=False)

        user.set_password(self.cleaned_data['password'])

        user.save()

        # Создаем профиль и сохраняем avatar
        print(self.cleaned_data.get('avatar'))
        profile = Profile.objects.create(user=user, avatar=self.cleaned_data.get('avatar'))
        profile.save()

        return user
