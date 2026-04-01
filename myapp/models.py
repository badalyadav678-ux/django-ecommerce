from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    def __str__(self):
        return self.name


class Order(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    total_price = models.IntegerField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"
    
class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # ✅ ADD THIS
    message = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.user.username}"
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"