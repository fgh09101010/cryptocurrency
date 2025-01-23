# Generated by Django 5.1.5 on 2025-01-23 01:12

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Coin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coinname', models.CharField(max_length=100)),
                ('abbreviation', models.CharField(max_length=100)),
                ('logo_url', models.URLField(blank=True, null=True)),
                ('api_id', models.BigIntegerField(null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='NewsArticle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('url', models.URLField(max_length=255, unique=True)),
                ('image_url', models.URLField(max_length=500, null=True)),
                ('content', models.TextField(null=True)),
                ('time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='NewsWebsite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('url', models.URLField(max_length=255, unique=True)),
                ('icon_url', models.URLField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='XPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ids', models.CharField(max_length=255, unique=True)),
                ('html', models.TextField()),
                ('text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='BitcoinPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usd', models.FloatField()),
                ('twd', models.FloatField()),
                ('jpy', models.FloatField()),
                ('eur', models.FloatField()),
                ('market_cap', models.DecimalField(decimal_places=2, max_digits=30, null=True)),
                ('volume_24h', models.DecimalField(decimal_places=2, max_digits=30, null=True)),
                ('change_24h', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('timestamp', models.DateTimeField()),
                ('coin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='price', to='main.coin')),
            ],
        ),
        migrations.CreateModel(
            name='CoinHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('open_price', models.DecimalField(decimal_places=10, max_digits=20)),
                ('high_price', models.DecimalField(decimal_places=10, max_digits=20)),
                ('low_price', models.DecimalField(decimal_places=10, max_digits=20)),
                ('close_price', models.DecimalField(decimal_places=10, max_digits=20)),
                ('volume', models.DecimalField(decimal_places=10, max_digits=65)),
                ('coin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to='main.coin')),
            ],
        ),
        migrations.CreateModel(
            name='DepthData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_update_id', models.BigIntegerField()),
                ('bids', models.JSONField()),
                ('asks', models.JSONField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('coin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='depth_data', to='main.coin')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='main.newsarticle')),
            ],
        ),
        migrations.AddField(
            model_name='newsarticle',
            name='website',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.newswebsite'),
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='main.comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserNotificationPreference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('news_notifications', models.BooleanField(default=True)),
                ('email_notifications', models.BooleanField(default=False)),
                ('site_notifications', models.BooleanField(default=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='notification_preference', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_image', models.ImageField(default='profile_images/default.jpg', null=True, upload_to='profile_images/')),
                ('favorite_coin', models.ManyToManyField(blank=True, to='main.coin')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
