
import requests

BASE_URL = "https://postman-echo.com"

def test_get_with_query_params():
    # Проверяет, что GET-параметры корректно отражаются в ответе.
    params = {"foo": "bar", "baz": 123}
    response = requests.get(f"{BASE_URL}/get", params=params)
    assert response.status_code == 200
    data = response.json()
    expected = {k: str(v) for k, v in params.items()}
    assert data["args"] == expected
    assert "url" in data
    assert data["url"].startswith(BASE_URL)

def test_post_json():
   # Проверяет, что POST с JSON-телом возвращает его в поле 'json'.
    payload = {"name": "John", "age": 30}
    response = requests.post(f"{BASE_URL}/post", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["json"] == payload
    assert "headers" in data

def test_post_form_data():
    # Проверяет, что POST с form-data возвращает данные в поле 'form'.
    data = {"username": "testuser", "password": "secret"}
    response = requests.post(f"{BASE_URL}/post", data=data)
    assert response.status_code == 200
    result = response.json()
    assert result["form"] == data

def test_get_headers_echo():
    # Проверяет, что сервер возвращает отправленные заголовки.
    custom_headers = {"X-Custom-Header": "my-value", "User-Agent": "pytest-test"}
    response = requests.get(f"{BASE_URL}/get", headers=custom_headers)
    assert response.status_code == 200
    returned_headers = response.json()["headers"]
    # Сервер может менять регистр ключей, поэтому проверяем через lower()
    assert returned_headers.get("x-custom-header") == "my-value"
    assert returned_headers.get("user-agent") == "pytest-test"

def test_post_with_raw_text():
    # Проверяет, что отправка сырого текста возвращает его в поле 'data'.
    raw_text = "Hello, world!"
    response = requests.post(f"{BASE_URL}/post", data=raw_text,
                             headers={"Content-Type": "text/plain"})
    assert response.status_code == 200
    result = response.json()
    assert result["data"] == raw_text
    # Проверяем, что сервер принял наш Content-Type
    assert result["headers"]["content-type"].startswith("text/plain")