# Generated by Django 2.2.28 on 2024-12-10 22:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('record', '0014_auto_20241209_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='completeness',
            name='name',
            field=models.CharField(max_length=256, verbose_name='Наименование'),
        ),
        migrations.AlterField(
            model_name='completeness',
            name='note',
            field=models.TextField(verbose_name='Примечание'),
        ),
        migrations.AlterField(
            model_name='completeness',
            name='position_number',
            field=models.CharField(blank=True, max_length=10, verbose_name='Номер позиции'),
        ),
        migrations.AlterField(
            model_name='department',
            name='manager_code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='managed_departments', to='record.Employee', verbose_name='Код работника руководителя'),
        ),
        migrations.AlterField(
            model_name='department',
            name='name',
            field=models.CharField(max_length=256, verbose_name='Наименование'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='full_name',
            field=models.CharField(max_length=256, verbose_name='ФИО'),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='equipment_code',
            field=models.CharField(blank=True, max_length=10, primary_key=True, serialize=False, verbose_name='Код оборудования'),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='name',
            field=models.CharField(max_length=256, verbose_name='Наименование'),
        ),
        migrations.AlterField(
            model_name='equipmentcategory',
            name='name',
            field=models.CharField(max_length=256, verbose_name='Наименование'),
        ),
        migrations.AlterField(
            model_name='inventorycard',
            name='completeness_sign',
            field=models.CharField(choices=[('Полная комплектация', 'Полная комплектация'), ('Частичная комплектация', 'Частичная комплектация'), ('Неполная комплектация', 'Неполная комплектация')], max_length=50, verbose_name='Признак комплектности'),
        ),
        migrations.DeleteModel(
            name='Boss',
        ),
    ]
