"""Unit tests for the ContactBook class."""
import json

import pytest

from contact_book.contacts import ContactBook


def test_add_contact(tmp_path):
    """Add a contact and verify it appears in list_contacts()."""
    db = tmp_path / "contacts.json"
    book = ContactBook(str(db))

    book.add_contact("Alice Smith", "555-1234", "alice@example.com")

    contacts = book.list_contacts()
    assert len(contacts) == 1
    assert contacts[0]["name"] == "Alice Smith"
    assert contacts[0]["phone"] == "555-1234"
    assert contacts[0]["email"] == "alice@example.com"


def test_search_contact_found(tmp_path):
    """Search returns the correct contact when a match exists."""
    db = tmp_path / "contacts.json"
    book = ContactBook(str(db))
    book.add_contact("Bob Jones", "555-9999", "bob@example.com")
    book.add_contact("Carol White", "555-0000", "carol@example.com")

    results = book.search_contact("Bob")

    assert len(results) == 1
    assert results[0]["name"] == "Bob Jones"


def test_search_contact_case_insensitive(tmp_path):
    """Search is case-insensitive."""
    db = tmp_path / "contacts.json"
    book = ContactBook(str(db))
    book.add_contact("Dave Brown", "555-1111", "dave@example.com")

    results = book.search_contact("dave")
    assert len(results) == 1
    assert results[0]["name"] == "Dave Brown"


def test_search_contact_not_found(tmp_path):
    """Search returns an empty list when there is no match."""
    db = tmp_path / "contacts.json"
    book = ContactBook(str(db))
    book.add_contact("Eve Green", "555-2222", "eve@example.com")

    results = book.search_contact("NoSuchPerson")

    assert results == []


def test_delete_contact(tmp_path):
    """Delete removes the matching contact from the list."""
    db = tmp_path / "contacts.json"
    book = ContactBook(str(db))
    book.add_contact("Frank Hall", "555-3333", "frank@example.com")
    book.add_contact("Grace King", "555-4444", "grace@example.com")

    book.delete_contact("Frank Hall")

    contacts = book.list_contacts()
    assert len(contacts) == 1
    assert contacts[0]["name"] == "Grace King"


def test_delete_contact_missing(tmp_path):
    """Deleting a non-existent name does not raise and leaves other contacts intact."""
    db = tmp_path / "contacts.json"
    book = ContactBook(str(db))
    book.add_contact("Henry Lane", "555-5555", "henry@example.com")

    # Should not raise
    book.delete_contact("DoesNotExist")

    contacts = book.list_contacts()
    assert len(contacts) == 1
    assert contacts[0]["name"] == "Henry Lane"


def test_json_persistence(tmp_path):
    """Data written by one ContactBook instance survives a reload from the same file."""
    db = tmp_path / "contacts.json"

    book1 = ContactBook(str(db))
    book1.add_contact("Iris Pond", "555-6666", "iris@example.com")
    book1.add_contact("Jack Reed", "555-7777", "jack@example.com")

    # Load from the same file with a new instance
    book2 = ContactBook(str(db))
    contacts = book2.list_contacts()

    assert len(contacts) == 2
    names = [c["name"] for c in contacts]
    assert "Iris Pond" in names
    assert "Jack Reed" in names


def test_json_file_format(tmp_path):
    """Saved file is valid JSON containing the expected contact data."""
    db = tmp_path / "contacts.json"
    book = ContactBook(str(db))
    book.add_contact("Karen Fox", "555-8888", "karen@example.com")

    with open(str(db)) as f:
        data = json.load(f)

    assert isinstance(data, list)
    assert data[0]["name"] == "Karen Fox"


def test_duplicate_handling(tmp_path):
    """Adding the same name twice results in two separate entries."""
    db = tmp_path / "contacts.json"
    book = ContactBook(str(db))
    book.add_contact("Leo Star", "555-0001", "leo1@example.com")
    book.add_contact("Leo Star", "555-0002", "leo2@example.com")

    contacts = book.list_contacts()
    assert len(contacts) == 2
    # Both entries are preserved
    phones = {c["phone"] for c in contacts}
    assert phones == {"555-0001", "555-0002"}


def test_empty_contact_book(tmp_path):
    """A newly created ContactBook starts with zero contacts."""
    db = tmp_path / "contacts.json"
    book = ContactBook(str(db))

    assert book.list_contacts() == []


def test_multiple_search_results(tmp_path):
    """Search returns all contacts whose names contain the query string."""
    db = tmp_path / "contacts.json"
    book = ContactBook(str(db))
    book.add_contact("Smith Alice", "555-1001", "salice@example.com")
    book.add_contact("Smith Bob", "555-1002", "sbob@example.com")
    book.add_contact("Jones Carol", "555-1003", "jcarol@example.com")

    results = book.search_contact("Smith")

    assert len(results) == 2
    names = {c["name"] for c in results}
    assert names == {"Smith Alice", "Smith Bob"}
