from datetime import datetime
import requests


def get_weather_forecast(today=datetime.today().strftime('%Y-%m-%d'), lat='55.7558', lon='37.6176'):
    """
    Функция для получения прогноза погоды на указанный день по широте и долготе.

    :param lat: Широта (по умолчанию для Москвы)
    :param lon: Долгота (по умолчанию для Москвы)
    :param input_date: Дата в формате 'YYYY-MM-DD'
    """
    url = f'https://api.weather.yandex.ru/v2/forecast?lat={lat}&lon={lon}&limit=7'
    access_key = '67560e0e-9691-4e48-bcab-ae894ab5ae97'

    headers = {
        'X-Yandex-Weather-Key': access_key
    }

    # Выполнение запроса
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()

        # Преобразуем введённую дату в datetime объект
        target_date = datetime.strptime(today, '%Y-%m-%d').date()

        # Проходим по каждому дню в прогнозе
        for day in data['forecasts']:
            # Преобразуем дату прогноза в datetime объект
            forecast_date = datetime.strptime(day['date'], '%Y-%m-%d').date()

            if forecast_date == target_date:
                temperature = day['parts']['day']['temp_avg']  # Средняя температура днём
                condition = day['parts']['day']['condition']  # Погодные условия днём

                return int(temperature), str(condition), today

        return f'Прогноз на {today} не доступен. Доступен только на ближайшие {len(data["forecasts"])} дней.'
    else:
        return f'Ошибка при запросе данных: {response.status_code}. Текст ответа: {response.text}'


# Пример вызова функции:
print(get_weather_forecast())