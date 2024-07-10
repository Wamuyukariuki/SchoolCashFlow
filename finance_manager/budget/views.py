from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from savings.models import Saving
from .models import Expense
from .forms import ExpenseForm, SignUpForm


@login_required
def dashboard(request):
    expenses = Expense.objects.filter(user=request.user)
    savings = Saving.objects.filter(user=request.user)  # Retrieve savings for the user
    context = {
        'user': request.user,
        'expenses': expenses,
        'savings': savings,  # Add savings data to the context
    }
    return render(request, 'budget/dashboard.html', context)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('dashboard')  # Redirect to the dashboard directly after signup
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user)
    return render(request, 'budget/expense_list.html', {'expenses': expenses})


@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user  # Set the user before saving
            expense.save()
            messages.success(request, 'Expense added successfully.')  # Add success message
            return redirect('expense_list')
        else:
            messages.error(request, 'Error adding expense. Please check the form.')
    else:
        form = ExpenseForm()
    return render(request, 'budget/add_expense.html', {'form': form})


@login_required
def expense_create(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save()
            return redirect('expense_list')  # Redirect to expense list after successful form submission
    else:
        form = ExpenseForm()

    return render(request, 'budget/expense_create.html', {'form': form})
