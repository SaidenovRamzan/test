from typing import Any, Dict
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from rents.models import OrderOfRent, UserImages
from books.models import Book
import base64

from rents.models.user_shelf import UserShelf


class OrderListView(LoginRequiredMixin, ListView):
    model = OrderOfRent
    template_name = 'rents/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return OrderOfRent.objects.filter(user=self.request.user)
    

class OrderDetailView(LoginRequiredMixin, DetailView):
    model = OrderOfRent
    template_name = 'rents/order_detail.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_object()
        user_shelf = UserShelf.objects.get(pk=order.usershelf_id)
        context['order'] = order
        book = Book.objects.get(id_Book=user_shelf.id_book)
        context['name'] = book.id_composition.name
        context['author'] = book.id_composition.author
        context['coverphoto'] = base64.b64encode(book.coverphoto.read()).decode('utf-8')
        context['user_images'] = self.get_user_images(user_shelf)
        context['izdatelstvo'] = book.izdatelstvo
        context['isbn'] = book.isbn
        context['book_state'] = user_shelf.get_book_state_display()
        context['status'] = user_shelf.get_status_display()
        context['purpose'] = user_shelf.get_purpose_display()
        context['count'] = user_shelf.count
        return context

    def get_user_images(self, user_shelf):
        images = UserImages.objects.filter(book_shelf=user_shelf)
        url_images = [image.image.url for image in images]
        return url_images
