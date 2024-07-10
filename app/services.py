import logging
from app import db
from app.models import Contact

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ContactService:
    @staticmethod
    def get_contacts(page=1, per_page=10):
        logger.info(f'Fetching contacts - page: {page}, per_page: {per_page}')
        contacts = Contact.query.paginate(page=page, per_page=per_page, error_out=False)
        logger.info(f'Retrieved {len(contacts.items)} contacts')
        return contacts

    @staticmethod
    def search_contacts(query):
        logger.info(f'Searching contacts with query: {query}')
        results = Contact.query.filter(
            (Contact.first_name.ilike(f'%{query}%')) |
            (Contact.last_name.ilike(f'%{query}%')) |
            (Contact.phone.ilike(f'%{query}%')) |
            (Contact.address.ilike(f'%{query}%'))
        ).all()
        logger.info(f'Found {len(results)} contacts matching query')
        return results

    @staticmethod
    def add_contact(first_name, last_name, phone, address=''):
        logger.info(f'Adding contact: First name: {first_name}  Last name: {last_name}, Phone: {phone}, Address: {address}')
        new_contact = Contact(first_name=first_name, last_name=last_name, phone=phone, address=address)
        db.session.add(new_contact)
        db.session.commit()
        logger.info(f'Added contact with ID: {new_contact.id}')
        return new_contact

    @staticmethod
    def edit_contact(person_id, first_name=None, last_name=None, phone=None, address=None):
        logger.info(f'Editing contact with ID: {person_id}')
        contact = Contact.query.get_or_404(person_id, description='ID is not found.')
        if first_name:
            contact.first_name = first_name
        if last_name:
            contact.last_name = last_name
        if phone:
            contact.phone = phone
        if address:
            contact.address = address
        db.session.commit()
        logger.info(f'Updated contact with ID: {contact.id}')
        return contact

    @staticmethod
    def delete_contact(person_id):
        logger.info(f'Deleting contact with ID: {person_id}')
        contact = Contact.query.get_or_404(person_id, description='ID is not found.')
        db.session.delete(contact)
        db.session.commit()
        logger.info(f'Deleted contact with ID: {contact.id}')
