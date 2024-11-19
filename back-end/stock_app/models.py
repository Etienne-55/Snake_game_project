from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    highest_score = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.score}"

    class Meta:
        ordering = ['-score']  # Order by score in descending order

class Coffee(models.Model):
    name = models.CharField(max_length=100)
    origin = models.CharField(max_length=100)
    roast_type = models.CharField(max_length=100)

    def __str__(self):
        return self.name