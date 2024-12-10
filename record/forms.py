from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, label="Логин", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=128, label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-control'}))


from django import forms
from .models import InventoryCard

class InventoryCardForm(forms.ModelForm):
    class Meta:
        model = InventoryCard
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
        widgets = {
            'release_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'commissioning_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
