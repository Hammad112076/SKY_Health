# Generated by Django 5.1.7 on 2025-06-17 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_name', '0003_alter_session_end_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='color',
            field=models.CharField(blank=True, choices=[('red', 'Red'), ('yellow', 'Yellow'), ('green', 'Green')], max_length=10, null=True),
        ),
    ]
