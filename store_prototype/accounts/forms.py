from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms


class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['username',
                  'password1',
                  'password2',
                  'first_name',
                  'last_name',
                  'email']
class UserChangeForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'birth_date']
        labels = {'first_name': 'Имя', 'last_name': 'Фамилия', 'email': 'Email',
                  'birth_date': 'день рождения'}
