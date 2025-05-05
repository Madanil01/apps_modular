from django.db import connection
from django.apps import apps
from django.core.management import call_command
import logging
from django.urls import clear_url_caches
from importlib import reload, import_module
from django.urls import reverse
import re
from pathlib import Path
from django.conf import settings
import os

logger = logging.getLogger(__name__)

def uninstall():
    """Eksekusi saat modul diuninstall"""
    try:
        logger.info("🗑️ Starting product module uninstallation...")
        
        #jika memakai konsep create and drop tabel
        try:
            app_config = apps.get_app_config('product')
            model_list = list(app_config.get_models())
        except LookupError:
            logger.warning("App product not found, maybe already uninstalled")
            return True

       
        # for model in reversed(model_list):
        #     # Hapus data
        #     model.objects.all().delete()
        #     logger.info(f"Deleted all data from {model.__name__}")
            
        #     # Hapus tabel
        #     with connection.schema_editor() as schema_editor:
        #         # pass
        #         schema_editor.delete_model(model)
        #         logger.info(f"Dropped table for {model.__name__}")

        # # 3. Hapus migrasi
        # # call_command('migrate', 'product', 'zero', interactive=False)
        
        # # 4. Hapus permissions
        # from django.contrib.auth.models import Permission
        # from django.contrib.contenttypes.models import ContentType
        # # remove_url_patterns()
        # content_types = ContentType.objects.filter(app_label='product')
        # Permission.objects.filter(content_type__in=content_types).delete()
        # content_types.delete()
        
        logger.info("✅ Product module uninstalled completely!")
        return True
    
    except Exception as e:
        logger.error(f"❌ Uninstallation failed: {str(e)}")
        raise
