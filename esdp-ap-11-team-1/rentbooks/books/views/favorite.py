from django.shortcuts import redirect
from books.models import Book
from django.urls import reverse_lazy


def favorite_unfavor(request, pk):
    curr_user = request.user
    if not curr_user.is_authenticated:
        return redirect('home')
    book = Book.objects.get(pk=pk)
    if curr_user in book.favorites.all():
        book.favorites.remove(curr_user)
        message = f'Пользователь "{request.user.username}" исключил книгу "{book.name}" из избранного (def favor_unfavor)!'
        # logger.info(message)
    else:
        book.favorites.add(curr_user)
        message = f'Пользователь "{request.user.username}" включил книгу "{book.name}" в избранное (def favor_unfavor)!'
        # logger.info(message)
    book.save()
    return redirect(reverse_lazy('detail_book', kwargs={'pk': book.pk}))


def delete_from_favorite(request, pk):
    curr_user = request.user
    if not curr_user.is_authenticated:
        return redirect('home')
    book = Book.objects.get(pk=pk)
    if curr_user in book.favorites.all():
        book.favorites.remove(curr_user)
        book.save()
        message = f'Пользователь "{request.user.username}" исключил книгу "{book.name}" из избранного (def delete_from_favorite)!'
        # logger.info(message)
    return redirect('user_profile')