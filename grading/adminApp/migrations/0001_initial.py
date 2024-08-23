# Generated by Django 4.2.13 on 2024-08-13 18:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_date', models.DateField()),
                ('payment_method', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='SubscriptionInfos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=255)),
                ('max_employee_numbers', models.IntegerField()),
                ('max_request_rate', models.IntegerField()),
                ('price', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Subscriptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('subscriptionInfo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='adminApp.subscriptioninfos')),
            ],
        ),
    ]
