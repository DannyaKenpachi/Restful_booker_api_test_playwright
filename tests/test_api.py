from playwright.sync_api import APIRequestContext, expect
import pytest
import allure

def test_get_booking_ids(api_context: APIRequestContext):
    response = api_context.get('/booking')
    assert response.ok
    result = response.json()
    assert len(result) > 0

def test_get_booking(api_context:APIRequestContext, create_booking):
    book_id, book_info = create_booking
    response = api_context.get(f'/booking/{book_id}')
    assert response.ok
    result = response.json()
    assert result == book_info

def test_update_booking(api_context:APIRequestContext, create_booking, auth_token):
    book_id, book_info = create_booking
    book_info['firstname'] = 'James'
    response = api_context.put(f'/booking/{book_id}',data=book_info, headers={
        'Cookie': f'token={auth_token}'
    })
    assert response.ok
    result = response.json()
    assert result['firstname'] == 'James'

def test_partial_update_booking(api_context:APIRequestContext, create_booking, auth_token):
    book_id, book_info = create_booking
    patch_data = {
        "firstname": "James",
        "lastname": "White"
    }
    response = api_context.patch(f'/booking/{book_id}', data=patch_data, headers={
        'Cookie': f'token={auth_token}'
    })
    assert response.ok
    result = response.json()
    assert result['firstname'] == patch_data['firstname']
    assert result['lastname'] == patch_data['lastname']

def test_delete_booking(api_context:APIRequestContext, auth_token, create_booking):
    book_id, book_info = create_booking
    response = api_context.delete(f'/booking/{book_id}', headers={
        'Cookie': f'token={auth_token}'
    })
    assert response.ok
    check_response = api_context.get(f'/booking/{book_id}')
    assert check_response.status == 404
