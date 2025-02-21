from django.db import models

# Create your models here.

# 1. Categories (Categorias)
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

# 2. Departments (Departamentos/Setores)
class Department(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    manager = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

# 3. Suppliers (Fornecedores)
class Supplier(models.Model):
    name = models.CharField(max_length=255)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField()

    def __str__(self):
        return self.name

# 4. Assets (Bens)
class Asset(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

# 5. Movements (Movimentações)
class Movement(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    from_department = models.ForeignKey(Department, related_name='movements_from', on_delete=models.CASCADE)
    to_department = models.ForeignKey(Department, related_name='movements_to', on_delete=models.CASCADE)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Movement of {self.asset.name} from {self.from_department.name} to {self.to_department.name} on {self.date}"

    class Meta:
        verbose_name = "Movement"
        verbose_name_plural = "Movements"
