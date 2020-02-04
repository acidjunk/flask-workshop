import datetime
import uuid

from flask_security import RoleMixin, UserMixin, SQLAlchemySessionUserDatastore
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import Boolean, Column, DateTime, Integer, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref

db = SQLAlchemy()


class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', UUID(as_uuid=True), ForeignKey('users.id'))
    role_id = Column('role_id', UUID(as_uuid=True), ForeignKey('roles.id'))


class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))

    # __str__ is required by Flask-Admin, so we can have human-readable values for the Role when editing a User.
    def __str__(self):
        return self.name

    # __hash__ is required to avoid the exception TypeError: unhashable type: 'Role' when saving a User
    def __hash__(self):
        return hash(self.name)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String(255), unique=True)
    first_name = Column(String(255), index=True)
    last_name = Column(String(255), index=True)
    username = Column(String(255), unique=True)
    password = Column(String(255))
    active = Column(Boolean())
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    confirmed_at = Column(DateTime())
    roles = relationship('Role', secondary='roles_users', backref=backref('users', lazy='dynamic'))

    mail_offers = Column(Boolean, default=False)
    mail_announcements = Column(Boolean, default=True)

    quick_token = Column(String(255), index=True)
    quick_token_created_at = Column(DateTime())

    fs_uniquifier = Column(String(255))

    # Human-readable values for the User when editing user related stuff.
    def __str__(self):
        return f'{self.username} : {self.email}'

    # __hash__ is required to avoid the exception TypeError: unhashable type: 'Role' when saving a User
    def __hash__(self):
        return hash(self.email)


class Tag(db.Model):
    __tablename__ = 'tags'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(60), unique=True, index=True)

    def __repr__(self):
        return self.name


class Todo(db.Model):
    __tablename__ = 'todo_items'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(60), unique=True, index=True)
    description = Column(Text)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    created_by = Column('created_by', UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    todo_tags = relationship("Tag", secondary='todo_tags')
    todo_to_tags = relationship("TodoTag")

    def __repr__(self):
        return self.name


class TodoTag(db.Model):
    __tablename__ = 'todo_tags'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    todo_id = Column('todo_id', UUID(as_uuid=True), ForeignKey('todo_items.id'), index=True)
    tag_id = Column('tag_id', UUID(as_uuid=True), ForeignKey('tags.id'), index=True)
    todo = db.relationship("Todo", lazy=True)
    tag = db.relationship("Tag", lazy=True)

    def __repr__(self):
        return self.tag.name


user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
