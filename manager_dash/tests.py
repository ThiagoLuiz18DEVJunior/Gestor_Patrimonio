from django.test import TestCase
from datetime import date
from .models import *

# Create your tests here.

class CategoryModelTest(TestCase):

    def test_create_category(self):
        category = Category.objects.create(name="Hardware", description="Categoria de hardware")
        self.assertEqual(category.name, "Hardware")
        self.assertEqual(category.description, "Categoria de hardware")
        self.assertEqual(str(category), "Hardware")

class DepartmentModelTest(TestCase):

    def test_create_department(self):
        department = Department.objects.create(name="TI", location="Bloco A", manager="João")
        self.assertEqual(department.name, "TI")
        self.assertEqual(department.location, "Bloco A")
        self.assertEqual(department.manager, "João")
        self.assertEqual(str(department), "TI")

class SupplierModelTest(TestCase):

    def test_create_supplier(self):
        supplier = Supplier.objects.create(
            name="Fornecedor A",
            contact_email="fornecedor@example.com",
            contact_phone="1234567890",
            address="Rua X, 123"
        )
        self.assertEqual(supplier.name, "Fornecedor A")
        self.assertEqual(supplier.contact_email, "fornecedor@example.com")
        self.assertEqual(supplier.contact_phone, "1234567890")
        self.assertEqual(supplier.address, "Rua X, 123")
        self.assertEqual(str(supplier), "Fornecedor A")

class AssetModelTest(TestCase):

    def test_create_asset(self):
        category = Category.objects.create(name="Hardware")
        department = Department.objects.create(name="TI", location="Bloco A")
        supplier = Supplier.objects.create(
            name="Fornecedor A",
            contact_email="fornecedor@example.com",
            contact_phone="1234567890",
            address="Rua X, 123"
        )

        asset = Asset.objects.create(
            name="Computador",
            description="Computador de mesa",
            value=1500.00,
            purchase_date=date.today(),
            category=category,
            department=department,
            supplier=supplier
        )

        self.assertEqual(asset.name, "Computador")
        self.assertEqual(asset.value, 1500.00)
        self.assertEqual(asset.purchase_date, date.today())
        self.assertEqual(str(asset), "Computador")
        self.assertEqual(asset.category.name, "Hardware")
        self.assertEqual(asset.department.name, "TI")
        self.assertEqual(asset.supplier.name, "Fornecedor A")

class MovementModelTest(TestCase):

    def test_create_movement(self):
        category = Category.objects.create(name="Hardware")
        department_from = Department.objects.create(name="TI", location="Bloco A")
        department_to = Department.objects.create(name="Financeiro", location="Bloco B")
        supplier = Supplier.objects.create(
            name="Fornecedor A",
            contact_email="fornecedor@example.com",
            contact_phone="1234567890",
            address="Rua X, 123"
        )
        asset = Asset.objects.create(
            name="Computador",
            description="Computador de mesa",
            value=1500.00,
            purchase_date=date.today(),
            category=category,
            department=department_from,
            supplier=supplier
        )

        movement = Movement.objects.create(
            asset=asset,
            from_department=department_from,
            to_department=department_to,
            date=date.today(),
            description="Transferência de TI para Financeiro"
        )

        self.assertEqual(movement.asset.name, "Computador")
        self.assertEqual(movement.from_department.name, "TI")
        self.assertEqual(movement.to_department.name, "Financeiro")
        self.assertEqual(movement.description, "Transferência de TI para Financeiro")
        self.assertEqual(str(movement), f"Movement of Computador from TI to Financeiro on {date.today()}")

class AssetModelTest(TestCase):

    def test_create_asset_with_rfid(self):
        category = Category.objects.create(name="Hardware")
        department = Department.objects.create(name="TI", location="Bloco A")
        supplier = Supplier.objects.create(
            name="Fornecedor A",
            contact_email="fornecedor@example.com",
            contact_phone="1234567890",
            address="Rua X, 123"
        )

        # Criando um bem com a tag RFID
        asset = Asset.objects.create(
            name="Computador",
            description="Computador de mesa",
            value=1500.00,
            purchase_date=date.today(),
            category=category,
            department=department,
            supplier=supplier,
            rfid_tag="1234567890"  # A tag RFID
        )

        self.assertEqual(asset.rfid_tag, "1234567890")
        self.assertEqual(Asset.objects.filter(rfid_tag="1234567890").exists(), True)


