from django import forms
from captcha import helpers, fields
from .models import Bb, Comment


class BbForm(forms.ModelForm):

	captcha = fields.CaptchaField(generator=helpers.math_challenge, label="Решите задачу с картинки",
								  error_messages={'invalid': "Задача решена неправильно, попробуйте еще раз."})

	class Meta:
		model = Bb
		fields = ('author', 'title', 'content', 'price', 'rubric')
		widgets = {'author': forms.HiddenInput}


class CommentForm(forms.ModelForm):

	author = forms.CharField(disabled=True)
	captcha = fields.CaptchaField(generator=helpers.math_challenge, label="Решите задачу с картинки",
								  error_messages={'invalid': "Задача решена неправильно, попробуйте еще раз."})

	class Meta:
		model = Comment
		fields = ('bb', 'author', 'content')
		widgets = {'bb': forms.HiddenInput}
