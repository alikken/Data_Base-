from django.db import models
import uuid
from datetime import datetime
class EquipmentCategory(models.Model):
    """Категория оборудования"""

    category_code = models.CharField(max_length=10, primary_key=True, verbose_name="Код категории оборудования", editable=True)
    name = models.CharField(max_length=50, verbose_name="Наименование")
    depreciation_rate = models.FloatField(verbose_name="Процент амортизационных отчислений")

    class Meta:
        verbose_name = "Категория оборудования"
        verbose_name_plural = "Категории оборудования"
        db_table = "equipment_category"

    def save(self, *args, **kwargs):
        if not self.category_code:
            # Генерация уникального кода (первые 8 символов UUID)
            self.category_code = str(uuid.uuid4())[:8].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category_code} - {self.name}"


class Equipment(models.Model):
    """Оборудование"""

    equipment_code = models.CharField(
        max_length=10, 
        primary_key=True, 
        verbose_name="Код оборудования", 
        editable=True
    )
    name = models.CharField(max_length=50, verbose_name="Наименование")

    class Meta:
        verbose_name = "Оборудование"
        verbose_name_plural = "Оборудование"
        db_table = "equipment"

    def save(self, *args, **kwargs):
        if not self.equipment_code:
            # Генерация уникального кода (первые 8 символов UUID)
            self.equipment_code = str(uuid.uuid4())[:8].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.equipment_code} - {self.name}"


class Boss(models.Model):
    """Код руководителя работников"""
    full_name = models.CharField(max_length=50, verbose_name="ФИО")

    class Meta:
        verbose_name = "Руководитель подразделения"
        verbose_name_plural = "Руководители подразделений"
        db_table = "manager"

    def __str__(self):
        return self.full_name


class Department(models.Model):
    """Подразделения"""

    department_code = models.CharField(
        max_length=10, 
        primary_key=True, 
        verbose_name="Код подразделения", 
        editable=True
    )
    name = models.CharField(max_length=50, verbose_name="Наименование")
    manager_code = models.ForeignKey(
        'Boss', 
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
            # Генерация уникального кода (первые 8 символов UUID)
            self.department_code = str(uuid.uuid4())[:8].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.department_code} - {self.name}"


class Employee(models.Model):
    """Работники"""

    employee_code = models.CharField(
        max_length=10, 
        primary_key=True, 
        verbose_name="Код работника", 
        editable=True,
        blank=True,
        # null=True
    )
    full_name = models.CharField(max_length=100, verbose_name="ФИО")
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
            # Генерация уникального кода (первые 8 символов UUID)
            self.employee_code = str(uuid.uuid4())[:8].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Card {self.employee_code} - {self.full_name}"

class InventoryCard(models.Model):
    """Инвентарная карточка"""

    card_number = models.CharField(
        max_length=10, 
        primary_key=True, 
        verbose_name="Номер карточки", 
        editable=True
    )
    equipment_code = models.ForeignKey(Equipment, on_delete=models.CASCADE, verbose_name="Код оборудования")
    completeness_sign = models.CharField(max_length=15, verbose_name="Признак комплектности")
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
        return f"Card {self.card_number} - {self.equipment_code}"



from django.db import models

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
        editable=True
    )
    name = models.CharField(max_length=50, verbose_name="Наименование")
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    note = models.CharField(max_length=100, verbose_name="Примечание")

    class Meta:
        verbose_name = "Комплектность"
        verbose_name_plural = "Комплектности"
        db_table = "completeness"
        unique_together = ("position_number",)

    def save(self, *args, **kwargs):
        if not self.position_number:
            # Определение следующего номера позиции для конкретной карточки
            last_position = Completeness.objects.filter(card_number=self.card_number).order_by('-position_number').first()
            if last_position and last_position.position_number.isdigit():
                next_position = int(last_position.position_number) + 1
            else:
                next_position = 1
            # Форматирование номера в виде 001, 002 и т.д.
            self.position_number = f"{next_position:03}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.card_number} - {self.position_number} - {self.name}"



class Accrual(models.Model):
    """Начисления"""

    card_number = models.ForeignKey(InventoryCard, on_delete=models.CASCADE, verbose_name="Номер карточки", related_name="accruals")
    amount = models.FloatField(default=0, verbose_name="Сумма начислений")
    month = models.PositiveIntegerField(verbose_name="Месяц", blank=True)
    year = models.PositiveIntegerField(verbose_name="Год", blank=True)

    class Meta:
        verbose_name = "Начисление"
        verbose_name_plural = "Начисления"
        db_table = "accrual"
        unique_together = ("card_number", "month", "year")

    def save(self, *args, **kwargs):
        # Устанавливаем текущий месяц и год, если они не заданы
        if not self.month:
            self.month = datetime.now().month
        if not self.year:
            self.year = datetime.now().year
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.card_number} - {self.month}/{self.year} - {self.amount}"
