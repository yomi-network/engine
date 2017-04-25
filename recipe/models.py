from django.contrib.postgres.fields import JSONField
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(max_length=800)
    images = JSONField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    _my_subclass = models.CharField(max_length=200) 


    class Meta:
        ordering = ["-created_at"]

    @property
    def kind(self):
        return getattr(self, self._my_subclass).__class__.__name__.lower()

    def save(self, *args, **kwargs):
        if type(self) == Post:
            return
        else:
            self._my_subclass = self.__class__.__name__.lower() 
            super(Post, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if type(self) == Post:
            return
        else:
            super(Post, self).save(*args, **kwargs)

# Create your models here.
class Recipe(Post):
    ingredients = JSONField()
    steps = JSONField()
    portions = models.PositiveIntegerField()
    cost = models.DecimalField(decimal_places=2, max_digits=6)

class Menu(Post):
    collaborative = models.BooleanField()
    entries = JSONField()
