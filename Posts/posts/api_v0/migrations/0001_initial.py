# Generated by Django 3.0.4 on 2020-06-13 10:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('post_id', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.TextField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('like_count', models.IntegerField()),
                ('dislike_count', models.IntegerField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.CharField(editable=False, max_length=200, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('full_name', models.CharField(max_length=200)),
                ('password_hash', models.CharField(max_length=1000)),
                ('email', models.EmailField(blank=True, db_index=True, max_length=70, null=True, unique=True)),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('user_image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_verified', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('refresh_token', models.TextField(blank=True, null=True)),
                ('access_token', models.TextField(blank=True, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('is_expired', models.BooleanField(default=False)),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api_v0.User')),
            ],
        ),
        migrations.CreateModel(
            name='PostTag',
            fields=[
                ('post_tag_id', models.IntegerField(primary_key=True, serialize=False)),
                ('tag', models.TextField(blank=True, null=True)),
                ('weight', models.IntegerField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='post_tags', to='api_v0.Post')),
            ],
        ),
        migrations.CreateModel(
            name='PostLike',
            fields=[
                ('post_like_id', models.CharField(editable=False, max_length=200, primary_key=True, serialize=False)),
                ('is_like', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('post_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='post_data', to='api_v0.Post')),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api_v0.User')),
            ],
        ),
        migrations.CreateModel(
            name='PostImage',
            fields=[
                ('post_image_id', models.IntegerField(primary_key=True, serialize=False)),
                ('image_url', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('post_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='post_images', to='api_v0.Post')),
            ],
        ),
        migrations.AddIndex(
            model_name='postlike',
            index=models.Index(fields=['user_id', 'post_id'], name='api_v0_post_user_id_bead9d_idx'),
        ),
    ]
