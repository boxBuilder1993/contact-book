"""CLI integration tests for contact_book via subprocess."""
import subprocess
import sys

import pytest

# Root of the cloned repository — used as cwd so 'contact_book' is importable.
import pathlib

REPO_ROOT = str(pathlib.Path(__file__).resolve().parent.parent)


def run_cli(args, tmp_file):
    """Run `python -m contact_book --file <tmp_file> <args>` and return CompletedProcess."""
    cmd = [sys.executable, "-m", "contact_book", "--file", str(tmp_file)] + args
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )


def test_cli_add(tmp_path):
    """`add` command exits with code 0 and prints a confirmation message."""
    db = tmp_path / "contacts.json"
    result = run_cli(["add", "--name", "Alice Smith", "--phone", "555-1234", "--email", "alice@example.com"], db)

    assert result.returncode == 0
    assert "Alice Smith" in result.stdout


def test_cli_list_shows_added_contact(tmp_path):
    """`list` command shows all previously added contacts."""
    db = tmp_path / "contacts.json"

    # Add two contacts
    run_cli(["add", "--name", "Bob Jones", "--phone", "555-9999", "--email", "bob@example.com"], db)
    run_cli(["add", "--name", "Carol White", "--phone", "555-0000", "--email", "carol@example.com"], db)

    result = run_cli(["list"], db)

    assert result.returncode == 0
    assert "Bob Jones" in result.stdout
    assert "Carol White" in result.stdout


def test_cli_list_empty(tmp_path):
    """`list` on an empty contact book prints an appropriate message."""
    db = tmp_path / "contacts.json"
    result = run_cli(["list"], db)

    assert result.returncode == 0
    assert "No contacts found" in result.stdout


def test_cli_search_returns_correct_result(tmp_path):
    """`search` returns the matching contact and not unrelated ones."""
    db = tmp_path / "contacts.json"
    run_cli(["add", "--name", "Dave Brown", "--phone", "555-1111", "--email", "dave@example.com"], db)
    run_cli(["add", "--name", "Eve Green", "--phone", "555-2222", "--email", "eve@example.com"], db)

    result = run_cli(["search", "--name", "Dave"], db)

    assert result.returncode == 0
    assert "Dave Brown" in result.stdout
    assert "Eve Green" not in result.stdout


def test_cli_search_no_match(tmp_path):
    """`search` with a name that doesn't match prints an appropriate message."""
    db = tmp_path / "contacts.json"
    run_cli(["add", "--name", "Frank Hall", "--phone", "555-3333", "--email", "frank@example.com"], db)

    result = run_cli(["search", "--name", "NoSuchPerson"], db)

    assert result.returncode == 0
    assert "No contacts found" in result.stdout


def test_cli_delete_removes_contact(tmp_path):
    """`delete` removes the contact; subsequent `list` confirms absence."""
    db = tmp_path / "contacts.json"
    run_cli(["add", "--name", "Grace King", "--phone", "555-4444", "--email", "grace@example.com"], db)
    run_cli(["add", "--name", "Henry Lane", "--phone", "555-5555", "--email", "henry@example.com"], db)

    del_result = run_cli(["delete", "--name", "Grace King"], db)
    assert del_result.returncode == 0

    list_result = run_cli(["list"], db)
    assert "Grace King" not in list_result.stdout
    assert "Henry Lane" in list_result.stdout


def test_cli_delete_nonexistent(tmp_path):
    """`delete` with a name that doesn't exist exits cleanly without error."""
    db = tmp_path / "contacts.json"
    run_cli(["add", "--name", "Iris Pond", "--phone", "555-6666", "--email", "iris@example.com"], db)

    result = run_cli(["delete", "--name", "DoesNotExist"], db)

    assert result.returncode == 0

    # Existing contact should be untouched
    list_result = run_cli(["list"], db)
    assert "Iris Pond" in list_result.stdout


def test_cli_add_then_search_then_delete_workflow(tmp_path):
    """Full workflow: add → search → delete → verify removal."""
    db = tmp_path / "contacts.json"

    # Add
    add_result = run_cli(
        ["add", "--name", "Jack Reed", "--phone", "555-7777", "--email", "jack@example.com"], db
    )
    assert add_result.returncode == 0

    # Search
    search_result = run_cli(["search", "--name", "Jack Reed"], db)
    assert search_result.returncode == 0
    assert "Jack Reed" in search_result.stdout

    # Delete
    delete_result = run_cli(["delete", "--name", "Jack Reed"], db)
    assert delete_result.returncode == 0

    # Verify removal
    list_result = run_cli(["list"], db)
    assert "Jack Reed" not in list_result.stdout
