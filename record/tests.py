from django.test import TestCase, Client
from django.urls import reverse
from .models import (
    InventoryCard, Department, Equipment, EquipmentCategory, Employee
)
from datetime import datetime

class ViewsTestCase(TestCase):

    def setUp(self):
        # Создание тестовых данных
        self.equipment_category = EquipmentCategory.objects.create(
            category_code='CAT001',
            name='Категория 1',
            depreciation_rate=10.0
        )
        self.equipment = Equipment.objects.create(
            equipment_code='EQ001',
            name='Оборудование 1'
        )
        self.department = Department.objects.create(
            department_code='DEP001',
            name='Отдел 1',
        )
        self.employee = Employee.objects.create(
            employee_code='EMP001',
            full_name='Иван Иванов',
            department_code=self.department
        )
        self.inventory_card = InventoryCard.objects.create(
            card_number='0001',
            equipment_code=self.equipment,
            completeness_sign='Полная комплектация',
            category_code=self.equipment_category,
            initial_cost=10000.0,
            total_depreciation_amount=1000.0,
            release_date=datetime.now().date(),
            commissioning_date=datetime.now().date(),
            department_code=self.department,
            employee_code=self.employee
        )

    def test_inventory_card_list_view(self):
        # Проверка отображения списка инвентарных карточек
        response = self.client.get(reverse('inventory_card_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'model/inventory_card_list.html')
        self.assertContains(response, 'Инвентарные карточки')

    def test_inventory_card_filter_by_completeness(self):
        # Проверка фильтрации по признаку комплектности
        response = self.client.get(reverse('inventory_card_list'), {'completeness_sign': 'Полная комплектация'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Полная комплектация')

    def test_inventory_card_filter_by_date_range(self):
        # Проверка фильтрации по диапазону дат
        start_date = self.inventory_card.commissioning_date
        end_date = self.inventory_card.commissioning_date
        response = self.client.get(reverse('inventory_card_list'), {
            'start_date': start_date,
            'end_date': end_date
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '0001')  # Номер карточки

    def test_inventory_card_create_view(self):
        # Проверка создания инвентарной карточки
        response = self.client.post(reverse('inventory_card_add'), {
            'card_number': '0002',
            'equipment_code': self.equipment.pk,
            'completeness_sign': 'Полная комплектация',
            'category_code': self.equipment_category.pk,
            'initial_cost': 20000.0,
            'total_depreciation_amount': 2000.0,
            'release_date': datetime.now().date(),
            'commissioning_date': datetime.now().date(),
            'department_code': self.department.pk,
            'employee_code': self.employee.pk
        })
        self.assertEqual(response.status_code, 302)  # Перенаправление
        self.assertTrue(InventoryCard.objects.filter(card_number='0002').exists())

    def test_inventory_card_delete_view(self):
        # Проверка удаления инвентарной карточки
        response = self.client.post(reverse('inventory_card_delete', args=[self.inventory_card.pk]))
        self.assertEqual(response.status_code, 302)  # Перенаправление
        self.assertFalse(InventoryCard.objects.filter(pk=self.inventory_card.pk).exists())

    def test_department_list_view(self):
        # Проверка отображения списка подразделений
        response = self.client.get(reverse('department_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'model/department_list.html')
        self.assertContains(response, 'Отдел 1')

    def test_department_create_view(self):
        # Проверка создания подразделения
        response = self.client.post(reverse('department_add'), {
            'department_code': 'DEP002',
            'name': 'Отдел 2',
            'manager_code': ""
        })
        self.assertEqual(response.status_code, 302)  # Перенаправление
        self.assertTrue(Department.objects.filter(department_code='DEP002').exists())

    def test_department_delete_view(self):
        # Проверка удаления подразделения
        response = self.client.post(reverse('department_delete', args=[self.department.pk]))
        self.assertEqual(response.status_code, 302)  # Перенаправление
        self.assertFalse(Department.objects.filter(pk=self.department.pk).exists())

    def test_inventory_card_report(self):
        # Проверка генерации отчета
        response = self.client.get(reverse('inventory_card_report'), {
            'start_date': self.inventory_card.commissioning_date,
            'end_date': self.inventory_card.commissioning_date,
            'pdf': 'true'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
