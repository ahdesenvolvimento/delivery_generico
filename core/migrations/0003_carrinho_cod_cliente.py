# Generated by Django 3.0.5 on 2020-05-27 20:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20200526_1926'),
    ]

    operations = [
        migrations.AddField(
            model_name='carrinho',
            name='cod_cliente',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
