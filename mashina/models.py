from django.db import models

class Mashina(models.Model):
    title = models.CharField(max_length=200)
    descriptions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'mashina'

# Create your models here.
