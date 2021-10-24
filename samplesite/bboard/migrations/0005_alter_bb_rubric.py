# Generated by Django 3.2.7 on 2021-10-17 12:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0004_auto_20211017_1143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bb',
            name='rubric',
            field=models.ForeignKey(default='Без рубрики', help_text='Выберите рубрику из выпадающего списка', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='bboards', to='bboard.rubric', verbose_name='Рубрика'),
        ),
    ]