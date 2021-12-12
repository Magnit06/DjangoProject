"""
Модуль форм. Здесь задаются настройки отображения форм на сайте
"""
from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from captcha import helpers, fields
from .models import Bb, Comment, CustomUser


class BbForm(forms.ModelForm):
    """
    Форма добавления объявлений
    """

    captcha = fields.CaptchaField(generator=helpers.math_challenge,
                                  label="Решите задачу с картинки",
                                  error_messages={'invalid': "Задача решена неправильно, "
                                                             "попробуйте еще раз."})

    class Meta:
        """
        Мета класс дополнительных
        настроек отображения полей формы
        добавления объявлений
        """
        model = Bb
        fields = ('author', 'slug', 'title', 'content', 'price', 'rubric')
        widgets = {'author': forms.HiddenInput, 'slug': forms.HiddenInput}


class CommentForm(forms.ModelForm):
    """
    Форма добавления комментариев
    """

    captcha = fields.CaptchaField(generator=helpers.math_challenge,
                                  label="Решите задачу с картинки",
                                  error_messages={'invalid': "Задача решена неправильно, "
                                                             "попробуйте еще раз."})

    class Meta:
        """
        Мета класс дополнительных
        настроек отображения полей формы
        добавления комментариев
        """
        model = Comment
        fields = ('bb', 'author', 'content')
        widgets = {'bb': forms.HiddenInput, 'author': forms.HiddenInput}


class CustomUserEditForm(forms.ModelForm):
    """
    Форма редактирования пользовательских
    данных
    """
    email = forms.EmailField(required=True,
                             label='Адрес электронной почты.')
    password1 = forms.CharField(required=True,
                                label='Пароль',
                                widget=forms.PasswordInput,
                                help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(required=True,
                                label='Пароль (повторно)',
                                help_text='Введите тот же пароль второй раз.',
                                widget=forms.PasswordInput)
    captcha = fields.CaptchaField(generator=helpers.math_challenge,
                                  label="Решите задачу с картинки",
                                  error_messages={'invalid': "Задача решена неправильно, "
                                                             "попробуйте еще раз."})

    def get_password1_cleaned(self):
        password1 = self.cleaned_data['password1']
        if password1:
            # если все хорошо return None else Exception
            password_validation.validate_password(password=password1)
        return password1

    def clean(self):
        super().clean()
        password1 = self.get_password1_cleaned()
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            errors = {'password2': ValidationError(
                'Введенные пароли не совпадают.', code='password_mismatch'
            )}
            raise ValidationError(errors)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

    class Meta:
        """
        здесь задаем параметры отображения формы
        """
        model = CustomUser
        fields = ('username', 'email',
                  'password1', 'password2',
                  'first_name', 'last_name', 'middle_name',
                  'phone')
