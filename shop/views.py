from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import CreateView

from .models import Product, Purchase, Discount


# Create your views here.
def index(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'shop/index.html', context)


class PurchaseCreate(CreateView):
    model = Purchase
    fields = ['product', 'person', 'quantity', 'address']

    def form_valid(self, form):
        self.object = form.save()
        product = Product.objects.get(id=self.object.product.id)
        new_quantity = product.quantity - self.object.quantity
        new_price = product.price
        if new_quantity < 0:
            return HttpResponse(f'К сожалению, выбранного количества товара нет')
        discount_quantity = product.quantity
        discount_percentage = 0.2
        if Discount.objects.filter(product=self.object.product.id).exists():
            discount = Discount.objects.get(product=self.object.product)
            discount_quantity = discount.start_quantity
            discount_percentage = discount.discount_percentage
        else:
            Discount.objects.create(
                product=self.object.product,
                start_quantity=product.quantity,
                discount_percentage=discount_percentage
            )
        if new_quantity <= discount_quantity // 2 < product.quantity:
            new_price = product.price * (1 + discount_percentage)
        product.price = new_price
        product.quantity = new_quantity
        product.save()
        return HttpResponse(f'Спасибо за покупку, {self.object.person}!')

