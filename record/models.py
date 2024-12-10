import random
from django.db import models
from datetime import datetime
import uuid

class EquipmentCategory(models.Model):
    """Категория оборудования"""

    category_code = models.CharField(max_length=10, primary_key=True, verbose_name="Код категории оборудования", editable=False, blank=True)
    name = models.CharField(max_length=256, verbose_name="Наименование")
    depreciation_rate = models.FloatField(verbose_name="Процент амортизационных отчислений")

    class Meta:
        verbose_name = "Категория оборудования"
        verbose_name_plural = "Категории оборудования"
        db_table = "equipment_category"

    def save(self, *args, **kwargs):
        if not self.category_code:
            # Генерация уникального 10-значного кода
            while True:
                new_code = ''.join([str(random.randint(0, 9)) for _ in range(10)])
                if not EquipmentCategory.objects.filter(category_code=new_code).exists():
                    self.category_code = new_code
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return self.category_code


class Equipment(models.Model):
    """Оборудование"""

    equipment_code = models.CharField(
        max_length=10, 
        primary_key=True, 
        verbose_name="Код оборудования", 
        editable=False,
        blank=True
    )
    name = models.CharField(max_length=256, verbose_name="Наименование")

    class Meta:
        verbose_name = "Оборудование"
        verbose_name_plural = "Оборудование"
        db_table = "equipment"

    def save(self, *args, **kwargs):
        if not self.equipment_code:
            # Генерация уникального 10-значного кода
            while True:
                new_code = ''.join([str(random.randint(0, 9)) for _ in range(10)])
                if not Equipment.objects.filter(equipment_code=new_code).exists():
                    self.equipment_code = new_code
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return self.equipment_code

class Department(models.Model):
    """Подразделения"""

    department_code = models.CharField(
        max_length=10, 
        primary_key=True, 
        verbose_name="Код подразделения", 
        editable=False,
        blank=True
    )
    name = models.CharField(max_length=256, verbose_name="Наименование")
    # По сути связи здесь не должно быть, надо подумать над кодом
    manager_code = models.ForeignKey(
        'Employee', # добавить еще модель с руководителями
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name="Код работника руководителя", 
        related_name="managed_departments"
    )

    class Meta:
        verbose_name = "Подразделение"
        verbose_name_plural = "Подразделения"
        db_table = "department"

    def save(self, *args, **kwargs):
        if not self.department_code:
            # Генерация уникального 10-значного кода
            while True:
                new_code = ''.join([str(random.randint(0, 9)) for _ in range(10)])
                if not Department.objects.filter(department_code=new_code).exists():
                    self.department_code = new_code
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return self.department_code


class Employee(models.Model):
    """Работники"""

    employee_code = models.CharField(
        max_length=10, 
        primary_key=True, 
        verbose_name="Код работника", 
        editable=False,
        blank=True,
        
    )
    full_name = models.CharField(max_length=256, verbose_name="ФИО")
    department_code = models.ForeignKey(
        Department, 
        on_delete=models.CASCADE, 
        verbose_name="Код подразделения", 
        related_name="employees"
    )

    class Meta:
        verbose_name = "Работник"
        verbose_name_plural = "Работники"
        db_table = "employee"

    def save(self, *args, **kwargs):
        if not self.employee_code:
            # Генерация уникального 10-значного кода
            while True:
                new_code = ''.join([str(random.randint(0, 9)) for _ in range(10)])
                if not Employee.objects.filter(employee_code=new_code).exists():
                    self.employee_code = new_code
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return self.employee_code

class InventoryCard(models.Model):
    """Инвентарная карточка"""

    COMPLETENESS_CHOICES = [
        ('Полная комплектация', 'Полная комплектация'),
        ('Частичная комплектация', 'Частичная комплектация'),
        ('Неполная комплектация', 'Неполная комплектация'),
    ]

    card_number = models.CharField(
        max_length=10, 
        primary_key=True, 
        verbose_name="Номер карточки", 
        editable=False,
        blank=True,
        
    )
    equipment_code = models.ForeignKey(Equipment, on_delete=models.CASCADE, verbose_name="Код оборудования")
    completeness_sign = models.CharField(max_length=50, verbose_name="Признак комплектности", choices=COMPLETENESS_CHOICES)
    category_code = models.ForeignKey(EquipmentCategory, on_delete=models.CASCADE, verbose_name="Код категории оборудования")
    initial_cost = models.FloatField(verbose_name="Первоначальная стоимость")
    total_depreciation_amount = models.FloatField(verbose_name="Общая сумма амортизаций")
    release_date = models.DateField(verbose_name="Дата выпуска оборудования")
    commissioning_date = models.DateField(verbose_name="Дата ввода в эксплуатацию")
    department_code = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name="Код подразделения")
    employee_code = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="Код работника")

    class Meta:
        verbose_name = 'Инвентарная карточка'
        verbose_name_plural = 'Инвентарные карточки'
        db_table = "inventory_card"

    def save(self, *args, **kwargs):
        if not self.card_number:
            # Получение последнего номера карточки
            last_card = InventoryCard.objects.order_by('-card_number').first()
            if last_card and last_card.card_number.isdigit():
                next_number = int(last_card.card_number) + 1
            else:
                next_number = 1
            # Форматирование номера в виде 0001, 0002 и т.д.
            self.card_number = f"{next_number:04}"
        super().save(*args, **kwargs)


    def __str__(self):
        return self.card_number


class Completeness(models.Model):
    """Комплектность"""

    card_number = models.ForeignKey(
        InventoryCard, 
        on_delete=models.CASCADE, 
        verbose_name="Номер карточки", 
        related_name="completeness"
    )
    position_number = models.CharField(
        max_length=10, 
        verbose_name="Номер позиции", 
        editable=False,
        blank=True
    )
    name = models.CharField(max_length=256, verbose_name="Наименование")
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    note = models.TextField(verbose_name="Примечание")

    class Meta:
        verbose_name = "Комплектность"
        verbose_name_plural = "Комплектности"
        db_table = "completeness"
        unique_together = ("position_number",)

    def save(self, *args, **kwargs):
        if not self.position_number:
            # Определяем последний номер позиции для данной карточки
            last_position = Completeness.objects.filter(card_number=self.card_number).order_by('-position_number').first()
            if last_position and last_position.position_number.isdigit():
                next_position = int(last_position.position_number) + 1
            else:
                next_position = 1
            # Форматируем номер позиции в виде 001, 002, ...
            self.position_number = f"{next_position:03}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.position_number



class Accrual(models.Model):
    """Начисления"""

    MONTH_CHOICES = [
        (1, "Январь"),
        (2, "Февраль"),
        (3, "Март"),
        (4, "Апрель"),
        (5, "Май"),
        (6, "Июнь"),
        (7, "Июль"),
        (8, "Август"),
        (9, "Сентябрь"),
        (10, "Октябрь"),
        (11, "Ноябрь"),
        (12, "Декабрь"),
    ]

    CURRENT_YEAR = datetime.now().year
    YEAR_CHOICES = [(year, str(year)) for year in range(CURRENT_YEAR - 10, CURRENT_YEAR + 1)]

    card_number = models.ForeignKey(InventoryCard, on_delete=models.CASCADE, verbose_name="Номер карточки", related_name="accruals")
    amount = models.FloatField(default=0, verbose_name="Сумма начислений")
    month = models.PositiveIntegerField(choices=MONTH_CHOICES, verbose_name="Месяц", blank=True)
    year = models.PositiveIntegerField(choices=YEAR_CHOICES, verbose_name="Год", blank=True)

    class Meta:
        verbose_name = "Начисление"
        verbose_name_plural = "Начисления"
        db_table = "accrual"
        unique_together = ("card_number", "month", "year")


    def __str__(self):
        return f"{self.month}/{self.year}"

