from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from .views import AccrualCreateView, AccrualDeleteView, AccrualListView, AccrualUpdateView, CompletenessCreateView, CompletenessDeleteView, CompletenessListView, CompletenessUpdateView, CurrentYearCompletenessCountView, CurrentYearCostByDepartmentView, DepartmentCreateView, DepartmentDeleteView, DepartmentListView, DepartmentUpdateView, DepreciationSumView, EmployeeCreateView, EmployeeDeleteView, EmployeeListView, EmployeeUpdateView, EquipmentCategoryCreateView, EquipmentCategoryDeleteView, EquipmentCategoryListView, EquipmentCategoryUpdateView, EquipmentContainingTolView, EquipmentCreateView, EquipmentDeleteView, EquipmentInRangeView, EquipmentListView, EquipmentUpdateView, InventoryCardCreateView, InventoryCardDeleteView,  InventoryCardListView, InventoryCardUpdateView, equipment_by_employee_report, equipment_downtime_view, equipment_writeoff_report, insert_employees_procedure, inventory_by_category, inventory_card_report, login_view, logout_view, mismatched_years_view
urlpatterns = [
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('inventory-cards/', InventoryCardListView.as_view(), name='inventory_card_list'),
    path('inventory-cards/add/', InventoryCardCreateView.as_view(), name='inventory_card_add'),
    path('inventory-cards/<pk>/edit/', InventoryCardUpdateView.as_view(), name='inventory_card_edit'),
    path('inventory-cards/<pk>/delete/', InventoryCardDeleteView.as_view(), name='inventory_card_delete'),
    path('departments/', DepartmentListView.as_view(), name='department_list'),
    path('departments/add/', DepartmentCreateView.as_view(), name='department_add'),
    path('departments/<pk>/edit/', DepartmentUpdateView.as_view(), name='department_edit'),
    path('departments/<pk>/delete/', DepartmentDeleteView.as_view(), name='department_delete'),
    path('completeness/', CompletenessListView.as_view(), name='completeness_list'),
    path('completeness/add/', CompletenessCreateView.as_view(), name='completeness_add'),
    path('completeness/<pk>/edit/', CompletenessUpdateView.as_view(), name='completeness_edit'),
    path('completeness/<pk>/delete/', CompletenessDeleteView.as_view(), name='completeness_delete'),
    path('accruals/', AccrualListView.as_view(), name='accrual_list'),
    path('accruals/add/', AccrualCreateView.as_view(), name='accrual_add'),
    path('accruals/<pk>/edit/', AccrualUpdateView.as_view(), name='accrual_edit'),
    path('accruals/<pk>/delete/', AccrualDeleteView.as_view(), name='accrual_delete'),
    path('equipment/add/', EquipmentCreateView.as_view(), name='equipment_add'),
    path('equipment/<pk>/edit/', EquipmentUpdateView.as_view(), name='equipment_edit'),
    path('equipment/<pk>/delete/', EquipmentDeleteView.as_view(), name='equipment_confirm_delete'),
    path('equipment/', EquipmentListView.as_view(), name='equipment_list'),
    path('equipment-categories/', EquipmentCategoryListView.as_view(), name='equipment_category_list'),
    path('equipment-categories/<pk>/edit/', EquipmentCategoryUpdateView.as_view(), name='equipment_category_edit'),
    path('equipment-categories/<pk>/delete/', EquipmentCategoryDeleteView.as_view(), name='equipment_category_confirm_delete'),
    path('employees/', EmployeeListView.as_view(), name='employee_list'),
    path('employees/<pk>/edit/', EmployeeUpdateView.as_view(), name='employee_edit'),
    path('employees/<pk>/delete/', EmployeeDeleteView.as_view(), name='employee_confirm_delete'),
    path('equipment-categories/add/', EquipmentCategoryCreateView.as_view(), name='equipment_category_add'),
    path('employees/add/', EmployeeCreateView.as_view(), name='employee_add'),



    path('current-year-cost/', CurrentYearCostByDepartmentView.as_view(), name='current_year_cost_by_department'),
    path('current-year-completeness/', CurrentYearCompletenessCountView.as_view(), name='current_year_completeness_count'),
    #  path('inventory-card-report/', inventory_card_report, name='inventory_card_report'),
    path('equipment/containing-tol/', EquipmentContainingTolView.as_view(), name='equipment_containing_tol'),
    path('equipment/in-range/', EquipmentInRangeView.as_view(), name='equipment_in_range'),
    path('depreciation-sum/', DepreciationSumView.as_view(), name='depreciation_sum'),

    path('report/inventory-card/', inventory_card_report, name='inventory_card_report'),
    path('report/equipment-writeoff-report/', equipment_writeoff_report, name='equipment_writeoff_report'),
    path('report/equipment-by-employee/', equipment_by_employee_report, name='equipment_by_employee_report'),


    path('procedure/mismatched-years/', mismatched_years_view, name='mismatched_years'),
    path('procedure/inventory-by-category/', inventory_by_category, name='inventory_by_category'),
    path('procedure/insert-employees/', insert_employees_procedure, name='insert_employees'),
    path('procedure/downtime/', equipment_downtime_view, name='equipment_downtime'),
]



if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)

urlpatterns += staticfiles_urlpatterns()