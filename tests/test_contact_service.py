import pytest

from main import create_app
from app.models import db, Contact
from app.services import ContactService


@pytest.fixture(scope='module')
def setup_database():
    app = create_app()
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()


def test_add_contact(setup_database):
    new_contact = ContactService.add_contact('Ben', 'Koren', '1234567890', 'Tel aviv 11')

    assert new_contact.id is not None
    assert new_contact.first_name == 'Ben'
    assert new_contact.last_name == 'Koren'
    assert new_contact.phone == '1234567890'
    assert new_contact.address == 'Tel aviv 11'
    ContactService.delete_contact(new_contact.id)


def test_get_contacts(setup_database):
    first_contact = ContactService.add_contact('Ben', 'Koren', '1234567890', 'Tel aviv 11')
    second_contact = ContactService.add_contact('Bat', 'Sheva', '0987654321', 'ramat gan 25')

    contacts = ContactService.get_contacts(page=1, per_page=10)

    assert len(contacts.items) == 2
    assert contacts.items[0].first_name == 'Ben'
    assert contacts.items[1].first_name == 'Bat'
    ContactService.delete_contact(first_contact.id)
    ContactService.delete_contact(second_contact.id)


def test_search_contacts(setup_database):
    first_contact = ContactService.add_contact('Ben', 'Koren', '1234567890', 'Tel aviv 11')
    second_contact = ContactService.add_contact('Bat', 'Sheva', '0987654321', 'ramat gan 25')

    results = ContactService.search_contacts('Ben')

    assert len(results) == 1
    assert results[0].first_name == 'Ben'
    ContactService.delete_contact(first_contact.id)
    ContactService.delete_contact(second_contact.id)


def test_edit_contact(setup_database):
    new_contact = ContactService.add_contact('Ben', 'Koren', '1234567890', 'Tel aviv 11')

    edited_contact = ContactService.edit_contact(new_contact.id, first_name='Benny', address='rosh pina 11')

    assert edited_contact.id == new_contact.id
    assert edited_contact.first_name == 'Benny'
    assert edited_contact.address == 'rosh pina 11'
    ContactService.delete_contact(new_contact.id)


def test_delete_contact(setup_database):
    new_contact = ContactService.add_contact('Ben', 'Koren', '1234567890', 'Tel aviv 11')

    ContactService.delete_contact(new_contact.id)

    with pytest.raises(Exception):
        Contact.query.filter_by(id=new_contact.id).one()


if __name__ == '__main__':
    pytest.main()
