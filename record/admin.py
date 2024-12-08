from django.contrib import admin
from .models import InventoryCard, Completeness, Department, Accrual, Equipment, EquipmentCategory, Employee, Boss

admin.site.register(InventoryCard)
admin.site.register(Completeness)
admin.site.register(Department)
admin.site.register(Accrual)
admin.site.register(Equipment)
admin.site.register(EquipmentCategory)
admin.site.register(Employee)
admin.site.register(Boss)