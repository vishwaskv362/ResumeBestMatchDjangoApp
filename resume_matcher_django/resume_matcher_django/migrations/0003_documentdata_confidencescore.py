# Generated by Django 4.2.8 on 2024-03-17 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume_matcher_django', '0002_alter_documentdata_extracted_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentdata',
            name='confidenceScore',
            field=models.IntegerField(default=0, max_length=10),
        ),
    ]