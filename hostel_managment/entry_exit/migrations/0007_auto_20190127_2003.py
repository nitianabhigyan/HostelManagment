# Generated by Django 2.0.5 on 2019-01-27 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entry_exit', '0006_auto_20190127_1959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student_still_out',
            name='is_complete',
            field=models.BooleanField(default=False),
        ),
    ]
