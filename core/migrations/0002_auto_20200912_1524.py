# Generated by Django 3.0.5 on 2020-09-12 18:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carrinho',
            name='cod_prod_adicional',
        ),
        migrations.AddField(
            model_name='carrinho',
            name='cod_prod',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='core.Produto'),
        ),
        migrations.DeleteModel(
            name='AdicionalProduto',
        ),
    ]
