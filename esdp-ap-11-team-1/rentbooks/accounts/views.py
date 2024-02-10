import base64
from typing import Any, Dict
import logging


from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.shortcuts import redirect
from accounts.forms import UserRegistrationForm, UserUpdateForm

from rents.models import UserShelf, OrderOfRent
from books.models import Book, FavoriteBook
from accounts.models import User

from accounts.models import Estimation, UsersEstimates
from rest_framework.reverse import reverse

logger = logging.getLogger('main')


class UserRegistrationView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'registration/login.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('user_profile')


class UserProfileView(DetailView):
    model = User
    template_name = 'user_profile.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.request.user

    def get_user_shelfs(self):
        user_shelfs = UserShelf.objects.all().filter(user=self.request.user.id, is_active=True)
        user_shelf_objects = []
        for user_shelf in user_shelfs:
            book = Book.objects.filter(id_Book=user_shelf.id_book).first()
            user_shelf_objects.append({
                'user_shelf': user_shelf,
                'book': book,
                'coverphoto': base64.b64encode(book.coverphoto.read()).decode('utf-8')
            })
        return user_shelf_objects

    def get_favorites(self):
        favorites = FavoriteBook.objects.filter(user_id=self.request.user.id)
        favorites_objects = []
        for favorite in favorites:
            book = Book.objects.filter(id_composition=favorite.composition_id).first()
            favorites_objects.append({
                'favorite': favorite,
                'book': book,
                'coverphoto': base64.b64encode(book.coverphoto.read()).decode('utf-8')
            })
        return favorites_objects


    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        favorites = FavoriteBook.objects.filter(user_id=self.request.user.id).all()
        favorite_ids = favorites.values_list('composition_id', flat=True)
        context['favorites'] = self.get_favorites()
        context['user_id'] = self.request.user.id
        context['user_shelf_objects'] = self.get_user_shelfs()
        context['orders_to_me'] = self.get_orders_to_me()
        context['my_orders'] = self.get_my_orders()

        return context

    def get_orders_to_me(self):
        try:
            orders = OrderOfRent.objects.filter(usershelf__user_id=self.request.user.id, is_active=True)
        except OrderOfRent.DoesNotExist:
            return None

        orders_objects = []
        for order in orders:
            try:
                book = Book.objects.filter(id_Book=order.usershelf.id_book).first()
                coverphoto = base64.b64encode(book.coverphoto.read()).decode('utf-8')
            except Book.DoesNotExist:
                book = None
                coverphoto = None
            except AttributeError:
                book = None
                coverphoto = None

            orders_objects.append({
                'order': order,
                'book': book,
                'coverphoto': coverphoto
            })

        return orders_objects

    def get_my_orders(self):
        try:
            orders = OrderOfRent.objects.filter(user_id=self.request.user.id, is_active=True)
        except OrderOfRent.DoesNotExist:
            return None

        orders_objects = []
        for order in orders:
            try:
                book = Book.objects.filter(id_Book=order.usershelf.id_book).first()
                coverphoto = base64.b64encode(book.coverphoto.read()).decode('utf-8')
            except Book.DoesNotExist:
                book = None
                coverphoto = None
            except AttributeError:
                book = None
                coverphoto = None

            orders_objects.append({
                'order': order,
                'book': book,
                'coverphoto': coverphoto
            })

        return orders_objects


class UserProfileUpdateView(UpdateView):
    model = User
    template_name = 'registration/login.html'
    form_class = UserUpdateForm
    context_object_name = 'user'
    success_url = reverse_lazy('user_profile')

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            self.object = self.get_object()
            form = self.get_form()
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        else:
            return self.get(request, *args, **kwargs)


def user_ratio(request, pk, rt):    # Функция для оценки пользователя
    owner = User.objects.get(pk=pk)     # получаем владельца страницы
    curr_user = request.user            # получаем текущего пользователя
    if not Estimation.objects.filter(owner_id=pk).exists():
        estimation = Estimation()
        estimation.owner = owner
        estimation.save()

    estimation = Estimation.objects.get(owner_id=pk)

    if not curr_user in estimation.put_ratio.all():
        estimation.put_ratio.add(curr_user)
        estimation.save()

    # Сохранение оценки текущего пользователя
    rating = UsersEstimates.objects.get(estimation=estimation, estimator=curr_user)
    rating.ratio = rt   # Оценка текущего пользователя
    rating.save()

    # Подсчет средней оценки пользователей
    count_ratio = 0
    count_users = 0
    for estimator in estimation.put_ratio.all():
        rating = UsersEstimates.objects.get(estimation=estimation, estimator=estimator)
        count_users += 1
        count_ratio += rating.ratio
    aver_ratio = count_ratio / count_users
    estimation.aver_ratio = aver_ratio
    estimation.save()

    return redirect(reverse('user_page', kwargs={'pk': pk}))


class UserPageView(DetailView):
    model = User
    template_name = 'user_page.html'
    context_object_name = 'account'

    def get_user_shelfs(self, owner):
        bookshelfs = UserShelf.objects.filter(user=owner)
        user_shelf_objects = []
        for user_shelf in bookshelfs:
            book = Book.objects.get(id_Book=user_shelf.id_book)
            user_shelf_objects.append({
                'user_shelf': user_shelf,
                'book': book,
                'coverphoto': base64.b64encode(book.coverphoto.read()).decode('utf-8')
            })

        return user_shelf_objects

    def check_estimation(self, id_owner):
        if not Estimation.objects.filter(owner_id=id_owner).exists():
            estimation = Estimation()
            estimation.owner_id = id_owner
            estimation.save()
        curr_user = self.request.user
        print('open_est')
        estimation = Estimation.objects.get(owner_id=id_owner)
        print('opened_est')

        if not curr_user in estimation.put_ratio.all():
            estimation.put_ratio.add(curr_user)
            estimation.save()

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # print(f'{kwargs = }')
        # print(f'{kwargs["object"].id = }')
        owner = kwargs["object"]
        id_owner = owner.id
        context['user_id'] = self.request.user.id
        context['user_shelf_objects'] = self.get_user_shelfs(owner)
        self.check_estimation(id_owner)
        estimation = Estimation.objects.get(owner_id=id_owner)
        context['aver_ratio'] = estimation.aver_ratio
        rating = UsersEstimates.objects.get(estimator=self.request.user.id, estimation=estimation.id)
        context['ratings'] = str(rating.ratio)  # переводим в строку, т.к. в шаблоне рейтинг сравнивается со строковыми индексами

        return context