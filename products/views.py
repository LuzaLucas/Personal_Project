from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Product


class IndexListView(ListView):
    template_name = 'index.html'
    model = Product
    paginate_by = 3
    ordering = '-id'
    
    def get_queryset(self):
        return Product.objects.filter(is_published=True).order_by(self.ordering)
    
    
class CreateProductView(CreateView):
    model = Product
    template_name = 'product_form.html'
    fields = ['name', 'stock', 'price', 'description']
    success_url = reverse_lazy('index')
    
    
class UpdateProductView(UpdateView):
    model = Product
    template_name = 'product_form.html'
    fields = ['name', 'stock', 'price', 'description']
    success_url = reverse_lazy('index')
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.is_published = False
        self.object.save()
        return super().form_valid(form)
    
    
class DeleteProductView(DeleteView):
    model = Product
    template_name = 'product_del.html'
    success_url = reverse_lazy('index')
