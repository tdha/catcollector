from django.db import models
from django.urls import reverse

MEALS = (
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner')
)

class Cat(models.Model):
    name = models.CharField(max_length=128)
    breed = models.CharField(max_length=128)
    description = models.TextField(max_length=256)
    age = models.IntegerField()
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={ 'cat_id': self.id })

    def __str__(self):
        return f"{self.name}, {self.age}" # returns a string
    

class Feeding(models.Model):
    date = models.DateField('feeding date')
    meal = models.CharField(
        max_length=1,
        choices=MEALS,
        default=MEALS[0][0]
    )
    # create a cat_id FK
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_meal_display()} on {self.date} for {self.cat}"
    
    class Meta:
        ordering = ['-date']


class Toy(models.Model):
    name = models.CharField(max_length=256)
    color = models.CharField(max_length=16)

    def get_absolute_url(self):
        return reverse('toys_detail', kwargs={'pk': self.id}) #class-based views
    
    def __str__(self):
        return self.name