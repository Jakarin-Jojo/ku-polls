# Generated by Django 3.2.7 on 2021-10-09 12:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_question_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='end_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='end date'),
        ),
    ]