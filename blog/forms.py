from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Post
from django.utils.translation import gettext_lazy as _


class CustomAuthenticationForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username']:
            self.fields[fieldname].label = 'Vartotojo vardas'

        for fieldname in ['password']:
            self.fields[fieldname].label = 'Slaptažodis'


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username']:
            self.fields[fieldname].label = 'Vartotojo vardas'

        for fieldname in ['email']:
            self.fields[fieldname].label = 'Elektroninis paštas'

        for fieldname in ['password1']:
            self.fields[fieldname].label = 'Slaptažodis'

        for fieldname in ['password2']:
            self.fields[fieldname].label = 'Pakartokite slaptažodį'

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ("title", "slug", "author", "content", "status")

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)

        for fieldname in ['title']:
            self.fields[fieldname].label = 'Pavadinimas'

        for fieldname in ['slug']:
            self.fields[fieldname].label = 'Draugiška nuoroda(panaši į pavadinimą)'

        for fieldname in ['author']:
            self.fields[fieldname].label = 'Autorius'

        for fieldname in ['content']:
            self.fields[fieldname].label = 'Jūsų įrašas'

        for fieldname in ['status']:
            self.fields[fieldname].label = 'Statusas'
