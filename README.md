### Приложение Django Tree Menu

Это приложение Django реализует древовидную систему меню в соответствии с предоставленными спецификациями. Оно позволяет создавать, управлять и отображать древовидные меню через интерфейс администратора Django и шаблонные теги.

#### Особенности

- Система древовидного меню, реализованная через шаблонные теги
- Элементы меню хранятся в базе данных
- Возможность редактирования через интерфейс администратора Django
- Активный пункт меню определяется на основе текущего URL страницы
- Поддержка нескольких меню на одной странице
- URL меню могут быть явно определены или указаны через именованные URL
- Для отображения каждого меню требуется только один запрос к базе данных

#### Установка

```bash
git clone https://github.com/SaidenovRamzan/test.git
pip install -r requirements.txt
python manage.py runserver
```


Суперпользователь и данные

Суперпользователь уже создан с логином root и паролем root. База данных содержит некоторые тестовые данные.

Перейти в интерфейс администратора Django по адресу http://127.0.0.1:8000/admin/ для создания и управления меню.
Использование

Для отображения меню в шаблонах используйте следующий шаблонный тег:

```bash
{% draw_menu 'main_url' %}
```
