import plotly.express as px
import pandas as pd
from django.shortcuts import render
from django.urls import reverse_lazy
from django.db import models
from .models import *
from .forms import *
from django.views.generic import *


class DynamicUpdateView(UpdateView):
    template_name = 'update.html'
    def get_model_and_form(self):
        model_name = self.kwargs.get('model')
        
        if model_name == 'category':
            return Category, CategoryForm
        elif model_name == 'department':
            return Department, DepartmentForm
        elif model_name == 'supplier':
            return Supplier, SupplierForm
        elif model_name == 'asset':
            return Asset, AssetForm
        elif model_name == 'movement':
            return Movement, MovementForm
        else:
            return None, None

    def get_queryset(self):
        model, _ = self.get_model_and_form()
        if model:
            return model.objects.all()
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model, form_class = self.get_model_and_form()
        
        if model and form_class:
            # Usando o nome da classe para identificar o objeto
            context['model_name'] = model.__name__.lower()
            context['form'] = form_class(instance=self.object)
        return context

    def get_success_url(self):
        model, _ = self.get_model_and_form()
        if model:
            return reverse_lazy(f'{model.__name__.lower()}_list')
        return reverse_lazy('home')



def dashboard(request):
    # 1. Gráfico de Quantidade de Bens por Categoria (já existente)
    assets_by_category = Asset.objects.values('category__name').annotate(asset_count=models.Count('id'))
    df_category = pd.DataFrame(list(assets_by_category))
    fig_category = px.bar(df_category, x='category__name', y='asset_count', title='Quantidade de Bens por Categoria')
    graph_category_html = fig_category.to_html(full_html=False)

    # 2. Gráfico de Distribuição de Bens por Departamento
    assets_by_department = Asset.objects.values('department__name').annotate(asset_count=models.Count('id'))
    df_department = pd.DataFrame(list(assets_by_department))
    fig_department = px.pie(df_department, names='department__name', values='asset_count', title='Distribuição de Bens por Departamento')
    graph_department_html = fig_department.to_html(full_html=False)

    # 3. Gráfico de Valor Total de Bens por Categoria
    total_value_by_category = Asset.objects.values('category__name').annotate(total_value=models.Sum('value'))
    df_value_category = pd.DataFrame(list(total_value_by_category))
    fig_value_category = px.bar(df_value_category, x='category__name', y='total_value', title='Valor Total de Bens por Categoria')
    graph_value_category_html = fig_value_category.to_html(full_html=False)

    # 4. Gráfico de Movimentações de Bens ao Longo do Tempo
    movements_by_date = Movement.objects.values('date').annotate(movement_count=models.Count('id')).order_by('date')
    df_movements = pd.DataFrame(list(movements_by_date))
    df_movements.rename(columns={'date': 'movement_date'}, inplace=True)

    if not df_movements.empty:
        fig_movements = px.line(df_movements, x='movement_date', y='movement_count', title='Movimentações de Bens ao Longo do Tempo')
        graph_movements_html = fig_movements.to_html(full_html=False)
    else:
        graph_movements_html = "<p>Nenhuma movimentação registrada.</p>"

    # 5. Gráfico de Quantidade de Bens por Fornecedor
    assets_by_supplier = Asset.objects.values('supplier__name').annotate(asset_count=models.Count('id'))
    df_supplier = pd.DataFrame(list(assets_by_supplier))
    fig_supplier = px.bar(df_supplier, x='supplier__name', y='asset_count', title='Quantidade de Bens por Fornecedor')
    graph_supplier_html = fig_supplier.to_html(full_html=False)

    # 6. Gráfico de Movimentações por Departamento
    movements_by_departments = Movement.objects.values('from_department__name', 'to_department__name').annotate(movement_count=models.Count('id'))
    df_movements_dept = pd.DataFrame(list(movements_by_departments))
    fig_movements_dept = px.bar(df_movements_dept, x='from_department__name', y='movement_count', color='to_department__name', title='Movimentações por Departamento')
    graph_movements_dept_html = fig_movements_dept.to_html(full_html=False)

    # Passar todos os gráficos para o template
    return render(request, 'dashboard.html', {
        'graph_category_html': graph_category_html,
        'graph_department_html': graph_department_html,
        'graph_value_category_html': graph_value_category_html,
        'graph_movements_html': graph_movements_html,
        'graph_supplier_html': graph_supplier_html,
        'graph_movements_dept_html': graph_movements_dept_html,
    })
