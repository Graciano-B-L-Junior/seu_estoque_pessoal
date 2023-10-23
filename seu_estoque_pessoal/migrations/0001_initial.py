# Generated by Django 4.2.6 on 2023-10-21 22:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Fornecedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('nome', models.CharField(max_length=255)),
                ('senha', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('quantidade', models.IntegerField()),
                ('preco_custo', models.FloatField()),
                ('preco_venda', models.FloatField()),
                ('Categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seu_estoque_pessoal.categoria')),
                ('fornecedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seu_estoque_pessoal.fornecedor')),
            ],
        ),
    ]