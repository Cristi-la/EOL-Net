# Sample Django Data Population Script for EOL-Net

# This script assumes the Django settings module is already configured via DJANGO_SETTINGS_MODULE.
# You can run this using: 
#    python manage.py shell < test/sample_data.py

import os
import django
from datetime import date, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from app.apps.eol.models import Vendor, Product, Software
from django.db.models import Count

# Clear existing data (optional, for idempotent runs uncomment below)
Vendor.objects.all().delete()
Product.objects.all().delete()
Software.objects.all().delete()

# Create Vendors
vendors = [
    {'name': 'Cisco'},
    {'name': 'Juniper'},
    {'name': 'HPE/Aruba'},
    {'name': 'Dell'},
    {'name': 'Fortinet'},
    {'name': 'MikroTik'},
    {'name': 'TP-Link'},
]

vendor_instances = {}
for v in vendors:
    obj, created = Vendor.objects.get_or_create(name=v['name'])
    vendor_instances[v['name']] = obj

# Helper to generate dates
today = date.today()
delta = timedelta(days=365)

# Create Products for each vendor
products_data = [
    # Cisco Products
    {
        'vendor': 'Cisco',
        'name': 'Catalyst 9300',
        'end_of_life_announced_date': today - 2 * delta,
        'end_of_sale_date': today - delta,
        'end_of_engineering_date': today + delta,
        'end_of_life_date': today + 2 * delta,
    },
    {
        'vendor': 'Cisco',
        'name': 'ISR 4000 Series',
        'end_of_life_announced_date': today - 3 * delta,
        'end_of_sale_date': today - 2 * delta,
        'end_of_engineering_date': today - delta,
        'end_of_life_date': today,
    },
    # Juniper Products
    {
        'vendor': 'Juniper',
        'name': 'MX480',
        'end_of_life_announced_date': today - 3 * delta,
        'end_of_sale_date': today - 2 * delta,
        'end_of_engineering_date': today - delta,
        'end_of_life_date': today + delta,
    },
    {
        'vendor': 'Juniper',
        'name': 'EX4300',
        'end_of_life_announced_date': today - 4 * delta,
        'end_of_sale_date': today - 3 * delta,
        'end_of_engineering_date': today - 2 * delta,
        'end_of_life_date': today - delta,
    },
    # HPE/Aruba Products
    {
        'vendor': 'HPE/Aruba',
        'name': 'Aruba 2930F',
        'end_of_life_announced_date': today - 2 * delta,
        'end_of_sale_date': today - delta,
        'end_of_engineering_date': today + delta,
        'end_of_life_date': today + 3 * delta,
    },
    # Dell Products
    {
        'vendor': 'Dell',
        'name': 'Dell EMC PowerSwitch S5248',
        'end_of_life_announced_date': today - delta,
        'end_of_sale_date': today,
        'end_of_engineering_date': today + delta,
        'end_of_life_date': today + 2 * delta,
    },
    # Fortinet Products
    {
        'vendor': 'Fortinet',
        'name': 'FortiGate 60E',
        'end_of_life_announced_date': today - 3 * delta,
        'end_of_sale_date': today - 2 * delta,
        'end_of_engineering_date': today - delta,
        'end_of_life_date': today + delta,
    },
    # MikroTik Products
    {
        'vendor': 'MikroTik',
        'name': 'CCR1009-7G-1C-1S+',
        'end_of_life_announced_date': today - 4 * delta,
        'end_of_sale_date': today - 3 * delta,
        'end_of_engineering_date': today - 2 * delta,
        'end_of_life_date': today - delta,
    },
    # TP-Link Products
    {
        'vendor': 'TP-Link',
        'name': 'TL-SG108PE',
        'end_of_life_announced_date': today - delta,
        'end_of_sale_date': today,
        'end_of_engineering_date': today + delta,
        'end_of_life_date': today + 2 * delta,
    },
]

product_instances = {}
for pdata in products_data:
    vendor = vendor_instances[pdata['vendor']]
    obj, created = Product.objects.get_or_create(
        vendor=vendor,
        name=pdata['name'],
        defaults={
            'end_of_life_announced_date': pdata['end_of_life_announced_date'],
            'end_of_sale_date': pdata['end_of_sale_date'],
            'end_of_engineering_date': pdata['end_of_engineering_date'],
            'end_of_life_date': pdata['end_of_life_date'],
        }
    )
    product_instances[f"{pdata['vendor']}|{pdata['name']}"] = obj

# Create Software for each vendor
software_data = [
    # Cisco Software
    {
        'vendor': 'Cisco',
        'name': 'IOS XE 17.3.1',
        'end_of_life_announced_date': today - delta,
        'end_of_sale_date': today,
        'end_of_engineering_date': today + delta,
        'end_of_life_date': today + 2 * delta,
    },
    {
        'vendor': 'Cisco',
        'name': 'NX-OS 9.3.3',
        'end_of_life_announced_date': today - 2 * delta,
        'end_of_sale_date': today - delta,
        'end_of_engineering_date': today + delta,
        'end_of_life_date': today + delta,
    },
    # Juniper Software
    {
        'vendor': 'Juniper',
        'name': 'Junos OS 20.2R3',
        'end_of_life_announced_date': today - delta,
        'end_of_sale_date': today,
        'end_of_engineering_date': today + delta,
        'end_of_life_date': today + 2 * delta,
    },
    {
        'vendor': 'Juniper',
        'name': 'Junos OS 19.4R3',
        'end_of_life_announced_date': today - 3 * delta,
        'end_of_sale_date': today - 2 * delta,
        'end_of_engineering_date': today - delta,
        'end_of_life_date': today,
    },
    # HPE/Aruba Software
    {
        'vendor': 'HPE/Aruba',
        'name': 'ArubaOS 8.7',
        'end_of_life_announced_date': today - 2 * delta,
        'end_of_sale_date': today - delta,
        'end_of_engineering_date': today + delta,
        'end_of_life_date': today + 3 * delta,
    },
    # Dell Software
    {
        'vendor': 'Dell',
        'name': 'Dell EMC OS 10.5',
        'end_of_life_announced_date': today - delta,
        'end_of_sale_date': today,
        'end_of_engineering_date': today + delta,
        'end_of_life_date': today + 2 * delta,
    },
    # Fortinet Software
    {
        'vendor': 'Fortinet',
        'name': 'FortiOS 7.2',
        'end_of_life_announced_date': today - 3 * delta,
        'end_of_sale_date': today - 2 * delta,
        'end_of_engineering_date': today - delta,
        'end_of_life_date': today + delta,
    },
    # MikroTik Software
    {
        'vendor': 'MikroTik',
        'name': 'RouterOS v7.1',
        'end_of_life_announced_date': today - 4 * delta,
        'end_of_sale_date': today - 3 * delta,
        'end_of_engineering_date': today - 2 * delta,
        'end_of_life_date': today - delta,
    },
    # TP-Link Software
    {
        'vendor': 'TP-Link',
        'name': 'Omada SDN Controller 5.2.4',
        'end_of_life_announced_date': today - delta,
        'end_of_sale_date': today,
        'end_of_engineering_date': today + delta,
        'end_of_life_date': today + 2 * delta,
    },
]

software_instances = {}
for sdata in software_data:
    vendor = vendor_instances[sdata['vendor']]
    obj, created = Software.objects.get_or_create(
        vendor=vendor,
        name=sdata['name'],
        defaults={
            'end_of_life_announced_date': sdata['end_of_life_announced_date'],
            'end_of_sale_date': sdata['end_of_sale_date'],
            'end_of_engineering_date': sdata['end_of_engineering_date'],
            'end_of_life_date': sdata['end_of_life_date'],
        }
    )
    software_instances[f"{sdata['vendor']}|{sdata['name']}"] = obj


# Print summary
print("=== Vendors ===")
for v in Vendor.objects.annotate(prod_count=Count("products"), sw_count=Count("software_packages")):
    print(f"{v.name}: Products={v.prod_count}, Software={v.sw_count}")

print("\n=== Products ===")
for p in Product.objects.all():
    print(f"{p.vendor.name} - {p.name} | EOL: {p.end_of_life_date}")

print("\n=== Software ===")
for s in Software.objects.all():
    print(f"{s.vendor.name} - {s.name} | EOL: {s.end_of_life_date}")

