from django.db import models

class Cat(models.Model):
    name = models.CharField(max_length=128)
    breed = models.CharField(max_length=128)
    description = models.TextField(max_length=256)
    age = models.IntegerField()

    def __str__(self):
        return f"{self.name}, {self.age}" # returns a string
