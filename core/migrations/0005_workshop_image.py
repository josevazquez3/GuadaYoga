# Generated by Django 4.2.7 on 2025-03-26 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_workshop'),
    ]

    operations = [
        migrations.AddField(
            model_name='workshop',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='workshop_images/'),
        ),
    ]
