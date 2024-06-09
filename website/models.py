from django.db import models

# Create your models here.
class Records(models.Model):
    created_at= models.DateTimeField(auto_now_add=True)
    name= models.CharField(max_length=50)
    email= models.CharField(max_length=20)
    phone= models.CharField(max_length=10)
    amount= models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return (f'{self.name} {self.email}')
