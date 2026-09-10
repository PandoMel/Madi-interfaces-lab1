import requests

BASE_URL = "http://127.0.0.1:8000"


def show(title, response):
    print(f"\n{title}: {response.status_code}")
    if response.content:
        print(response.json())


created = requests.post(
    f"{BASE_URL}/dishes",
    json={"name": "Гречка с котлетой", "category": "Горячее"},
)
show("POST /dishes", created)

dish_id = created.json()["id"]

show("GET /dishes", requests.get(f"{BASE_URL}/dishes"))
show("GET /dishes/{id}", requests.get(f"{BASE_URL}/dishes/{dish_id}"))

updated = requests.put(
    f"{BASE_URL}/dishes/{dish_id}",
    json={"name": "Гречка с курицей", "category": "Горячее"},
)
show("PUT /dishes/{id}", updated)

show("DELETE /dishes/{id}", requests.delete(f"{BASE_URL}/dishes/{dish_id}"))
show("GET deleted dish", requests.get(f"{BASE_URL}/dishes/{dish_id}"))
