from django.db import models

from django.contrib.auth.models import AbstractUser


class Profile(AbstractUser):
    avatar = models.ImageField()
    subscribers = models.ManyToManyField('self', related_name='favorite_authors', symmetrical=False, blank=True)

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


'''
class Subcriptions(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='subscribers')
    subscriber = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='subscriptions')

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'

    def __str___(self):
        return f'{self.author} - {self.subscriber}'
'''
