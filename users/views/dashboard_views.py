from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views import View
from django.urls import reverse

from products.models import Product
from users.forms.product_form import UserProductForm


@login_required(login_url='users:login', redirect_field_name='next')
def Dashboard(request):
    products = Product.objects.filter(
        is_published=False,
        author=request.user,
    )

    return render(
        request, 'pages/dashboard.html',
        context={
            'products': products,
        }
    )


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
class DashboardProduct(View):
    def get_product(self, id=None):
        product = None

        if id is not None:
            product = Product.objects.filter(
                is_published=False,
                author=self.request.user,
                pk=id,
            ).first()

        return product

    def render_product(self, form, product=None):
        return render(
            self.request, 'pages/dashboard_product.html',
            context={
                'form': form,
                'product': product,
            }
        )

    def get(self, request, id=None):
        product = self.get_product(id)
        form = UserProductForm(instance=product)
        return self.render_product(form, product)

    def post(self, request, id=None):
        product = self.get_product(id)
        form = UserProductForm(
            data=request.POST or None,
            files=request.FILES or None,
            instance=product,
        )

        if form.is_valid():
            product = form.save(commit=False)

            product.author = request.user
            product.is_published = False

            if 'cover' in request.FILES:
                product.cover = request.FILES['cover']

            product.save()

            messages.success(request, 'Your product has been saved successfully')
            return redirect(reverse(
                'users:dashboard_product_edit', args=(product.id,)))

        return self.render_product(form, product)


@method_decorator(
    login_required(login_url='users:login', redirect_field_name='next'),
    name='dispatch'
)
class DashboardProductDelete(DashboardProduct):
    def post(self, *args, **kwargs):
        product = self.get_product(self.request.POST.get('id'))
        product.delete()  # type: ignore
        messages.success(self.request, 'Product deleted successfully')
        return redirect(reverse('users:dashboard'))