# Generated by Django 3.2.8 on 2022-05-06 20:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=6)),
                ('name', models.TextField()),
                ('documentIdentification', models.TextField()),
                ('phone', models.TextField()),
                ('email', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.TextField(default='110000')),
                ('seller', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='seller.seller')),
            ],
        ),
    ]