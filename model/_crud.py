from sqlalchemy.sql.expression import insert, delete, select, func
from model._cryption import *
from model.database.models import *
from model._dates import *
from IPython.display import clear_output
import hashlib

def insert_or_get_id(session, class_, column_names: list[str], values: list):

    conflict_column = column_names[0] 
    conflict_value = values[0]
    try:
        column_attribute = getattr(class_, conflict_column) 
        print(column_attribute)
        foreign_object = session.query(class_.id).filter_by(column_attribute==conflict_value).first()
        return foreign_object.id
    except:
        session.rollback()
        column_attribute = getattr(class_, conflict_column) 
        print(column_attribute)
        foreign_object = session.add(class_(conflict_column=conflict_value))
        session.commit()
        foreign_object = session.query(class_.id).filter_by(conflict_column==conflict_value).first()
        return foreign_object.id

def add_user(session, name, email, phone_number, address, post_code, city, country, region_name, keep_info=False):
    session.rollback()
    encrypted_name = encrypt(name)
    encrypted_email = hashlib.sha256(email.encode()).hexdigest()
    encrypted_phone_number = encrypt(phone_number)
    encrypted_address = encrypt(address)
    deleted_in = d_plus_five_y if keep_info == True else d_plus_two_w


    try:
        region_object = session.execute(select(Region).where(Region.name == region_name)).scalar_one()
    except:
        session.rollback()
        session.add(Region(name=region_name))
        session.commit()
        region_object = session.execute(select(Region).where(Region.name == region_name)).scalar_one()

    try:
        country_object = session.execute(select(Country).where(Country.name == country, Country.region_id == region_object.id)).scalar_one()
    except:
        session.rollback()
        session.add(Country(name=country, region_id = region_object.id))
        session.commit()
        country_object = session.execute(select(Country).where(Country.name == country, Country.region_id == region_object.id)).scalar_one()

    try:
        city_object = session.execute(select(City).where(City.name == city, City.country == country_object)).scalar_one()
    except:
        session.rollback()
        session.add(City(name=city, country=country_object))
        session.commit()
        city_object = session.execute(select(City).where(City.name == city, City.country == country_object)).scalar_one()

    try:
        post_code_object = session.execute(select(PostCode).where(PostCode.code == post_code, PostCode.city == city_object)).scalar_one()
    except:
        session.rollback()
        session.add(PostCode(code=post_code, city=city_object))
        session.commit()
        post_code_object = session.execute(select(PostCode).where(PostCode.code == post_code, PostCode.city == city_object)).scalar_one()

    new_user = User(name = encrypted_name, email=encrypted_email, phone_number=encrypted_phone_number, address=encrypted_address, keep_info=keep_info, deleted_in=deleted_in, post_code = post_code_object)
    session.rollback()
    session.add(new_user)
    session.commit()
    clear_output()

def add_game_version(session, platform, year, publisher, game, genre):
    session.rollback()

    try:
        platform_object = session.execute(select(Platform).where(Platform.name == platform)).scalar_one()
    except:
        session.rollback()
        session.add(Platform(name=platform))
        session.commit()
        platform_object = session.execute(select(Platform).where(Platform.name == platform)).scalar_one()

    try:
        rank_object = session.execute(select(Rank).where(Rank.ranking == rank)).scalar_one()
    except:
        session.rollback()
        rank = session.query(func.max(Rank.ranking)).first()[0] + 1
        session.add(Rank(ranking = rank))
        session.commit()
        rank_object = session.execute(select(Rank).where(Rank.ranking == rank)).scalar_one()

    try:
        year_object = session.execute(select(Year).where(Year.year_date == year)).scalar_one()
    except:
        session.rollback()
        session.add(Year(year_date=year))
        session.commit()
        year_object = session.execute(select(Year).where(Year.year_date == year)).scalar_one()

    try:
        publisher_object = session.execute(select(Publisher).where(Publisher.name == publisher)).scalar_one()
    except:
        session.rollback()
        session.add(Publisher(name=publisher))
        session.commit()
        publisher_object = session.execute(select(Publisher).where(Publisher.name == publisher)).scalar_one()

    try:
        game_object = session.execute(select(Game).where(Game.name == game)).scalar_one()
    except:
        session.rollback()
        session.add(Game(name=game))
        session.commit()
        game_object = session.execute(select(Game).where(Game.name == game)).scalar_one()

    try:
        genre_object = session.execute(select(Genre).where(Genre.name == genre)).scalar_one()
    except:
        session.rollback()
        session.add(Genre(name=genre))
        session.commit()
        genre_object = session.execute(select(Genre).where(Genre.name == genre)).scalar_one()

    new_game = GameVersion(platform = platform_object, rank=rank_object, year=year_object, publisher=publisher_object, game=game_object, genre=genre_object)
    session.rollback()
    session.add(new_game)
    session.commit()
    clear_output()

def retrive_user_with_mail(session, mail):
    session.rollback()
    encrypted_email = hashlib.sha256(mail.encode()).hexdigest()
    stmt = select(User).where(User.email == encrypted_email)
    user = session.execute(stmt).scalar_one_or_none()
    user_info = {'Name':decrypt(user.name).decode(),
                 'Email':mail,
                 'Phone number': decrypt(user.phone_number).decode(),
                 'Address': decrypt(user.address).decode(),
                 'Post Code': user.post_code.code,
                 'City': user.post_code.city.name,
                 'Country': user.post_code.city.country.name,
                 'Region': user.post_code.city.country.region.name}
    clear_output()
    return user_info

def retrive_game(session, game_name):
    session.rollback()
    stmt = select(GameVersion).join(GameVersion.game).where(Game.name == game_name)
    game = session.execute(stmt).scalar_one_or_none()
    game_info = {'Name':game.game.name, 'Platform':game.platform.name, 'Year':game.year.year_date, 'Publisher':game.publisher.name, 'Genre': game.genre.name}
    clear_output()
    return game_info