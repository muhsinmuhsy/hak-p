# Generated by Django 4.1 on 2024-05-21 06:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0003_alter_color_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='ColorImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='color')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='color',
            name='image',
        ),
        migrations.RemoveField(
            model_name='product',
            name='image',
        ),
        migrations.AddField(
            model_name='color',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='admin_app.product'),
        ),
        migrations.AddField(
            model_name='color',
            name='images',
            field=models.ManyToManyField(related_name='colors', to='admin_app.colorimage'),
        ),
    ]
