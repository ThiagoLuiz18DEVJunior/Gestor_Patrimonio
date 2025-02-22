from django import forms
from .models import *

# 1. Category Form (Formulário para Categorias)
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 3, 
                'placeholder': 'Descrição da categoria',
                'class': 'form-control',
            }),
            'name': forms.TextInput(attrs={
                'placeholder': 'Nome da categoria', 
                'class': 'form-control'
            }),
        }

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Nome da Categoria"
        self.fields['description'].label = "Descrição"


# 2. Department Form (Formulário para Departamentos/Setores)
class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'location', 'manager']
        widgets = {
            'location': forms.TextInput(attrs={
                'placeholder': 'Localização do departamento',
                'class': 'form-control'
            }),
            'manager': forms.TextInput(attrs={
                'placeholder': 'Responsável pelo departamento',
                'class': 'form-control'
            }),
            'name': forms.TextInput(attrs={
                'placeholder': 'Nome do departamento',
                'class': 'form-control'
            }),
        }

    def __init__(self, *args, **kwargs):
        super(DepartmentForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Nome do Departamento"
        self.fields['location'].label = "Localização"
        self.fields['manager'].label = "Responsável"


# 3. Supplier Form (Formulário para Fornecedores)
class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact_email', 'contact_phone', 'address']
        widgets = {
            'address': forms.Textarea(attrs={
                'rows': 3, 
                'placeholder': 'Endereço do fornecedor',
                'class': 'form-control'
            }),
            'contact_email': forms.EmailInput(attrs={
                'placeholder': 'Email de contato', 
                'class': 'form-control'
            }),
            'contact_phone': forms.TextInput(attrs={
                'placeholder': 'Telefone de contato', 
                'class': 'form-control'
            }),
            'name': forms.TextInput(attrs={
                'placeholder': 'Nome do fornecedor', 
                'class': 'form-control'
            }),
        }

    def __init__(self, *args, **kwargs):
        super(SupplierForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Nome do Fornecedor"
        self.fields['contact_email'].label = "Email de Contato"
        self.fields['contact_phone'].label = "Telefone de Contato"
        self.fields['address'].label = "Endereço"


# 4. Asset Form (Formulário para Bens)
class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name', 'description', 'value', 'purchase_date', 'category', 'department', 'supplier']
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 3, 
                'placeholder': 'Descrição do bem', 
                'class': 'form-control'
            }),
            'value': forms.NumberInput(attrs={
                'placeholder': 'Valor do bem', 
                'class': 'form-control'
            }),
            'purchase_date': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'form-control'
            }),
            'name': forms.TextInput(attrs={
                'placeholder': 'Nome do bem', 
                'class': 'form-control'
            }),
        }

    def __init__(self, *args, **kwargs):
        super(AssetForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Nome do Bem"
        self.fields['description'].label = "Descrição"
        self.fields['value'].label = "Valor"
        self.fields['purchase_date'].label = "Data de Compra"
        self.fields['category'].label = "Categoria"
        self.fields['department'].label = "Departamento"
        self.fields['supplier'].label = "Fornecedor"


# 5. Movement Form (Formulário para Movimentações)
class MovementForm(forms.ModelForm):
    class Meta:
        model = Movement
        fields = ['asset', 'from_department', 'to_department', 'date', 'description']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'rows': 3, 
                'placeholder': 'Descrição da movimentação', 
                'class': 'form-control'
            }),
            'asset': forms.Select(attrs={
                'class': 'form-control'
            }),
            'from_department': forms.Select(attrs={
                'class': 'form-control'
            }),
            'to_department': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

    def __init__(self, *args, **kwargs):
        super(MovementForm, self).__init__(*args, **kwargs)
        self.fields['asset'].label = "Bem"
        self.fields['from_department'].label = "Departamento de Origem"
        self.fields['to_department'].label = "Departamento de Destino"
        self.fields['date'].label = "Data da Movimentação"
        self.fields['description'].label = "Descrição"
