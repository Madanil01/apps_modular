from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.apps import apps
from .models import Product, DynamicField, CustomFieldValueProduct
from .forms import ProductForm  # kita buat form statis
from core.models import Module
from role.models import UserDetails
from django.contrib.auth.models import User
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from core.views import user_data_func
from django.db import connection, transaction
def _get_dynamic_fields():
    return DynamicField.objects.filter(model_name='Product')

def product_list(request): 
    try:
        with transaction.atomic():
            data = user_data_func(request)
            module = Module.objects.get(name='product')
            products = Product.objects.all()

            dyn_fields = _get_dynamic_fields()
            dataDynamicFields = []
            for dyn_field in dyn_fields:
                dataDynamicFields.append({
                    'field_name': dyn_field.field_name,
                    'field_type': dyn_field.field_type,
                    'default': dyn_field.default,
                    'max_length': dyn_field.max_length,
                })
        
            product_data = []
            for product in products:
                # Ambil nilai custom field untuk tiap produk
                cvs = CustomFieldValueProduct.objects.filter(product=product)
                
                # Kumpulkan custom fields, jika tidak ada, set nilai default None
                custom_fields = {}
                for dyn_field in dyn_fields:
                    # Cari nilai custom field jika ada, kalau tidak ada set None
                    field_value = next(
                        (cv.value for cv in cvs if cv.dynamic_field == dyn_field), 
                        None
                    )
                    custom_fields[dyn_field.field_name] = field_value
                
                # Serialisasi data produk
                product_info = {
                    'id': product.id,
                    'name': product.name,
                    'barcode': product.barcode,
                    'price': product.price,
                    'stock': product.stock,
                    'custom_fields': custom_fields
                }
                product_data.append(product_info)
            if module.is_active:
                products = Product.objects.all()
                
                
                return render(request, 'product/list.html', {'products':product_data,'dyn_fields':dataDynamicFields, 'user':data})
            else:
                
                return render(request, 'core/notfound.html', {'redirect_url': '/module'})
    except Exception as e:
        messages.error(request, str(e))
        return redirect('product-list')

def product_create(request):
    try:
        with transaction.atomic():
            data = user_data_func(request)
            if 'R' not in data['access']:
                messages.error(request, "You don't have permission to access this action")
                return False
            dyn_fields = _get_dynamic_fields()
            if request.method == 'POST':
                form = ProductForm(request.POST)
                if form.is_valid():
                    product = form.save()
                    # simpan dynamic values
                    for df in dyn_fields:
                        val = request.POST.get(df.field_name)
                        if val is not None:
                            CustomFieldValueProduct.objects.create(
                                product=product,
                                dynamic_field=df,
                                value=val
                            )
                    messages.success(request, "Product created!")
                    return redirect('product-list')
            else:
                form = ProductForm()
            return render(request, 'product/form.html', {
                'form': form, 
                'dyn_fields': dyn_fields,
                'action': 'Tambah'
            })
    except Exception as e:
        messages.error(request, str(e))
        return redirect('product-list')

def product_update(request, pk):
    try:
        with transaction.atomic():
            data = user_data_func(request)
            if 'U' not in data['access']:
                messages.error(request, "You don't have permission to access this action")
                return False
            product = get_object_or_404(Product, pk=pk)
            dyn_fields = _get_dynamic_fields()
            # ambil existing values
            existing = {
                cf.dynamic_field.field_name: cf.value
                for cf in CustomFieldValueProduct.objects.filter(product=product)
            }
            if request.method == 'POST':
                form = ProductForm(request.POST, instance=product)
                if form.is_valid():
                    form.save()
                    # update dynamic values
                    for df in dyn_fields:
                        val = request.POST.get(df.field_name)
                        cf, created = CustomFieldValueProduct.objects.get_or_create(
                            product=product, dynamic_field=df,
                            defaults={'value': val or ''}
                        )
                        if not created:
                            cf.value = val or ''
                            cf.save()
                    messages.success(request, "Product updated!")
                    return redirect('product-list')
            else:
                form = ProductForm(instance=product)
            return render(request, 'product/form.html', {
                'form': form,
                'dyn_fields': dyn_fields,
                'existing': existing,
                'action': 'Edit'
            })
    except Exception as e:
        messages.error(request, str(e))
        return redirect('product-list')

def product_delete(request, pk):
    try:
        with transaction.atomic():
            data = user_data_func(request)
            if 'X' not in data['access']:
                messages.error(request, "You don't have permission to access this action")
                return False
            product = get_object_or_404(Product, pk=pk)
            if request.method == 'POST':
                product.delete()
                messages.success(request, "Product deleted!")
                return redirect('product-list')
            return render(request, 'product/confirm_delete.html', {'object': product})
    except Exception as e:
        messages.error(request, str(e))
        return redirect('product-list')
