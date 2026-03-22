import argparse
import sys

from contact_book.contacts import ContactBook


def cmd_add(book, args):
    book.add_contact(args.name, args.phone, args.email)
    print(f"Added {args.name}")


def cmd_list(book, args):
    contacts = book.list_contacts()
    if not contacts:
        print("No contacts found")
        return
    for c in contacts:
        print(f"{c['name']}  |  {c['phone']}  |  {c['email']}")


def cmd_search(book, args):
    results = book.search_contact(args.name)
    if not results:
        print("No contacts found")
        return
    for c in results:
        print(f"{c['name']}  |  {c['phone']}  |  {c['email']}")


def cmd_delete(book, args):
    book.delete_contact(args.name)
    print(f"Deleted contacts matching '{args.name}'")


def build_parser():
    parser = argparse.ArgumentParser(
        prog="contact_book",
        description="Simple command-line contact book",
    )
    parser.add_argument(
        "--file",
        default="contacts.json",
        metavar="FILE",
        help="Path to the contacts JSON file (default: contacts.json)",
    )

    subparsers = parser.add_subparsers(dest="command", metavar="COMMAND")
    subparsers.required = True

    # add
    p_add = subparsers.add_parser("add", help="Add a new contact")
    p_add.add_argument("--name", required=True, help="Contact name")
    p_add.add_argument("--phone", required=True, help="Phone number")
    p_add.add_argument("--email", required=True, help="Email address")

    # list
    subparsers.add_parser("list", help="List all contacts")

    # search
    p_search = subparsers.add_parser("search", help="Search contacts by name")
    p_search.add_argument("--name", required=True, help="Name (or partial name) to search")

    # delete
    p_delete = subparsers.add_parser("delete", help="Delete contacts matching a name")
    p_delete.add_argument("--name", required=True, help="Name (or partial name) to delete")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    book = ContactBook(args.file)

    dispatch = {
        "add": cmd_add,
        "list": cmd_list,
        "search": cmd_search,
        "delete": cmd_delete,
    }
    dispatch[args.command](book, args)


if __name__ == "__main__":
    main()
