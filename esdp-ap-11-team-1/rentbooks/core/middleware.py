import logging
import re
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse

from books.models import Book

logger = logging.getLogger('main')


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print('begin call')
        logger.info(f"Request path: {request.path}, method: {request.method}, user: {request.user}, id: {request.user.id}")


# Логирование информации по приложению accounts
        Anonym = request.user
        if request.path == '/login/' and request.method == 'GET':
            message = f'Пользователь {Anonym} открыл форму входа в систему'
            logger.info(message)

        if request.path == '/login/' and request.method == 'POST':
            if 'Anonym' in str(Anonym):
                message = f'Пользователь {Anonym} пытается войти в систему'
                logger.info(message)


        if request.path == '/auth/accounts/profile/' and request.method == 'GET':
            message = f'Пользователь {request.user.username} вошел в личный кабинет'
            logger.info(message)

        if 'accounts/profile/update/' in request.path and request.method == 'GET':
            message = f'Пользователь {request.user.username} зашел на форму изменения личных данных'
            logger.info(message)

        if 'accounts/profile/update/' in request.path and request.method == 'POST':
            message = f'Пользователь {request.user.username} внес изменения в личные данные'
            logger.info(message)

        if request.path == '/logout/' and request.method == 'GET':
            message = f'Пользователь {request.user.username} вышел из системы'
            logger.info(message)

        if request.path == '/' and request.method == 'GET':
            message = f'Пользователь {request.user.username} зашел на главную страницу'
            logger.info(message)

        if request.path == '/auth/accounts/register/' and request.method == 'GET':
            message = f'Пользователь {request.user} зашел в форму регистрации'
            logger.info(message)

        if request.path == '/auth/accounts/register/' and request.method == 'POST':
            message = f'Пользователь {request.user} создал свою учетную запись'
            logger.info(message)

# Логирование информации по приложению web

        if request.path == '/book_create/' and request.method == 'POST':
            message = f'Пользователь {request.user.username} создал новую книгу '
            logger.info(message)

        if request.path == '/books/' and request.method == 'GET':
            message = f'Пользователь {request.user.username} просматривает список найденных книг'
            logger.info(message)

        if 'details' in request.path:
            shablon = '\/book\/\d+\/details\/'
            match = re.match(shablon, request.path)
            if match != None:
                nums = re.findall(r'\d+', request.path)
                str_pk = nums[0]
                pk = int(str_pk)
                book = Book.objects.get(pk=pk)
                message = f' Class: "BookDetailView", Пользователь {request.user.username} просматривает информацию о книге "{book.name}"'
                logger.info(message)

        if 'update' in request.path:
            shablon = '\/book\/\d+\/update\/'
            match = re.match(shablon, request.path)
            if match != None:
                nums = re.findall(r'\d+', request.path)
                str_pk = nums[0]
                pk = int(str_pk)
                book = Book.objects.get(pk=pk)
                message = f'Пользователь {request.user.username} редактирует информацию о книге "{book.name}"'
                logger.info(message)

        if 'delete' in request.path and request.method == 'GET':
            shablon = '\/book\/\d+\/delete\/'
            match = re.match(shablon, request.path)
            if match != None:
                nums = re.findall(r'\d+', request.path)
                str_pk = nums[0]
                pk = int(str_pk)
                book = Book.objects.get(pk=pk)
                message = f'Пользователь {request.user.username} открыл форму удаления книги "{book.name}"'
                logger.info(message)

        if 'delete' in request.path and request.method == 'POST':
            shablon = '\/book\/\d+\/delete\/'
            match = re.match(shablon, request.path)
            if match != None:
                nums = re.findall(r'\d+', request.path)
                str_pk = nums[0]
                pk = int(str_pk)
                book = Book.objects.get(pk=pk)
                message = f'Пользователь {request.user.username} удалил книгу "{book.name}"'
                logger.info(message)

        if 'to_favor' in request.path:
            shablon = '\/book\/\d+\/to_favor\/'
            match = re.match(shablon, request.path)
            if match != None:
                nums = re.findall(r'\d+', request.path)
                str_pk = nums[0]
                pk = int(str_pk)
                book = Book.objects.get(pk=pk)
                curr_user = request.user
                if curr_user in book.favorites.all():
                    state_favor = 'исключает из списка'
                else:
                    state_favor = 'включает в список'

                message = f'def "favor_unfavor", Пользователь {request.user.username} {state_favor} избранных книгу "{book.name}"'
                logger.info(message)

        if 'delete_favorite' in request.path:
            shablon = '\/book\/\d+\/delete_favorite\/'
            match = re.match(shablon, request.path)
            if match != None:
                nums = re.findall(r'\d+', request.path)
                str_pk = nums[0]
                pk = int(str_pk)
                book = Book.objects.get(pk=pk)
                curr_user = request.user
                if curr_user in book.favorites.all():
                    state_favor = 'исключает из списка'

                message = f'Пользователь {request.user.username} {state_favor} избранных книгу "{book.name}"'
                logger.info(message)

        if 'comment_add' in request.path and request.method == 'POST':
            shablon = '\/comment_add\/\d+\/'
            match = re.match(shablon, request.path)
            if match != None:
                nums = re.findall(r'\d+', request.path)
                str_pk = nums[0]
                pk = int(str_pk)
                book = Book.objects.get(pk=pk)
                text = (request.POST.get('comment'))
                message = f'Пользователь {request.user.username} написал комментарий: "{text}" к книге "{book.name}"'
                logger.info(message)


        response = self.get_response(request)


        # Логирование информации о ответе
        # logger.info(f"Состояние запроса: {response.status_code}")

        return response

    def process_exception(self, request, exception):
        message = f'Ошибка: "{exception}" in {path2func(request.path)}'
        logger.info(message)
        return HttpResponse('Произошла ошибка, подробнее в файле information.log. <br/> <br/> <a href="/"> Вернуться на главную страницу </a>')


def path2func(zhol):
    func = ''
    if '/book_create/' in zhol: func = 'web.views.py Класс: BookCreateView'
    if '/details/' in zhol: func = 'web.views.py Класс: BookDetailView'
    if '/update/' in zhol: func = 'web.views.py Класс: BookUpdateView'
    if '/delete/' in zhol: func = 'web.views.py Класс: BookDeleteView'
    if '/books/' in zhol: func = 'web.views.py Класс: BooksView'
    if '/comment_add/' in zhol: func = 'web.views.py Функция: add_comment'
    if '/to_favor/' in zhol: func = 'web.views.py Функция: favor_unfavor'
    if '/delete_favorite/' in zhol: func = 'web.views.py Функция: delete_from_favorite'
    if '/accounts/register/' in zhol: func = 'accounts.views.py Класс: UserRegistrationView'
    if '/accounts/profile/' in zhol: func = 'accounts.views.py Класс: UserProfileView'
    if '/accounts/profile/update/' in zhol: func = 'accounts.views.py Класс: UserProfileUpdateView'
    return func


