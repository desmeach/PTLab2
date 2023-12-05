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
        if new_quantity < 0:
            return HttpResponse(f'К сожалению, выбранного количества товара нет')
        discount = Discount.get_by_product(product)
        product.price = product.get_discount_price(discount)
        product.quantity = new_quantity
        product.save()
        return HttpResponse(f'Спасибо за покупку, {self.object.person}!')

