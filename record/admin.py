from django.contrib import admin
from .models import InventoryCard, Completeness, Department, Accrual, Equipment, EquipmentCategory, Employee

# admin.site.register(InventoryCard)
# admin.site.register(Completeness)
# admin.site.register(Department)
# admin.site.register(Accrual)
# admin.site.register(Equipment)
# admin.site.register(EquipmentCategory)
# admin.site.register(Employee)

from django.contrib import admin
from .models import InventoryCard, Completeness, Department, Accrual, Equipment, EquipmentCategory, Employee

@admin.register(InventoryCard)
class InventoryCardAdmin(admin.ModelAdmin):
    list_display = (
        'card_number', 
        'equipment_code', 
        'completeness_sign', 
        'category_code', 
        'initial_cost', 
        'total_depreciation_amount', 
        'release_date', 
        'commissioning_date', 
        'department_code', 
        'employee_code'
    )


@admin.register(Completeness)
class CompletenessAdmin(admin.ModelAdmin):
    list_display = (
        'card_number', 
        'position_number', 
        'name', 
        'quantity', 
        'note'
    )


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = (
        'department_code', 
        'name', 
        'manager_code'
    )


@admin.register(Accrual)
class AccrualAdmin(admin.ModelAdmin):
    list_display = (
        'card_number', 
        'amount', 
        'month', 
        'year'
    )


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = (
        'equipment_code', 
        'name'
    )


@admin.register(EquipmentCategory)
class EquipmentCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'category_code', 
        'name', 
        'depreciation_rate'
    )


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'employee_code', 
        'full_name', 
        'department_code'
    )
