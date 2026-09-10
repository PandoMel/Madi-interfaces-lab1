import argparse
import requests

BASE_URL = "http://127.0.0.1:8000"


def print_response(response):
    print(f"HTTP {response.status_code}")
    if response.content:
        print(response.json())


parser = argparse.ArgumentParser(description="CLI для сервиса меню столовой")
subparsers = parser.add_subparsers(dest="command", required=True)

subparsers.add_parser("list")

get_parser = subparsers.add_parser("get")
get_parser.add_argument("id", type=int)

add_parser = subparsers.add_parser("add")
add_parser.add_argument("name")
add_parser.add_argument("category")

update_parser = subparsers.add_parser("update")
update_parser.add_argument("id", type=int)
update_parser.add_argument("name")
update_parser.add_argument("category")

delete_parser = subparsers.add_parser("delete")
delete_parser.add_argument("id", type=int)

subparsers.add_parser("menu")

menu_add_parser = subparsers.add_parser("menu-add")
menu_add_parser.add_argument("date")
menu_add_parser.add_argument("dish_id", type=int)

menu_delete_parser = subparsers.add_parser("menu-delete")
menu_delete_parser.add_argument("date")
menu_delete_parser.add_argument("dish_id", type=int)

args = parser.parse_args()

if args.command == "list":
    response = requests.get(f"{BASE_URL}/dishes")
elif args.command == "get":
    response = requests.get(f"{BASE_URL}/dishes/{args.id}")
elif args.command == "add":
    response = requests.post(
        f"{BASE_URL}/dishes",
        json={"name": args.name, "category": args.category},
    )
elif args.command == "update":
    response = requests.put(
        f"{BASE_URL}/dishes/{args.id}",
        json={"name": args.name, "category": args.category},
    )
elif args.command == "delete":
    response = requests.delete(f"{BASE_URL}/dishes/{args.id}")
elif args.command == "menu":
    response = requests.get(f"{BASE_URL}/menu")
elif args.command == "menu-add":
    response = requests.post(f"{BASE_URL}/menu/{args.date}/dishes/{args.dish_id}")
else:
    response = requests.delete(f"{BASE_URL}/menu/{args.date}/dishes/{args.dish_id}")

print_response(response)
