import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Users, Content, my_data
from config import userdb, passworddb

DSM = f'postgresql://{userdb}:{passworddb}@localhost:5432/vkinder'
engine = sqlalchemy.create_engine(DSM)


def add_my_data(user_id, first_name, last_name, bdate, city, user_sex, relation):
    create_tables(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    my = my_data(id_vk=user_id, first_name=first_name, last_name=last_name, bdate=bdate, city=city, user_sex=user_sex, relation=relation)

    # last_name = my_data(last_name="Бронников")

    session.add(my)
    session.commit()
    print(my.id)

    session.close()