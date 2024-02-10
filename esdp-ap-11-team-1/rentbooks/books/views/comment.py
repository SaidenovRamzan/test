from django.shortcuts import get_object_or_404, redirect
from books.models import Book, Comment
from django.urls import reverse_lazy


def add_comment(request, pk):
    book = get_object_or_404(Book, pk=pk)
    current_user = request.user
    if not current_user:
        # messages.warning(request, message: "Вы не авторизованы!")
        return redirect('home')
    if request.method == "POST":
        text = (request.POST.get('comment'))
        comment = Comment()
        comment.text = text
        comment.book_id = book.id
        comment.user_id = current_user.id
        comment.save()

    return redirect(reverse_lazy('detail_book', kwargs={'pk': book.pk}))