from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from django.views.generic import ListView
from .models import (
    InventoryCard, Completeness, Department, Accrual,
    Equipment, EquipmentCategory, Employee
)
from django.db.models import Q

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


# Представление для InventoryCard
class InventoryCardListView(ListView):
    model = InventoryCard
    template_name = 'model/inventory_card_list.html'
    context_object_name = 'inventory_cards'

    def get_queryset(self):
        queryset = super().get_queryset()

        # Фильтр по признаку комплектности
        inventory_filter = self.request.GET.get('completeness_sign', None)
        if inventory_filter:
            queryset = queryset.filter(completeness_sign=inventory_filter)

        # Фильтрация по диапазону дат
        start_date = self.request.GET.get('start_date', None)
        end_date = self.request.GET.get('end_date', None)

        if start_date and end_date:
            queryset = queryset.filter(
                Q(commissioning_date__gte=start_date) & Q(commissioning_date__lte=end_date)
            )
        elif start_date:
            queryset = queryset.filter(commissioning_date__gte=start_date)
        elif end_date:
            queryset = queryset.filter(commissioning_date__lte=end_date)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['completeness_sign_choices'] = InventoryCard.COMPLETENESS_CHOICES
        return context


# Представление для Department
class DepartmentListView(ListView):
    model = Department
    template_name = 'model/department_list.html'
    context_object_name = 'departments'

    def get_queryset(self):
        queryset = super().get_queryset()
        department_filter = self.request.GET.get('department_code', None)
        if department_filter:
            queryset = queryset.filter(department_code=department_filter)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['department_choices'] = Department.objects.values_list('department_code', flat=True).distinct()
        return context


# Представление для других моделей (по аналогии)
class CompletenessListView(ListView):
    model = Completeness
    template_name = 'model/completeness_list.html'
    context_object_name = 'completeness'


class AccrualListView(ListView):
    model = Accrual
    template_name = 'model/accrual_list.html'
    context_object_name = 'accruals'


class EquipmentListView(ListView):
    model = Equipment
    template_name = 'model/equipment_list.html'
    context_object_name = 'equipment'


class EquipmentCategoryListView(ListView):
    model = EquipmentCategory
    template_name = 'model/equipment_category_list.html'
    context_object_name = 'equipment_categories'


class EmployeeListView(ListView):
    model = Employee
    template_name = 'model/employee_list.html'
    context_object_name = 'employees'



#  Удаление и добавление
# from django.views.generic.edit import CreateView, DeleteView
# from django.urls import reverse_lazy

# class InventoryCardCreateView(CreateView):
#     model = InventoryCard
#     template_name = 'add_del/inventory_card_form.html'
#     fields = [
#         'card_number', 'equipment_code', 'completeness_sign',
#         'category_code', 'initial_cost', 'total_depreciation_amount',
#         'release_date', 'commissioning_date', 'department_code', 'employee_code'
#     ]
#     success_url = reverse_lazy('inventory_card_list')  # Перенаправление после успешного добавления

# class InventoryCardDeleteView(DeleteView):
#     model = InventoryCard
#     template_name = 'add_del/inventory_card_confirm_delete.html'
#     success_url = reverse_lazy('inventory_card_list')  # Перенаправление после успешного удаления

# class DepartmentCreateView(CreateView):
#     model = Department
#     template_name = 'add_del/department_form.html'
#     fields = ['department_code', 'name', 'manager_code']  # Поля, которые пользователь может заполнить
#     success_url = reverse_lazy('department_list')  # Перенаправление после успешного добавления

# class DepartmentDeleteView(DeleteView):
#     model = Department
#     template_name = 'add_del/department_confirm_delete.html'
#     success_url = reverse_lazy('department_list')  # Перенаправление после успешного удаления




# Отчеты

# from django.shortcuts import render
# from django.http import HttpResponse
# from django.template.loader import render_to_string
# import pdfkit
# from .models import InventoryCard
# from django.db.models import Q
# import pdfkit

# import pdfkit
# from datetime import datetime

# def inventory_card_report(request):
#     start_date = request.GET.get('start_date')
#     end_date = request.GET.get('end_date')
    
#     # Базовый QuerySet
#     inventory_cards = InventoryCard.objects.all()

#     # Применение фильтрации только если даты заданы корректно
#     if start_date or end_date:
#         try:
#             if start_date:
#                 # Преобразование строки в объект даты для проверки формата
#                 start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
#             if end_date:
#                 # Преобразование строки в объект даты для проверки формата
#                 end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

#             # Применение фильтров
#             if start_date and end_date:
#                 inventory_cards = inventory_cards.filter(
#                     Q(commissioning_date__gte=start_date) & Q(commissioning_date__lte=end_date)
#                 )
#             elif start_date:
#                 inventory_cards = inventory_cards.filter(commissioning_date__gte=start_date)
#             elif end_date:
#                 inventory_cards = inventory_cards.filter(commissioning_date__lte=end_date)

#         except ValueError:
#             # Если формат даты неверный, пропускаем фильтрацию
#             pass

#     context = {
#         'inventory_cards': inventory_cards,
#         'start_date': start_date,
#         'end_date': end_date,
#     }

#     if 'pdf' in request.GET:  # Если нужно сгенерировать PDF
#         html = render_to_string('report/inventory_card_report_pdf.html', context)
#         # Укажите путь к wkhtmltopdf
#         config = pdfkit.configuration(wkhtmltopdf='D:/Python_project/Coursework_bd/wkhtmltox/bin/wkhtmltopdf.exe')  # Укажите правильный путь
#         pdf = pdfkit.from_string(html, False, configuration=config, options={
#             'page-size': 'A4',
#             'encoding': "UTF-8",
#         })
#         response = HttpResponse(pdf, content_type='application/pdf')
#         response['Content-Disposition'] = 'attachment; filename="inventory_card_report.pdf"'
#         return response

#     return render(request, 'report/inventory_card_report.html', context)

