# Generated migration for enhanced review system

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('applications', '0001_initial'),
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='application',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='review', to='applications.Application'),
        ),
        migrations.AddField(
            model_name='review',
            name='communication',
            field=models.PositiveSmallIntegerField(default=5),
        ),
        migrations.AddField(
            model_name='review',
            name='professionalism',
            field=models.PositiveSmallIntegerField(default=5),
        ),
        migrations.AddField(
            model_name='review',
            name='punctuality',
            field=models.PositiveSmallIntegerField(default=5),
        ),
        migrations.AddField(
            model_name='review',
            name='quality_rating',
            field=models.PositiveSmallIntegerField(default=5),
        ),
        migrations.AddField(
            model_name='review',
            name='title',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='review',
            name='is_featured',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='review',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='review',
            name='helpful_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='review',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddIndex(
            model_name='review',
            index=models.Index(fields=['reviewee', '-created_at'], name='reviews_revi_reviewe_idx'),
        ),
        migrations.AddIndex(
            model_name='review',
            index=models.Index(fields=['rating'], name='reviews_revi_rating_idx'),
        ),
        migrations.CreateModel(
            name='ReviewReply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('review', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='reply', to='reviews.review')),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
    ]
