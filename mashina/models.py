from django.db import models

class Mashina(models.Model):
    image = models.ImageField(upload_to='image/', null=True, blank=True)
    title = models.CharField(max_length=200)
    descriptions = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'mashina'

# Create your models here.
