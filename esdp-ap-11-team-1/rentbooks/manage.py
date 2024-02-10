#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
    
        # Получение параметров запроса
        status_param = request.query_params.get('status', 'open')
        limit_param = request.query_params.get('limit', 50)
        after_param = request.query_params.get('after', '2000-01-02T15:04:05Z')
        until_param = request.query_params.get('until', '2026-01-02T15:04:05Z')
        direction_param = request.query_params.get('direction', 'desc')
        nested_param = request.query_params.get('nested', False)
        symbols_param = request.query_params.get('symbols', 'AAPL%2CTSLA%2CMSFT')
        qty_above_param = request.query_params.get('qty_above', -10000000000000000)
        qty_below_param = request.query_params.get('qty_below', 1000000000000000000000)
        subtag_param = request.query_params.get('subtag')

        url = f"https://broker-api.sandbox.alpaca.markets/v1/trading/accounts/{account_id}/orders"
        url += f"?limit={str(limit_param)}&status={status_param}&after={after_param}&until={until_param}"
        url += f"&direction={direction_param}&nested={nested_param}&symbols={symbols_param}"
        url += f"&qty_above={str(qty_above_param)}&qty_below={str(qty_below_param)}&subtag={str(subtag_param)}"

        username = os.getenv('API_KEY')
        password = os.getenv('API_SECRET')

        # Объединяем имя пользователя и пароль с помощью двоеточия
        credentials = f"{username}:{password}"

        # Преобразуем строку в формат Base64
        base64_credentials = base64.b64encode(credentials.encode()).decode()

        # Полученный результат
        headers = {
            "accept": "application/json",
            "authorization": f"Basic {base64_credentials}"
        }

        response = requests.get(url, headers=headers)
        data = response.json()
        logging.warning(len(data))
        logging.warning(data)
        
        # Фильтрация заказов на основе параметров запроса
        orders = Order.objects.all()
        if status_param in ['open', 'closed', 'all']:
            if status_param == 'open':
                orders = orders.filter(status='accepted')
            elif status_param == 'closed':
                orders = orders.filter(status='canceled')
        if after_param:
            orders = orders.filter(created_at__gt=after_param)

        if until_param:
            orders = orders.filter(created_at__lt=until_param)

        if symbols_param:
            symbols = symbols_param.split(',')
            orders = orders.filter(symbol__in=symbols)

        if qty_above_param:
            orders = orders.filter(qty__gt=float(qty_above_param))

        if qty_below_param:
            orders = orders.filter(qty__lt=float(qty_below_param))

        if subtag_param:
            orders = orders.filter(subtag=subtag_param)

        # Упорядочивание заказов
        if direction_param == 'asc':
            orders = orders.order_by('created_at')
        else:
            orders = orders.order_by('-created_at')

        # Ограничение количества заказов
        orders = orders[:limit_param]

        # Сериализация и отправка ответа
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
