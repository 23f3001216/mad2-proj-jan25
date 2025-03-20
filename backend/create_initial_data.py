from flask import current_app as app
from backend.models import db
from flask_security import SQLAlchemyUserDatastore, hash_password

with app.app_context():
    db.create_all()

    userdatastore : SQLAlchemyUserDatastore = app.security.datastore

    userdatastore.find_or_create_role(name = 'admin', description = 'superuser')
    userdatastore.find_or_create_role(name = 'user', description = 'general customer')
    # userdatastore.find_or_create_role(name = 'customer', description = 'general customer')
    # userdatastore.find_or_create_role(name = 'professional', description = 'professional')

    if (not userdatastore.find_user(email = 'admin@fixitfast.com')):
        userdatastore.create_user(email = 'admin@fixitfast.com', password = hash_password('admin'), roles = ['admin'])

    db.session.commit()