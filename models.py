import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Partners(Base):
    __tablename__ = "partners"

    id = sq.Column(sq.Integer, primary_key = True)
    id_vk= sq.Column(sq.Integer, unique = True)
    first_name = sq.Column(sq.String())
    last_name = sq.Column(sq.String())
    # bdate = sq.Column(sq.Integer)
    # city = sq.Column(sq.String())
    # user_sex = sq.Column(sq.Integer)
    # relation = sq.Column(sq.Integer)
    pages = sq.Column(sq.String())
    user_id = sq.Column(sq.Integer)

    # contents = relationship("content", back_populates="users")

class Content(Base):

    __tablename__  = "content"

    id_content = sq.Column(sq.Integer, primary_key = True)
    id_user = sq.Column(sq.Integer, sq.ForeignKey("partners.id"),nullable=False)
    url_foto1 = sq.Column(sq.String())
    url_foto2 = sq.Column(sq.String())
    url_foto3 = sq.Column(sq.String())

    # users = relationship("user", back_populates="content")
    users = relationship(Partners, backref="contents")

class User(Base):
    __tablename__ = "user"

    id = sq.Column(sq.Integer, primary_key = True)
    id_vk= sq.Column(sq.Integer, unique = True)
    first_name = sq.Column(sq.String())
    last_name = sq.Column(sq.String())
    bdate = sq.Column(sq.Integer)
    city = sq.Column(sq.String())
    user_sex = sq.Column(sq.Integer)
    relation = sq.Column(sq.Integer)

# class User_Partners(Base):
#     __tablename__ = "user_parthers"
#     user_id = sq.Column(sq.Integer, References=users(User.id)) 
#     partners_id
    def __str__(self):
        return f'{self.id}, ({self.id_vk},{self.first_name},{self.last_name})'

def create_tables(engine):
    Base.metadata.drop_all(engine)   ###  Убрать !
    Base.metadata.create_all(engine)

def drop_tables(engine):
    Base.metadata.drop.Parners(engine)

    