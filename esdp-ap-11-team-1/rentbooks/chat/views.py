from django.shortcuts import render
import base64
from chat.services import ChatServices
from chat.models import Chat
from accounts.models import User
from rents.models import UserShelf
from books.models import Book


def get_chat(request, *args, **kwargs):
    return render(request, 'message.html')


def get_all_chats(request, *args, **kwargs):
    user_id = request.user.id
    chat_ids = ChatServices.get_all_chats(user_id=user_id)
    user_ids = []
    
    for chat_id in chat_ids:
        chat = Chat.objects.get(id=chat_id)
        user_shelf = UserShelf.objects.get(id=chat.user_shelf)
        book = Book.objects.get(id_Book=user_shelf.id_book)
        if chat.user_1 == user_id:
            user_ids.append((chat.user_2, book, user_shelf))
        else:
            user_ids.append((chat.user_1, book, user_shelf))
          
    users = []
    for user_id, book, user_shelff in user_ids:
        coverphoto = base64.b64encode(book.coverphoto.read()).decode('utf-8')
        users.append((User.objects.get(id=user_id), book, user_shelff, coverphoto))
        
    return render(request, 'chat.html', context={'users': users})
