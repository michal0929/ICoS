from __future__ import unicode_literals
from django.db import migrations
from django.utils.text import slugify


def initial_topic(apps, schema_editor):
    topic = apps.get_model(app_label='forum', model_name='Topic')

    topic(author='John',
          subject='I like this forum!',
          slug=slugify('I like this forum!'),
          topic_message='...'
          ).save()



class Migration(migrations.Migration):
    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(initial_topic)
    ]
