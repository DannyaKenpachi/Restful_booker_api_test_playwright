from playwright.sync_api import APIRequestContext, Playwright
import pytest

@pytest.fixture(scope='session')
def api_context(playwright: Playwright):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    request_context = playwright.request.new_context(
        base_url="https://restful-booker.herokuapp.com",
        extra_http_headers=headers
    )
    yield request_context
    request_context.dispose()

@pytest.fixture(scope='session')
def auth_token(api_context:APIRequestContext):
    response = api_context.post('/auth', data={
        "username" : "admin",
        "password" : "password123"
    })
    assert response.ok
    result = response.json()
    assert 'token' in result, f"В ответе нет поля 'token'. Ответ сервера: {result}"
    assert result['token'], 'Токен вернулся пустой!'
    yield result['token']

@pytest.fixture(scope='function')
def create_booking(api_context:APIRequestContext):
    new_book = {
        "firstname" : "Jim",
        "lastname" : "Brown",
        "totalprice" : 111,
        "depositpaid" : True,
        "bookingdates" : {
            "checkin" : "2018-01-01",
            "checkout" : "2019-01-01"
        },
        "additionalneeds" : "Breakfast"
    }
    response = api_context.post('/booking', data=new_book)
    assert response.ok
    result = response.json()
    assert 'bookingid' in result
    book_id = result['bookingid']
    yield book_id, new_book