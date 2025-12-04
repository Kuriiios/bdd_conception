from sqlalchemy import Column, Integer, String, Boolean, Date, LargeBinary, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Platform(Base):
    __tablename__='platforms'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)

    game_version = relationship('GameVersion', back_populates= 'platform')


class Rank(Base):
    __tablename__='ranks'

    id = Column(Integer, primary_key=True)
    ranking = Column(Integer, nullable=False, unique=True)

    game_version = relationship('GameVersion', back_populates= 'rank')

class Year(Base):
    __tablename__ = 'years'

    id = Column(Integer, primary_key=True)
    year_date = Column(Integer, nullable=False, unique=True)

    game_version = relationship('GameVersion', back_populates='year')

class Publisher(Base):
    __tablename__ = 'publishers'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)

    game_version = relationship('GameVersion', back_populates='publisher')

class Genre(Base):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)

    game_version = relationship('GameVersion', back_populates='genre')

class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False, unique=True)

    game_version = relationship('GameVersion', back_populates='game')

class GameVersion(Base):
    __tablename__ = 'game_versions'

    id = Column(Integer, primary_key=True)

    platform_id = Column(Integer, ForeignKey('platforms.id'), nullable=False)
    platform = relationship('Platform', back_populates= 'game_version')

    rank_id = Column(Integer, ForeignKey('ranks.id'), nullable=False)
    rank = relationship('Rank', back_populates= 'game_version')

    year_id = Column(Integer, ForeignKey('years.id'))
    year = relationship('Year', back_populates='game_version')

    publisher_id = Column(Integer, ForeignKey('publishers.id'))
    publisher = relationship ('Publisher', back_populates='game_version')

    game_id = Column(Integer, ForeignKey('games.id'), nullable=False)
    game = relationship('Game', back_populates='game_version')

    genre_id = Column(Integer, ForeignKey('genres.id'))
    genre = relationship('Genre', back_populates='game_version')

    sale = relationship('Sale', back_populates='game_version')

    transaction = relationship('Transaction', back_populates='game_version')

class Sale(Base):
    __tablename__ = 'sales'

    id = Column (Integer, primary_key=True)
    na_sales = Column(Integer)
    eu_sales = Column(Integer)
    jp_sales = Column(Integer)
    other_sales = Column(Integer)

    game_version_id = Column(Integer, ForeignKey('game_versions.id'), nullable=False)
    game_version = relationship('GameVersion', back_populates='sale')

class Region(Base):
    __tablename__ = 'regions'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False, unique=True)

    country = relationship('Country', back_populates='region') 

class Country(Base):
    __tablename__ = 'countries'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)

    region_id = Column(Integer, ForeignKey('regions.id'), nullable=False)
    region = relationship('Region', back_populates='country')

    city = relationship('City', back_populates='country')

class City(Base):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)

    country_id = Column(Integer, ForeignKey('countries.id'), nullable=False)
    country = relationship('Country', back_populates='city')

    post_code = relationship('PostCode', back_populates='city')

class PostCode(Base):
    __tablename__ = 'post_codes'

    id = Column(Integer, primary_key=True)
    code = Column(String(10), nullable=False, unique=True)

    city_id = Column(Integer, ForeignKey('cities.id'), nullable=False)
    city = relationship('City', back_populates='post_code')

    user = relationship('User', back_populates='post_code')

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(LargeBinary, nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    phone_number = Column(LargeBinary, nullable=False, unique=True)
    address = Column(LargeBinary, nullable=False)
    keep_info = Column(Boolean, nullable=False)
    deleted_in = Column(Date)

    post_code_id = Column(Integer, ForeignKey('post_codes.id'), nullable=False)
    post_code = relationship('PostCode', back_populates='user')

    transaction = relationship('Transaction', back_populates='user')

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    quantity = Column (Integer, nullable=False)

    game_version_id = Column(Integer, ForeignKey('game_versions.id'), nullable=False)
    game_version = relationship('GameVersion', back_populates='transaction')

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='transaction')
