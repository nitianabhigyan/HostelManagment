# Generated by Django 2.0.5 on 2018-10-13 17:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('password_reset', '0003_reset_pass_db_token1'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reset_pass_db',
            old_name='token1',
            new_name='token0',
        ),
    ]