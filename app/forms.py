from django import forms
from django.contrib.auth.models import User

from app.models import Profile, Question, Answer


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
        fields = ['username', 'email', 'password', 'repeat_password', 'avatar']  # Добавить поле 'avatar' в форму

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("repeat_password")

        if password != confirm_password:
            self.add_error("password", "Passwords must match")
            self.add_error("repeat_password", "Passwords must match")
            raise forms.ValidationError("Passwords must match")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.save()

        # Создаем профиль и сохраняем avatar
        print(self.cleaned_data.get('avatar'))
        profile = Profile.objects.create(user=user, avatar=self.cleaned_data.get('avatar'))
        profile.save()

        return user


class EditProfileForm(forms.ModelForm):
    avatar = forms.ImageField(label='Avatar', required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'avatar']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        exclude = ['user', 'created_at', 'updated_at']

    def save_with_related_data(self, user):
        question = super().save(commit=False)
        question.user = user
        question.save()

        return question


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']

    def save_with_related_data(self, user, question):
        answer = super().save(commit=False)
        answer.user = user
        answer.question = question
        answer.save()

        return answer
