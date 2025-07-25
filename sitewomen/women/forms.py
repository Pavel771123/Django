from django import forms
from .models import Husband, Category, Women
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from captcha.fields import CaptchaField

@deconstructible
class RussianValidator:
    ALLOWED_CHARS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя0123456789- '
    code = 'russian'


    def __init__(self, message= None):
        self.message = message if message else "Должны быть только русские символы"


    def __call__(self, value,*args, **kwds):
        if not (set(value)<= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, code=self.code)

class AddPostForm(forms.ModelForm):
    cat = forms.ModelChoiceField(queryset=Category.objects.all(
    ), empty_label='Категория не выбрана', label='Категории')
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(
    ), empty_label='Не замужем', required=False, label='Супруг')

    class Meta:
        model = Women
        fields =  ['title', 'slug', 'content', 'photo', 'is_published', 'cat','husband', 'tags']
        widgets = {
            'title':forms.TextInput(attrs={'class':'form-input'}),
            'content':forms.Textarea(attrs={'cols':50,'rows':5}),
        }

        labels = {'slug': 'URL',}


       
    def clean_title(self):    #Начинается clean_{имя поля}
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Должно быть не больше 50 ')
        return title
    
class UploadFileForm(forms.Form):
    file = forms.FileField(label='Файл')

class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=255)
    email = forms.EmailField(label='Email')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols':60, 'rows': 10}))
    captcha = CaptchaField()