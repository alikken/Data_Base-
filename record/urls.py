from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from .views import AccrualListView, CompletenessListView, DepartmentListView, EmployeeListView, EquipmentCategoryListView, EquipmentListView,  InventoryCardListView, login_view, logout_view
urlpatterns = [
    # path('index/', index, name='index'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    # path('models/', model_tables, name='model_tables'),
    path('inventory-cards/', InventoryCardListView.as_view(), name='inventory_card_list'),
    # path('inventory-cards/add/', InventoryCardCreateView.as_view(), name='inventory_card_add'),
    # path('inventory-cards/<pk>/delete/', InventoryCardDeleteView.as_view(), name='inventory_card_delete'),
    path('departments/', DepartmentListView.as_view(), name='department_list'),
    # path('departments/add/', DepartmentCreateView.as_view(), name='department_add'),
    # path('departments/<pk>/delete/', DepartmentDeleteView.as_view(), name='department_delete'),
    path('completeness/', CompletenessListView.as_view(), name='completeness_list'),
    path('accruals/', AccrualListView.as_view(), name='accrual_list'),
    path('equipment/', EquipmentListView.as_view(), name='equipment_list'),
    path('equipment-categories/', EquipmentCategoryListView.as_view(), name='equipment_category_list'),
    path('employees/', EmployeeListView.as_view(), name='employee_list'),



    #  path('inventory-card-report/', inventory_card_report, name='inventory_card_report'),
]



if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)

urlpatterns += staticfiles_urlpatterns()