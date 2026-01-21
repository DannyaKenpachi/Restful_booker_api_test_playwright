from playwright.sync_api import APIRequestContext, expect
import pytest
import allure

@allure.feature('Бронирование (Booking API)')
@allure.story('Получение списка бронирований')
@allure.title('Проверка получения всех ID бронирований')
def test_get_booking_ids(api_context: APIRequestContext):
    with allure.step('Отправка GET запроса на /booking'):
        response = api_context.get('/booking')
    with allure.step('Проверка статус кода 200'):
        assert response.ok
    with allure.step('Проверка, что список не пустой'):
        result = response.json()
        assert len(result) > 0

@allure.story('Получение конкретной брони')
@allure.title('Проверка получения брони по ID')
def test_get_booking(api_context:APIRequestContext, create_booking):
    book_id, book_info = create_booking
    with allure.step('Запрос данных для ID {book_id}'):
        response = api_context.get(f'/booking/{book_id}')
    with allure.step('Сравнение полученных данных с ожидаемыми'):
        assert response.ok
        result = response.json()
        assert result == book_info

@allure.story('Изменение брони')
@allure.title('Полное обновление брони (PUT)')
def test_update_booking(api_context:APIRequestContext, create_booking, auth_token):
    book_id, book_info = create_booking
    with allure.step('Подготовка новых данных (изменение имени)'):
        book_info['firstname'] = 'James'
    with allure.step('Отправка PUT запроса с токеном'):
        response = api_context.put(f'/booking/{book_id}',data=book_info, headers={
            'Cookie': f'token={auth_token}'
        })
    with allure.step('Сравнение полученных данных с ожидаемыми'):
        assert response.ok
        result = response.json()
        assert result['firstname'] == 'James'

@allure.story('Изменение брони')
@allure.title('Полное обновление брони (PATCH)')
def test_partial_update_booking(api_context:APIRequestContext, create_booking, auth_token):
    book_id, book_info = create_booking
    with allure.step('Подготовка новых данных(изменяем Имени и Фамилии в брони)'):
        patch_data = {
        "firstname": "James",
        "lastname": "White"
        }
    with allure.step('Отправка PATCH запроса с токеном'):
        response = api_context.patch(f'/booking/{book_id}', data=patch_data, headers={
            'Cookie': f'token={auth_token}'
        })
    with allure.step('Сравнение полученных данных с ожидаемыми'):
        assert response.ok
        result = response.json()
        assert result['firstname'] == patch_data['firstname']
        assert result['lastname'] == patch_data['lastname']

@allure.story('Удаление брони')
@allure.title("Удаление существующей брони (DELETE)")
def test_delete_booking(api_context:APIRequestContext, auth_token, create_booking):
    book_id, book_info = create_booking
    with allure.step(f"Удаление брони {book_id}"):
        response = api_context.delete(f'/booking/{book_id}', headers={
            'Cookie': f'token={auth_token}'
        })
    with allure.step("Проверка, что бронь удалена (ожидаем 404)"):
        assert response.ok
        check_response = api_context.get(f'/booking/{book_id}')
        assert check_response.status == 404
