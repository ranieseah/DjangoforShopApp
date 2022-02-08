# Generated by Django 4.0.2 on 2022-02-07 08:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Addresses',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('recipient_name', models.CharField(blank=True, max_length=30)),
                ('address', models.TextField()),
                ('is_active', models.BooleanField(default=True)),
                ('account_of', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('prod_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=25)),
                ('price', models.PositiveSmallIntegerField()),
                ('description', models.TextField()),
                ('qty', models.PositiveSmallIntegerField()),
                ('image', models.CharField(max_length=500)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrdersList',
            fields=[
                ('batch_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('order_status', models.CharField(choices=[('PR', 'Order Received! Order Processing...'), ('RY', 'Order Ready and waiting for Pickup!'), ('DE', 'Order out for Delivery'), ('CM', 'Order Complete.')], default='PR', max_length=2)),
                ('account_of', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('order_status', models.CharField(choices=[('PR', 'Order Received! Order Processing...'), ('RY', 'Order Ready and waiting for Pickup!'), ('DE', 'Order out for Delivery'), ('CM', 'Order Complete.')], default='PR', max_length=2)),
                ('addresses_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main_app.addresses')),
                ('batch_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.orderslist')),
                ('prod_id', models.ManyToManyField(to='main_app.Products')),
            ],
        ),
    ]
