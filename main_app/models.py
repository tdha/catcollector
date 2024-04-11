from django.db import models
from django.urls import reverse

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