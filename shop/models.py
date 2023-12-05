from django.db import models


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField()
    start_quantity = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=0)

    def get_discount_price(self, discount):
        if self.price <= discount.start_quantity // 2 < self.quantity:
            return self.price * (1 + discount.discount_percentage)
        return self.price


class Purchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    person = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)


class Discount(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    start_quantity = models.PositiveIntegerField(default=0)
    discount_percentage = models.FloatField(default=0.2)

    @staticmethod
    def get_by_product(product):
        if Discount.objects.filter(product=product.id).exists():
            discount = Discount.objects.get(product=product)
        else:
            discount = Discount.objects.create(
                product=product,
                start_quantity=product.quantity
            )
        return discount
