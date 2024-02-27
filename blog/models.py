from django.db import models
from django.utils.text import slugify
from django.urls import reverse

NULLABLE = {'blank': True, 'null': True}


class BlogPost(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.CharField(unique=True, max_length=100, verbose_name='Адрес')
    post_content = models.TextField(verbose_name='Содержимое', **NULLABLE)
    preview = models.ImageField(upload_to='blog_previews/', verbose_name='Превью (изображение)', **NULLABLE)
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_published = models.BooleanField(default=True, verbose_name='Признак публикации')
    view_count = models.BigIntegerField(default=0, verbose_name='Количество просмотров')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def generate_slug(self):
        """
        Генерирует уникальный слаг на основе заголовка.
        """
        slug = slugify(self.title)
        unique_slug = slug
        extension = 1

        while BlogPost.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}-{extension}"
            extension += 1

        return unique_slug

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'