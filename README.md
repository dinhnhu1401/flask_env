# flask_env
Flask Python - Corey Schafer



My note

Part 3:
import secrets
>>> secrets.token_hex()
'a779dc4829fc55ab28ef032181b051af96e660e1afa23a900985eb05715ddd21'
>>> secrets.token_hex(16)
'0007e0e77196b310f124fb653e1ef277'

Part4:

Luc chua to chuc lai project
from app import db, User, Post
db.create_all()
db.drop_all()

u1 = User(username='nameA', email='mailA@gmail.com', password='passA')
db.session.add(u1)
>>> db.session.commit()
>>> User.query.all()
[User('nameA', 'mailA@gmail.com', 'default.jpg'), User('nameB', 'mailB@gmail.com', 'default.jpg'), User('name3', 'mail3@gmail.com', 'default.jpg')]
>>> User.query.first()
>>> User.query.filter_by(username='nameBdsf').all()
[]
>>> User.query.filter_by(username='nameB').all()
[User('nameB', 'mailB@gmail.com', 'default.jpg')]