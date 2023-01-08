import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, drop_tables, User, Partners, Content
from config import userdb, passworddb

DSM = f'postgresql://{userdb}:{passworddb}@localhost:5432/vkinder'
engine = sqlalchemy.create_engine(DSM)
Session = sessionmaker(bind=engine)

def add_my_data(user_id, first_name, last_name, bdate, city, user_sex, relation):
    session = Session()
    create_tables(engine)
    result_query =[x.id_vk for x in session.query(User.id_vk).distinct()]
    result_search = False

    for vk_id in result_query:
        if vk_id == int(user_id):
            result_search = True
            print("пользователь существует!")
            break
    if result_search == False:
        user = User(id_vk=user_id, first_name=first_name, last_name=last_name, bdate=bdate, city=city, user_sex=user_sex, relation=relation)
        session.add(user)
        session.commit()
        print(user)  
        print("пользователь не существует!")
    session.close()


def add_parthers_data(user_id, first_name, last_name, vk_id, vk_link):
    create_tables(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    # session.query(Partners).delete()
    partners = Partners(id_vk=vk_id, first_name=first_name, last_name=last_name, pages=vk_link, user_id=user_id)
    session.add(partners)
    session.commit()
    
    print(partners.id)
    session.close()

