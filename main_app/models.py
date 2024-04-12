from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

MEALS = (
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner')
)



class Toy(models.Model):
    name = models.CharField(max_length=256)
    color = models.CharField(max_length=16)

    def get_absolute_url(self):
        return reverse('toys_detail', kwargs={'pk': self.id}) #class-based views
    
    def __str__(self):
        return self.name



class Cat(models.Model):
    name = models.CharField(max_length=128)
    breed = models.CharField(max_length=128)
    description = models.TextField(max_length=256)
    age = models.IntegerField()
    toys = models.ManyToManyField(Toy) # label is arbitrary
    user = models.ForeignKey(User, on_delete=models.CASCADE) # adds user_id FK column
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={ 'cat_id': self.id })
    
    def fed_for_today(self):
        # return self.feeding_set.filter(date=date.today().count()) >= len(MEALS)
        len( self.feeding_set.filter(date=date.today()) )

    def __str__(self):
        return f"{self.name}, {self.age}" # returns a string
    


class Feeding(models.Model):
    date = models.DateField('feeding date')
    meal = models.CharField(
        max_length=1,
        choices=MEALS,
        default=MEALS[0][0]
    )
    
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE) # create a cat_id FK

    def __str__(self):
        return f"{self.get_meal_display()} on {self.date} for {self.cat}"
    
    class Meta:
        ordering = ['-date']



class Photo(models.Model):
    url = models.CharField(max_length=200)
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for cat_id: {self.cat_id} @{self.url}"