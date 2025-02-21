from django import forms
from .models import *

# 1. Category Form (Formulário para Categorias)
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Descrição da categoria'}),
        }

# 2. Department Form (Formulário para Departamentos/Setores)
class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'location', 'manager']
        widgets = {
            'location': forms.TextInput(attrs={'placeholder': 'Localização do departamento'}),
            'manager': forms.TextInput(attrs={'placeholder': 'Responsável pelo departamento'}),
        }

# 3. Supplier Form (Formulário para Fornecedores)
class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact_email', 'contact_phone', 'address']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Endereço do fornecedor'}),
            'contact_email': forms.EmailInput(attrs={'placeholder': 'Email de contato'}),
            'contact_phone': forms.TextInput(attrs={'placeholder': 'Telefone de contato'}),
        }

# 4. Asset Form (Formulário para Bens)
class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name', 'description', 'value', 'purchase_date', 'category', 'department', 'supplier']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Descrição do bem'}),
            'value': forms.NumberInput(attrs={'placeholder': 'Valor do bem'}),
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
        }

# 5. Movement Form (Formulário para Movimentações)
class MovementForm(forms.ModelForm):
    class Meta:
        model = Movement
        fields = ['asset', 'from_department', 'to_department', 'date', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Descrição da movimentação'}),
        }
