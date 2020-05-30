# Generated by Django 3.0.5 on 2020-05-27 22:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_endereco_cod_cliente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='endereco',
            name='cod_cliente',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
