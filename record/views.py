from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import InventoryCard, Completeness, Department, Accrual, Equipment, EquipmentCategory, Employee
from .forms import LoginForm

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('model_tables')
            else:
                form.add_error(None, "Неверный логин или пароль")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def model_tables(request):
    context = {
        'inventory_cards': InventoryCard.objects.all(),
        'completeness': Completeness.objects.all(),
        'departments': Department.objects.all(),
        'accruals': Accrual.objects.all(),
        'equipment': Equipment.objects.all(),
        'equipment_categories': EquipmentCategory.objects.all(),
        'employees': Employee.objects.all(),
    }
    return render(request, 'index.html', context)







