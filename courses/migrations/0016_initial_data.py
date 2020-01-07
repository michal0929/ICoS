from __future__ import unicode_literals
from django.db import migrations
from django.utils.text import slugify


def initial_course(apps, schema_editor):
    course = apps.get_model(app_label='courses', model_name='Chapter')

    course( course_name = 'test',
          ).save()



class Migration(migrations.Migration):
    dependencies = [
        ('courses', '0015_auto_20160502_0014'),
    ]

    operations = [
        migrations.RunPython(initial_course)
    ]
