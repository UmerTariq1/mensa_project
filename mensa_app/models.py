from django.db import models
from django.contrib.auth.models import User

class MenuItem(models.Model):
    name = models.CharField(max_length=50, default="test")
    description = models.CharField(max_length=500)
    picture = models.ImageField(upload_to='')

    def __str__(self):
        return "Name : " + self.name + "  Description : " + self.description

class Rating(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])

    def __str__(self):
        return f"{self.menu_item.description} - {self.rating}"