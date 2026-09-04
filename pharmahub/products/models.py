from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    description = models.TextField()
    stock = models.IntegerField()
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    def __str__(self):
        return self.name
    
class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)



class Order(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)