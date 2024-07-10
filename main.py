import logging
from flask import Flask, jsonify, abort, request
from app import db
from app.services import ContactService


def create_app():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///phonebook.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.errorhandler(400)
    def bad_request(error):
        logger.error(f'Bad request: {str(error)}')
        return jsonify({'error': 'Bad request', 'message': str(error)}), 400

    @app.errorhandler(404)
    def not_found(error):
        logger.error(f'Not found: {str(error)}')
        return jsonify({'error': 'Not found', 'message': str(error)}), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        logger.error(f'Internal server error: {str(error)}')
        return jsonify({'error': 'Internal server error', 'message': str(error)}), 500

    @app.route('/contacts', methods=['GET'])
    def get_contacts():
        page = request.args.get('page', 1, type=int)
        per_page = 10
        logger.info(f'Fetching contacts - page: {page}, per_page: {per_page}')
        contacts = ContactService.get_contacts(page, per_page)
        logger.info(f'Retrieved {len(contacts.items)} contacts')
        return jsonify([contact.to_dict() for contact in contacts.items])

    @app.route('/contacts/search', methods=['GET'])
    def search_contacts():
        query = request.args.get('query', '')
        logger.info(f'Searching contacts with query: {query}')
        contacts = ContactService.search_contacts(query)
        logger.info(f'Found {len(contacts)} contacts matching query')
        return jsonify([contact.to_dict() for contact in contacts])

    @app.route('/contacts', methods=['POST'])
    def add_contact():
        data = request.json
        required_fields = ['first_name', 'last_name', 'phone']

        for field in required_fields:
            if field not in data:
                message = f'Missing required field: {field}'
                logger.error(message)
                return jsonify({'error': 'Bad request', 'message': message}), 400

        try:
            new_contact = ContactService.add_contact(
                first_name=data['first_name'],
                last_name=data['last_name'],
                phone=data['phone'],
                address=data.get('address', '')
            )
            logger.info(f'Added contact with ID: {new_contact.id}')
            return jsonify({'message': 'Contact added successfully', 'contact': new_contact.to_dict()}), 201
        except Exception as e:
            logger.error(f'Error adding contact: {str(e)}')
            abort(500, description=str(e))

    @app.route('/contacts/<int:id>', methods=['PUT'])
    def edit_contact(id):
        data = request.json
        try:
            edited_contact = ContactService.edit_contact(id, data.get('first_name'), data.get('last_name'),
                                                         data.get('phone'), data.get('address'))
            logger.info(f'Updated contact with ID: {edited_contact.id}')
            return jsonify({'message': 'Contact updated successfully', 'contact': edited_contact.to_dict()}), 200
        except Exception as e:
            logger.error(f'Error editing contact: {str(e)}')
            abort(500, description=str(e))

    @app.route('/contacts/<int:id>', methods=['DELETE'])
    def delete_contact(id):
        try:
            ContactService.delete_contact(id)
            logger.info(f'Deleted contact with ID: {id}')
            return jsonify({'message': 'Contact deleted successfully'})
        except Exception as e:
            logger.error(f'Error deleting contact: {str(e)}')
            abort(500, description=str(e))

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', debug=True)
