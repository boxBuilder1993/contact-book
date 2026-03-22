# contact-book

A simple command-line contact book written in Python. Store, search, and manage contacts with data persisted in a JSON file.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Run the app as a Python module:

```bash
python -m contact_book [--file FILE] COMMAND [OPTIONS]
```

`--file FILE` — optional path to contacts JSON file (default: `contacts.json`)

### Add a contact

```bash
python -m contact_book add --name "Alice Smith" --phone "555-1234" --email "alice@example.com"
```

### List all contacts

```bash
python -m contact_book list
```

### Search contacts by name

```bash
python -m contact_book search --name "Alice"
```

### Delete a contact

```bash
python -m contact_book delete --name "Alice"
```

## Running Tests

```bash
pytest
```
