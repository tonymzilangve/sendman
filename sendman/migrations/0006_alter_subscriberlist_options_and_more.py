# Generated by Django 4.1.3 on 2022-11-27 02:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sendman', '0005_subscriberlist_number'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subscriberlist',
            options={'ordering': ['-created_at'], 'verbose_name': 'Список подписчиков', 'verbose_name_plural': 'Списки подписчиков'},
        ),
        migrations.AlterField(
            model_name='subscriberlist',
            name='name',
            field=models.CharField(max_length=30, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='subscriberlist',
            name='number',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Кол-во'),
        ),
    ]
