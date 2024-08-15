# Generated by Django 4.2.13 on 2024-08-15 07:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Classes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ExamForms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('form_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Students',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('father', models.CharField(max_length=255)),
                ('mother', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='StudentClasses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('examination_id', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('classes', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='userApp.classes')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='userApp.students')),
            ],
        ),
        migrations.CreateModel(
            name='questions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_number', models.IntegerField()),
                ('answer', models.CharField(max_length=10)),
                ('examForm', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='userApp.examforms')),
            ],
        ),
        migrations.CreateModel(
            name='Marks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark', models.IntegerField()),
                ('status', models.CharField(max_length=50)),
                ('studentClass', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='userApp.studentclasses')),
                ('xamForm', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='userApp.examforms')),
            ],
        ),
        migrations.CreateModel(
            name='Exams',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('complete_mark', models.IntegerField()),
                ('pass_mark', models.IntegerField()),
                ('question_number', models.IntegerField()),
                ('classes', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='userApp.classes')),
            ],
        ),
        migrations.AddField(
            model_name='examforms',
            name='exam',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='userApp.exams'),
        ),
    ]
