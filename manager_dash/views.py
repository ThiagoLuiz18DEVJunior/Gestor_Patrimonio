import plotly.express as px
import pandas as pd
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.db import models
from .models import *
from .forms import *
from django.views.generic import *

class_translation = {
    'category': 'Categoria',
    'department': 'Departamento',
    'supplier': 'Fornecedor',
    'asset': 'Ativo',
    'movement': 'Movimento',
}

class DynamicListView(ListView):
    template_name = 'list.html'

    def get_model(self):
        model_name = self.kwargs.get('model')
        
        if model_name == 'category':
            return Category
        elif model_name == 'department':
            return Department
        elif model_name == 'supplier':
            return Supplier
        elif model_name == 'asset':
            return Asset
        elif model_name == 'movement':
            return Movement
        else:
            return None

    def get_queryset(self):
        model_class = self.get_model()
        if not model_class:
            return None
        return model_class.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtemos o nome do modelo (em inglês)
        model_name = self.kwargs.get('model')
        
        # Traduzimos para português usando o dicionário
        translated_model_name = class_translation.get(model_name, model_name)
        
        # Passando tanto o nome em inglês quanto a tradução para o template
        context['model'] = translated_model_name
        context['model_class'] = model_name  # Para usar nas URLs
        
        return context

class DynamicCreateView(CreateView):
    template_name = 'add.html'

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

    def get(self, request, *args, **kwargs):
        model_class, form_class = self.get_model_and_form()
        if not model_class:
            return render(request, '404.html')
        form = form_class()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        model_class, form_class = self.get_model_and_form()
        if not model_class:
            return render(request, '404.html')
        form = form_class(request.POST)
        if form.is_valid():
            form.save()
            model = kwargs.get('model')  # Obtém o modelo da URL
            return redirect('dynamic_list', model=model)
        return render(request, self.template_name, {'form': form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model_name = self.kwargs.get('model')
        
        # Dicionário de traduções
        class_translation = {
            'category': 'Categoria',
            'department': 'Departamento',
            'supplier': 'Fornecedor',
            'asset': 'Ativo',
            'movement': 'Movimento',
        }
        
        # Traduzindo o nome do modelo
        translated_model_name = class_translation.get(model_name, model_name)
        
        # Passando o nome traduzido para o template
        context['model'] = translated_model_name
        context['model_class'] = model_name  # Passando o nome em inglês do modelo para o template
        return context

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

    def get_form_class(self):
        model, form_class = self.get_model_and_form()
        return form_class  # Passa o formulário correspondente ao modelo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model, form_class = self.get_model_and_form()
        
        if model and form_class:
            model_name = model.__name__.lower()
            context['model_name'] = model_name
            context['form'] = form_class(instance=self.object)
            # Usando o dicionário importado para pegar a tradução
            context['model_translation'] = class_translation.get(model_name, model_name.title())  # Adicionando a tradução
        return context

    def get_success_url(self):
        model, _ = self.get_model_and_form()
        if model:
            model_name = model.__name__.lower()  # Converte o nome do modelo para minúsculo
            return reverse_lazy('dynamic_list', kwargs={'model': model_name})
        return reverse_lazy('dashboard')

class DynamicDeleteView(DeleteView):
    template_name = 'del.html'

    def get_model(self):
        model_name = self.kwargs.get('model')
        
        if model_name == 'category':
            return Category
        elif model_name == 'department':
            return Department
        elif model_name == 'supplier':
            return Supplier
        elif model_name == 'asset':
            return Asset
        elif model_name == 'movement':
            return Movement
        else:
            return None

    def get(self, request, *args, **kwargs):
        model_class = self.get_model()
        if not model_class:
            return render(request, '404.html')
        obj = model_class.objects.get(pk=self.kwargs['pk'])
        context = {
            'object': obj,
            'model': model_class.__name__.lower(),  # Passando o nome do modelo para o template
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        model_class = self.get_model()
        if not model_class:
            return render(request, '404.html')
        obj = model_class.objects.get(pk=self.kwargs['pk'])
        obj.delete()
        return redirect('dynamic_list', model=model_class.__name__.lower())  # Corrigido para passar o modelo

    
def dashboard(request):
    # 1. Gráfico de Quantidade de Bens por Categoria:
    assets_by_category = Asset.objects.values('category__name').annotate(asset_count=models.Count('id'))
    df_category = pd.DataFrame(list(assets_by_category))
    fig_category = px.bar(df_category, x='category__name', y='asset_count', title='Quantidade de Bens por Categoria')
    fig_category.update_traces(
        hovertemplate='<b>%{x}</b><br>Quantidade de Bens: %{y}<extra></extra>'  # Personalizando o texto exibido
    )
    fig_category.update_layout(
        xaxis_title='Categoria',  
        yaxis_title='Quantidade de Bens'
    )
    graph_category_html = fig_category.to_html(full_html=False)

    # 2. Gráfico de Distribuição de Bens por Departamento:
    assets_by_department = Asset.objects.values('department__name').annotate(asset_count=models.Count('id'))
    df_department = pd.DataFrame(list(assets_by_department))
    fig_department = px.pie(df_department, names='department__name', values='asset_count', title='Distribuição de Bens por Departamento')
    fig_department.update_traces(
        hovertemplate='<b>%{label}</b><br>Quantidade de Bens: %{value}<extra></extra>'  # Personalizando o texto exibido
    )
    graph_department_html = fig_department.to_html(full_html=False)

    # 3. Gráfico de Valor Total de Bens por Categoria:
    total_value_by_category = Asset.objects.values('category__name').annotate(total_value=models.Sum('value'))
    df_value_category = pd.DataFrame(list(total_value_by_category))
    fig_value_category = px.bar(df_value_category, x='category__name', y='total_value', title='Valor Total de Bens por Categoria')
    fig_value_category.update_traces(
        hovertemplate='<b>%{x}</b><br>Valor Total: R$ %{y:.2f}<extra></extra>'  # Personalizando o texto exibido
    )
    fig_value_category.update_layout(
        xaxis_title='Categorias',  
        yaxis_title='Valor em Reais'
    )
    graph_value_category_html = fig_value_category.to_html(full_html=False)

    # 4. Gráfico de Movimentações de Bens ao Longo do Tempo:
    movements_by_date = Movement.objects.values('date').annotate(movement_count=models.Count('id')).order_by('date')
    df_movements = pd.DataFrame(list(movements_by_date))
    df_movements.rename(columns={'date': 'movement_date'}, inplace=True)
    if not df_movements.empty:
        fig_movements = px.line(df_movements, x='movement_date', y='movement_count', title='Movimentações de Bens ao Longo do Tempo')
        fig_movements.update_traces(
            hovertemplate='<b>%{x}</b><br>Movimentações: %{y}<extra></extra>'  # Personalizando o texto exibido
        )  
        fig_movements.update_layout(
        xaxis_title='Data da Movimentação',  
        yaxis_title='Quantidade de Movimentações'
        )
        graph_movements_html = fig_movements.to_html(full_html=False)
    else:
        graph_movements_html = "<p>Nenhuma movimentação registrada.</p>"

    # 5. Gráfico de Quantidade de Bens por Fornecedor
    assets_by_supplier = Asset.objects.values('supplier__name').annotate(asset_count=models.Count('id'))
    df_supplier = pd.DataFrame(list(assets_by_supplier))
    fig_supplier = px.bar(df_supplier, x='supplier__name', y='asset_count', title='Quantidade de Bens por Fornecedor')
    fig_supplier.update_traces(
        hovertemplate='<b>%{x}</b><br>Quantidade de Bens: %{y}<extra></extra>'  # Personalizando o texto exibido
    )
    fig_supplier.update_layout(
        title='Quantidade de Bens por Fornecedor',  # Título do gráfico
        xaxis_title='Fornecedor',  # Título do eixo X
        yaxis_title='Quantidade de Bens',  # Título do eixo Y
        plot_bgcolor='rgba(0,0,0,0)',  # Cor de fundo do gráfico (transparente)
        template="plotly_white",  # Usando um tema de fundo branco
        xaxis_tickangle=-45  # Rotacionando as labels do eixo X para melhor visibilidade (caso tenha muitos fornecedores)
    )
    graph_supplier_html = fig_supplier.to_html(full_html=False)

    # 6. Gráfico de Movimentações por Departamento
    movements_by_departments = Movement.objects.values('from_department__name', 'to_department__name').annotate(movement_count=models.Count('id'))
    df_movements_dept = pd.DataFrame(list(movements_by_departments))

    # Garantir que 'to_department__name' seja tratada como uma variável categórica
    df_movements_dept['to_department__name'] = df_movements_dept['to_department__name'].astype('category')

    # Criando o gráfico de barras com a movimentação por departamento
    fig_movements_dept = px.bar(df_movements_dept, 
                                x='from_department__name', 
                                y='movement_count', 
                                color='to_department__name', 
                                title='Movimentações por Departamento')

    # Personalizando o conteúdo do tooltip com hovertemplate
    fig_movements_dept.update_traces(
        hovertemplate='<b>De: %{x}</b><br>Para: %{customdata}<br>Movimentações: %{y}<extra></extra>',  # Acessando o valor correto
        customdata=df_movements_dept['to_department__name']  # Passando os dados corretos como customdata
    )

    # Personalizando a legenda (barra de cor) para exibir os nomes corretamente
    fig_movements_dept.update_layout(
        coloraxis_colorbar=dict(
            title='Departamento de Destino',  # Título da barra de cor (legenda)
        ),
        legend_title="Departamento de Destino"  # Título da legenda
    )

    # Asegurando que o nome dos departamentos aparece corretamente na legenda
    fig_movements_dept.update_traces(
        marker=dict(
            color=df_movements_dept['to_department__name'].cat.codes,  # Usando os códigos das categorias
            colorscale='Viridis',  # Usando uma escala de cores (pode ajustar conforme necessário)
        )
    )

    # Personalizando o layout do gráfico
    fig_movements_dept.update_layout(
        title='Movimentações por Departamento',  # Título do gráfico
        xaxis_title='Departamento de Origem',  # Título do eixo X
        yaxis_title='Quantidade de Movimentações',  # Título do eixo Y
        plot_bgcolor='rgba(0,0,0,0)',  # Cor de fundo do gráfico (transparente)
        template="plotly_white",  # Usando um tema de fundo branco
        xaxis_tickangle=-45,  # Rotacionando as labels do eixo X para melhor visibilidade
        barmode='stack',  # Empilhando as barras para mostrar as movimentações entre os departamentos
    )

    # Gerando o gráfico HTML
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
