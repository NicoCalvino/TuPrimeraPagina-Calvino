from django.shortcuts import render
from django.views.generic import ListView, DeleteView, DetailView, UpdateView, CreateView
from django.db.models import Q
from django.urls import reverse_lazy
from productos.models import Producto
from productos.forms import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class SuperUserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

class ProductoListView(ListView):
    model = Producto
    template_name = "productos/productos.html"
    context_object_name = "productos"
    
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("nombre")
        if query:
            queryset = queryset.filter(
                Q(nombre__icontains = query) | Q(marca__icontains=query) | Q(categoria__icontains=query)
            )
        return queryset

class ProductoDetailView(LoginRequiredMixin, DetailView):
    model = Producto
    template_name = "productos/ver_producto.html"
    context_object_name = "producto"
    slug_field ="code"
    slug_url_kwarg = "code"

class ProductoCreateView(SuperUserRequiredMixin, CreateView):
    model = Producto
    template_name = "productos/crear_producto.html"
    form_class = ProductoForm

    def get_success_url(self):
        return reverse_lazy(
            "detalle_producto",
            kwargs={"code":self.object.code}
            )

class ProductoUpdateView(SuperUserRequiredMixin, UpdateView):
    model = Producto
    template_name = "productos/crear_producto.html"
    form_class = ProductoForm
    slug_field ="code"
    slug_url_kwarg = "code"

    def get_success_url(self):
        return reverse_lazy(
            "detalle_producto",
            kwargs={"code":self.object.code}
            )

class ProductoDeleteView(SuperUserRequiredMixin, DeleteView):
    model = Producto
    template_name = "productos/confirm_delete.html"
    success_url = reverse_lazy("lista_productos")
