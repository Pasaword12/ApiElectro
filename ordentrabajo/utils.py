import os
import sys
sys.path.append(os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DrfApi.settings")
from docxtpl import DocxTemplate
from django.templatetags.static import static
from django.contrib.staticfiles.storage import staticfiles_storage
from django.conf import settings
import uuid
from django.core.files import File
import os



def docCreate(templatePath, diccionario, firma_tecnico, firma_cliente):
    doc = DocxTemplate('static/' + templatePath)

    doc.render(diccionario)
    doc.replace_media('static/firma_tecnicoxd.png', firma_tecnico)
    doc.replace_media('static/firma_clientexd.png', firma_cliente)
    fileName = f'OrdenTrabajo{uuid.uuid4()}'
    try:
        doc.save(f'static/{fileName}.docx') 
        file = open(f'static/{fileName}.docx', errors='ignore')
        file = File(file)
        file.name = file.name[7:]
        return file
    except Exception as ex:
        print(ex)
        print('Hubo un error Creando el documento word')
        return None

