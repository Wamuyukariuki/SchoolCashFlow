from django import forms
from .models import Expense, ExpenseCategory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ExpenseForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=ExpenseCategory.objects.all(), empty_label=None)

    class Meta:
        model = Expense
        fields = ['category', 'amount', 'date', 'description']


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
