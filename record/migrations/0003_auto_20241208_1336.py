# Generated by Django 2.2.28 on 2024-12-08 13:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('record', '0002_auto_20241208_1314'),
    ]

    operations = [
        migrations.CreateModel(
            name='Boss',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=50, verbose_name='ФИО')),
            ],
            options={
                'verbose_name': 'Руководитель подразделения',
                'verbose_name_plural': 'Руководители подразделений',
                'db_table': 'manager',
            },
        ),
        migrations.AlterField(
            model_name='department',
            name='manager_code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='managed_departments', to='record.Boss', verbose_name='Код работника руководителя'),
        ),
    ]
