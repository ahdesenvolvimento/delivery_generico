# Generated by Django 3.0.5 on 2020-05-17 16:33

import core.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import stdimage.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bairro',
            fields=[
                ('cod_bairro', models.AutoField(primary_key=True, serialize=False, verbose_name='Código do bairro')),
                ('nome', models.CharField(max_length=30, verbose_name='Nome do bairro')),
                ('taxa', models.FloatField(verbose_name='Taxa de entrega')),
            ],
            options={
                'verbose_name': 'Bairro',
                'verbose_name_plural': 'Bairros',
            },
        ),
        migrations.CreateModel(
            name='Base',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criacao', models.DateField(auto_now_add=True, verbose_name='Criação')),
                ('modificacao', models.DateField(auto_now=True, verbose_name='Modificação')),
            ],
        ),
        migrations.CreateModel(
            name='FormaPagamento',
            fields=[
                ('cod_forma', models.AutoField(primary_key=True, serialize=False, verbose_name='Código')),
                ('forma', models.CharField(max_length=75, verbose_name='Forma de pagamento')),
            ],
            options={
                'verbose_name': 'Forma de pagamento',
                'verbose_name_plural': 'Formas de pagamento',
            },
        ),
        migrations.CreateModel(
            name='Primario',
            fields=[
                ('cod_pri', models.AutoField(primary_key=True, serialize=False, verbose_name='Código da matéria prima')),
                ('nome', models.CharField(max_length=50, verbose_name='Nome base')),
            ],
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('cod_ing', models.AutoField(primary_key=True, serialize=False, verbose_name='Código do produto')),
                ('nome', models.CharField(max_length=50, verbose_name='Nome do produto')),
                ('descricao', models.TextField(max_length=120, verbose_name='Descrição do produto')),
                ('valor', models.FloatField(verbose_name='Preço')),
                ('imagem', stdimage.models.StdImageField(upload_to='produtos', verbose_name='Imagem')),
                ('cod_primario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Primario')),
            ],
            options={
                'verbose_name': 'Produto',
                'verbose_name_plural': 'Produtos',
            },
        ),
        migrations.CreateModel(
            name='Teste2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('k', models.CharField(max_length=142151, verbose_name='teste')),
            ],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('base_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='core.Base')),
                ('cod_compra', models.AutoField(primary_key=True, serialize=False, verbose_name='Código do pedido')),
                ('status', models.CharField(default='Aguardando confirmação', max_length=70, verbose_name='Status do pedido')),
                ('controle', models.BooleanField(default=False, verbose_name='Controle')),
                ('finalizado', models.BooleanField(default=False, verbose_name='Pedido Finalizado?')),
            ],
            bases=('core.base',),
        ),
        migrations.CreateModel(
            name='Teste',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x', models.CharField(max_length=142151, verbose_name='test')),
                ('y', models.ForeignKey(default=0, max_length=512, on_delete=django.db.models.deletion.CASCADE, to='core.Produto')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(max_length=25, unique=True, verbose_name='Username')),
                ('email', models.EmailField(max_length=75, verbose_name='Email')),
                ('telefone', models.CharField(max_length=15, verbose_name='Telefone')),
                ('numero', models.IntegerField(verbose_name='Número')),
                ('bairro', models.CharField(max_length=50, verbose_name='Bairro')),
                ('cep', models.CharField(max_length=50, verbose_name='CEP')),
                ('complemento', models.CharField(max_length=100, verbose_name='Complemento')),
                ('ponto', models.CharField(default=None, max_length=50, verbose_name='Ponto de referência')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Membro da equipe')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', core.models.BaseManager()),
            ],
        ),
        migrations.CreateModel(
            name='ProdutoPedido',
            fields=[
                ('cod', models.AutoField(primary_key=True, serialize=False, verbose_name='Código')),
                ('quantidade', models.IntegerField(verbose_name='Quantidade')),
                ('total', models.FloatField(default=None, null=True, verbose_name='Total')),
                ('cod_prod', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Produto')),
                ('cod_pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Pedido')),
            ],
            options={
                'verbose_name': 'Produto pedido',
                'verbose_name_plural': 'Produtos pedidos',
            },
        ),
        migrations.AddField(
            model_name='pedido',
            name='cod_cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='pedido',
            name='cod_forma',
            field=models.ForeignKey(null=True, on_delete=models.Model, to='core.FormaPagamento'),
        ),
    ]
