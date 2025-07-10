import datetime
from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Email',
                               widget=forms.TextInput(attrs={'class':'for-input'}))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'class':'for-input'}))

    

    # class Meta:
    #     model = get_user_model()
    #     fields = ['username', 'password']

class RegisteruserForm(UserCreationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={'class':'for-input'}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class':'for-input'}), )
    password2 = forms.CharField(label="Повтор пароля", widget=forms.PasswordInput(attrs={'class':'for-input'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        labels = {
            'email':'E-mail',
            'first_name':'Имя',
            'last_name':'Фамилия',
        }
        widgets = {
            'email':forms.TextInput(attrs={'class':'for-input'}),
            'first_name':forms.TextInput(attrs={'class':'for-input'}),
            'last_name':forms.TextInput(attrs={'class':'for-input'}),
        } 



    
    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Такой мейл уже существует')
        return email
    

class ProfileUsersForm(forms.ModelForm):
    username = forms.CharField(
        disabled=True,
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'for-input'})
    )
    email = forms.EmailField(
        disabled=True,
        required=False,
        label='E-mail',
        widget=forms.EmailInput(attrs={'class': 'for-input'})
    )
    this_year = datetime.date.today().year
    date_birth = forms.DateField(widget=forms.SelectDateWidget(
            years=tuple(range(this_year - 100, this_year - 4))))

    class Meta:
        model = get_user_model()
        fields = ['photo','username', 'email', 'date_birth', 'first_name', 'last_name']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'for-input'}),
            'last_name': forms.TextInput(attrs={'class': 'for-input'}),
        }

class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Старый пароль",widget=forms.PasswordInput(attrs={'class': 'for-input'}))
    new_password1 = forms.CharField(label="Новый пароль",widget=forms.PasswordInput(attrs={'class': 'for-input'}))
    new_password2 = forms.CharField(label="Подтверждение пароля",widget=forms.PasswordInput(attrs={'class': 'for-input'}))