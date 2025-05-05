from django.db import transaction
from django.contrib.contenttypes.management import create_contenttypes
from core.models import DynamicField
from product.models import Product, CustomFieldValueProduct

def upgrade(request):
    try:
        with transaction.atomic():
           
            # Dynamic import module
            action  = request.POST.get("action")
        
            if action == "add_field":
                modul_name = request.POST.get("modul_name")
                model_name = modul_name.capitalize()
                field_name = request.POST.get("field_name")
                field_type = request.POST.get("field_type")
                default = request.POST.get("default") or None
                max_length = request.POST.get("max_length") or None

                DynamicField.objects.create(
                    model_name=model_name,
                    field_name=field_name,
                    field_type=field_type,
                    default=default,
                    max_length=max_length if max_length else None,
                    nullable=True,
                    blank=True,
                ) 
            else :
        
                field_id = request.POST.get("field_id")
                field = DynamicField.objects.get(id=field_id)
                CustomFieldValueProduct.objects.filter(dynamic_field=field).delete()
                field.delete()

        return True
    except Exception as e:
       return False
