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
                return redirect('inventory_card_list')  # Редирект на список инвентарных карточек
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

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import InventoryCard

class InventoryCardUpdateView(UpdateView):
    model = InventoryCard
    template_name = 'add_del/inventory_card_form.html'
    fields = [
        'equipment_code', 
        'completeness_sign', 
        'category_code', 
        'initial_cost', 
        'total_depreciation_amount', 
        'release_date', 
        'commissioning_date', 
        'department_code', 
        'employee_code'
    ]
    success_url = reverse_lazy('inventory_card_list')

class InventoryCardDeleteView(DeleteView):
    model = InventoryCard
    template_name = 'add_del/inventory_card_confirm_delete.html'
    success_url = reverse_lazy('inventory_card_list')

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

from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy

class DepartmentUpdateView(UpdateView):
    model = Department
    template_name = 'add_del/department_edit.html'
    fields = ['name', 'manager_code']
    success_url = reverse_lazy('department_list')  # Перенаправление после редактирования

class DepartmentDeleteView(DeleteView):
    model = Department
    template_name = 'add_del/department_confirm_delete.html'
    success_url = reverse_lazy('department_list')  # Перенаправление после удаления


from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Completeness

class CompletenessCreateView(CreateView):
    model = Completeness
    template_name = 'add_del/completeness_add.html'
    fields = ['card_number', 'name', 'quantity', 'note']
    success_url = reverse_lazy('completeness_list')


# Представление для других моделей (по аналогии)
class CompletenessListView(ListView):
    model = Completeness
    template_name = 'model/completeness_list.html'
    context_object_name = 'completeness'

    def get_queryset(self):
        queryset = super().get_queryset()

        # Фильтрация по наименованию
        name_filter = self.request.GET.get('name', None)
        if name_filter:
            queryset = queryset.filter(name=name_filter)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name_choices'] = Completeness.objects.values_list('name', flat=True).distinct()
        return context

from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy

class CompletenessUpdateView(UpdateView):
    model = Completeness
    template_name = 'add_del/completeness_edit.html'
    fields = ['name', 'quantity', 'note']
    success_url = reverse_lazy('completeness_list')  # Перенаправление после редактирования

class CompletenessDeleteView(DeleteView):
    model = Completeness
    template_name = 'add_del/completeness_confirm_delete.html'
    success_url = reverse_lazy('completeness_list')  # Перенаправление после удаления


class AccrualListView(ListView):
    model = Accrual
    template_name = 'model/accrual_list.html'
    context_object_name = 'accruals'

    def get_queryset(self):
        queryset = super().get_queryset()

        # Фильтр по месяцу
        month = self.request.GET.get('month')
        if month:
            queryset = queryset.filter(month=month)

        # Фильтр по году
        year = self.request.GET.get('year')
        if year:
            queryset = queryset.filter(year=year)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['month_choices'] = Accrual.MONTH_CHOICES
        return context


from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, DeleteView

class AccrualUpdateView(UpdateView):
    model = Accrual
    template_name = 'add_del/accrual_edit.html'
    fields = ['card_number', 'amount', 'month', 'year']
    success_url = reverse_lazy('accrual_list')

class AccrualDeleteView(DeleteView):
    model = Accrual
    template_name = 'add_del/accrual_confirm_delete.html'
    success_url = reverse_lazy('accrual_list')


class EquipmentListView(ListView):
    model = Equipment
    template_name = 'model/equipment_list.html'
    context_object_name = 'equipment'

from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, DeleteView

class EquipmentUpdateView(UpdateView):
    model = Equipment
    template_name = 'add_del/equipment_edit.html'
    fields = ['name']
    success_url = reverse_lazy('equipment_list')

class EquipmentDeleteView(DeleteView):
    model = Equipment
    template_name = 'add_del/equipment_confirm_delete.html'
    success_url = reverse_lazy('equipment_list')


from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Equipment

class EquipmentCreateView(CreateView):
    model = Equipment
    template_name = 'add_del/equipment_form.html'
    fields = ['name']
    success_url = reverse_lazy('equipment_list')


class EquipmentCategoryListView(ListView):
    model = EquipmentCategory
    template_name = 'model/equipment_category_list.html'
    context_object_name = 'equipment_categories'

from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, DeleteView

class EquipmentCategoryUpdateView(UpdateView):
    model = EquipmentCategory
    template_name = 'add_del/equipment_category_edit.html'
    fields = ['name', 'depreciation_rate']
    success_url = reverse_lazy('equipment_category_list')

class EquipmentCategoryDeleteView(DeleteView):
    model = EquipmentCategory
    template_name = 'add_del/equipment_category_confirm_delete.html'
    success_url = reverse_lazy('equipment_category_list')


from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import EquipmentCategory

class EquipmentCategoryCreateView(CreateView):
    model = EquipmentCategory
    template_name = 'add_del/equipment_category_form.html'
    fields = ['name', 'depreciation_rate']
    success_url = reverse_lazy('equipment_category_list')


class EmployeeListView(ListView):
    model = Employee
    template_name = 'model/employee_list.html'
    context_object_name = 'employees'

from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, DeleteView

class EmployeeUpdateView(UpdateView):
    model = Employee
    template_name = 'add_del/employee_edit.html'
    fields = ['full_name', 'department_code']
    success_url = reverse_lazy('employee_list')

class EmployeeDeleteView(DeleteView):
    model = Employee
    template_name = 'add_del/employee_confirm_delete.html'
    success_url = reverse_lazy('employee_list')


from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Employee

class EmployeeCreateView(CreateView):
    model = Employee
    template_name = 'add_del/employee_form.html'
    fields = ['full_name', 'department_code']
    success_url = reverse_lazy('employee_list')


#  Удаление и добавление
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import InventoryCard

from .forms import InventoryCardForm

class InventoryCardCreateView(CreateView):
    model = InventoryCard
    template_name = 'add_del/inventory_card_form.html'
    form_class = InventoryCardForm
    success_url = reverse_lazy('inventory_card_list')
 # URL перенаправления после успешного добавления

from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Department

class DepartmentCreateView(CreateView):
    model = Department
    template_name = 'add_del/department_form.html'
    fields = ['name', 'manager_code']  # Поля, которые пользователь заполняет
    success_url = reverse_lazy('department_list')  # Перенаправление после добавления

class AccrualCreateView(CreateView):
    model = Accrual
    template_name = 'add_del/accrual_form.html'
    fields = ['card_number', 'amount', 'month', 'year']
    success_url = reverse_lazy('accrual_list')

# Запросы

from django.db.models import Sum
from django.utils.timezone import now
from django.views.generic import TemplateView
from .models import InventoryCard, Department

class CurrentYearCostByDepartmentView(TemplateView):
    template_name = 'requests/current_year_cost_by_department.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_year = now().year

        # Группировка и суммирование первоначальной стоимости по участкам
        data = (
            InventoryCard.objects.filter(commissioning_date__year=current_year)
            .values('department_code__name')  # Имя участка
            .annotate(total_cost=Sum('initial_cost'))  # Сумма стоимости
            .order_by('department_code__name')  # Сортировка по имени участка
        )

        context['data'] = data
        context['current_year'] = current_year
        return context

from django.views.generic import TemplateView
from django.utils.timezone import now
from .models import InventoryCard

class CurrentYearCompletenessCountView(TemplateView):
    template_name = 'requests/current_year_completeness_count.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_year = now().year

        # Получение комплектных изделий
        inventory_cards = InventoryCard.objects.filter(
            commissioning_date__year=current_year,
            completeness_sign="Полная комплектация"
        )

        context['inventory_cards'] = inventory_cards
        context['completeness_count'] = inventory_cards.count()
        context['current_year'] = current_year
        return context


from django.views.generic import TemplateView
from .models import Equipment

class EquipmentContainingTolView(TemplateView):
    template_name = 'requests/equipment_containing_tol.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Запрос оборудования с названием, содержащим "тол" (регистронезависимый поиск)
        equipment_list = Equipment.objects.filter(name__icontains="тол")
        context['equipment_list'] = equipment_list
        return context

from django.http import HttpResponseBadRequest

class EquipmentInRangeView(TemplateView):
    template_name = 'requests/equipment_in_range.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        equipment_list = InventoryCard.objects.all().order_by('card_number')

        # Получаем уникальные значения номеров карточек для выпадающих списков
        card_numbers = list(equipment_list.values_list('card_number', flat=True))

        # Получаем выбранные диапазоны
        start_range = self.request.GET.get('start_range', None)
        end_range = self.request.GET.get('end_range', None)

        # Проверка и фильтрация
        if start_range and end_range:
            if start_range > end_range:
                context['error'] = "Начало диапазона не может быть больше конца."
            else:
                equipment_list = equipment_list.filter(
                    card_number__gte=start_range,
                    card_number__lte=end_range
                )
        else:
            equipment_list = InventoryCard.objects.none()  # Пустой результат по умолчанию

        context['equipment_list'] = equipment_list
        context['card_numbers'] = card_numbers
        context['start_range'] = start_range
        context['end_range'] = end_range
        return context

from django.views.generic import TemplateView
from django.db.models import Sum
from datetime import datetime

class DepreciationSumView(TemplateView):
    template_name = 'requests/depreciation_sum.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получение текущего месяца
        selected_month = self.request.GET.get('month', datetime.now().month)

        # Сумма амортизационных отчислений за выбранный месяц
        depreciation_sum = Accrual.objects.filter(month=selected_month).aggregate(total_sum=Sum('amount'))['total_sum']

        context['depreciation_sum'] = depreciation_sum or 0
        context['month_choices'] = Accrual.MONTH_CHOICES
        context['selected_month'] = int(selected_month)
        context['month_name'] = dict(Accrual.MONTH_CHOICES).get(int(selected_month), "неизвестный")
        return context



# Отчеты

from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import InventoryCard
from django.db.models import Q
import pdfkit
from datetime import datetime

def inventory_card_report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Базовый QuerySet
    inventory_cards = InventoryCard.objects.all()

    # Применение фильтрации по диапазону дат
    if start_date or end_date:
        try:
            if start_date:
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            if end_date:
                end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

            if start_date and end_date:
                inventory_cards = inventory_cards.filter(
                    Q(commissioning_date__gte=start_date) & Q(commissioning_date__lte=end_date)
                )
            elif start_date:
                inventory_cards = inventory_cards.filter(commissioning_date__gte=start_date)
            elif end_date:
                inventory_cards = inventory_cards.filter(commissioning_date__lte=end_date)

        except ValueError:
            pass  # Пропускаем фильтрацию, если даты некорректны

    context = {
        'inventory_cards': inventory_cards,
        'start_date': start_date,
        'end_date': end_date,
    }

    if 'pdf' in request.GET:  # Генерация PDF
        html = render_to_string('report/inventory_card_report_pdf.html', context)
        config = pdfkit.configuration(wkhtmltopdf='D:/Python_project/Coursework_bd/wkhtmltox/bin/wkhtmltopdf.exe')
        pdf = pdfkit.from_string(html, False, configuration=config, options={
            'page-size': 'A4',
            'encoding': "UTF-8",
        })
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="inventory_card_report.pdf"'
        return response

    return render(request, 'report/inventory_card_report.html', context)


from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
import pdfkit
from .models import InventoryCard
from django.db.models import F


def equipment_writeoff_report(request):
    # Выбираем оборудование, подлежащее списанию
    writeoff_equipment = InventoryCard.objects.filter(
        initial_cost=F('total_depreciation_amount')
    )

    context = {
        'writeoff_equipment': writeoff_equipment,
    }

    if 'pdf' in request.GET:  # Генерация PDF
        html = render_to_string('report/equipment_writeoff_report_pdf.html', context)
        config = pdfkit.configuration(wkhtmltopdf='D:/Python_project/Coursework_bd/wkhtmltox/bin/wkhtmltopdf.exe')
        pdf = pdfkit.from_string(html, False, configuration=config, options={
            'page-size': 'A4',
            'encoding': "UTF-8",
        })
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="equipment_writeoff_report.pdf"'
        return response

    return render(request, 'report/equipment_writeoff_report.html', context)


from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
import pdfkit
from .models import InventoryCard, Employee


def equipment_by_employee_report(request):
    # Получаем ID сотрудника из GET-параметров
    employee_id = request.GET.get('employee_id', None)

    equipment_list = []
    employee = None

    if employee_id:
        try:
            # Находим сотрудника
            employee = Employee.objects.get(pk=employee_id)
            # Фильтруем оборудование, закрепленное за сотрудником
            equipment_list = InventoryCard.objects.filter(employee_code=employee)
        except Employee.DoesNotExist:
            employee = None

    context = {
        'equipment_list': equipment_list,
        'employee': employee,
        'employees': Employee.objects.all(),  # Для выпадающего списка
    }

    if 'pdf' in request.GET:  # Генерация PDF
        html = render_to_string('report/equipment_by_employee_report_pdf.html', context)
        config = pdfkit.configuration(wkhtmltopdf='D:/Python_project/Coursework_bd/wkhtmltox/bin/wkhtmltopdf.exe')
        pdf = pdfkit.from_string(html, False, configuration=config, options={
            'page-size': 'A4',
            'encoding': "UTF-8",
        })
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="equipment_by_employee_report.pdf"'
        return response

    return render(request, 'report/equipment_by_employee_report.html', context)


# Процедуры
from django.db import connection
from django.shortcuts import render

def mismatched_years_view(request):
    # Вызов хранимой процедуры
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM get_mismatched_years()")
        rows = cursor.fetchall()

    context = {
        'rows': rows
    }

    return render(request, 'procedure/mismatched_years.html', context)





from django.shortcuts import render
from django.db import connection

def inventory_by_category(request):
    category_code = request.GET.get('category_code')  # Получаем параметр из запроса
    inventory_list = []

    if category_code:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM get_inventory_by_category(%s)", [category_code])
            columns = [col[0] for col in cursor.description]
            inventory_list = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return render(request, 'procedure/inventory_by_category.html', {
        'inventory_list': inventory_list,
        'category_code': category_code,
    })



from django.shortcuts import render
from django.db import connection

def insert_employees_procedure(request):
    with connection.cursor() as cursor:
        cursor.callproc('insert_employees')  # Вызов хранимой процедуры
    return render(request, 'procedure/insert_employees.html', {})


from django.shortcuts import render
from django.db import connection
from .models import InventoryCard

def equipment_downtime_view(request):
    card_number_param = request.GET.get('card_number', None)
    downtime_data = []

    if card_number_param:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT card_number, equipment_code_id, release_date, commissioning_date, downtime_interval
                FROM calculate_equipment_downtime(%s)
            """, [card_number_param])
            downtime_data = cursor.fetchall()

    # Получение всех номеров карточек для выпадающего списка
    card_choices = InventoryCard.objects.values_list('card_number', flat=True)

    return render(request, 'procedure/equipment_downtime.html', {
        'downtime_data': downtime_data,
        'card_number_param': card_number_param,
        'card_choices': card_choices,
    })
