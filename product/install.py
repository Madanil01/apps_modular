from django.db import connection, transaction
from django.apps import apps
from django.core.management import call_command
import logging
from django.contrib.contenttypes.management import create_contenttypes

logger = logging.getLogger(__name__)

def install():
    """Eksekusi saat modul diinstall"""
    try:
        logger.info("📦 Starting product module installation...")
        #jika memakai konsep create and drop tabel
        app_config = apps.get_app_config('product')
        with transaction.atomic():
            pass
            # Buat schema
            # with connection.schema_editor() as schema_editor:
            #     for model in app_config.get_models():
            #         logger.info(f"Creating table for {model.__name__}")
            #         schema_editor.create_model(model)
            
            # # 3. Buat content types
            # create_contenttypes(app_config)
            
            # # 4. Buat permissions default
            # from django.contrib.auth.models import Permission
            # from django.contrib.contenttypes.models import ContentType
            
            # for model in app_config.get_models():
            #     content_type = ContentType.objects.get_for_model(model)
            #     Permission.objects.get_or_create(
            #         codename=f'view_{model._meta.model_name}',
            #         name=f'Can view {model._meta.verbose_name}',
            #         content_type=content_type
            #     )
        
        logger.info("✅ Product module installed successfully!")
        return True
    
    except Exception as e:
        logger.error(f"❌ Installation failed: {str(e)}")
        raise

__version__ = "1.0.0"