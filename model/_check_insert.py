from model.database.models import Platform, Rank, Year, Publisher, Genre, Game, GameVersion, Sale, Region, Country, City, PostCode, User, Transaction

class check_insert_data:
    def __init__(self, session):
        self.session = session

    def region(self, region_name):
        region_name_db = self.session.query(Region).filter_by(name = region_name).first()
        if not region_name_db:
            region_name_db = Region(name = region_name)
            self.session.add(region_name_db)
            self.session.flush()
        return region_name_db

    def country(self, region_name, country_name):
        region_name_db = self.region(region_name)
        country_name_db = self.session.query(Country).filter_by(name = country_name).first()
        if not country_name_db:
            country_name_db = Country(name = country_name, region = region_name_db)
            self.session.add(country_name_db)
            self.session.flush()
        return country_name_db


    def city(self, region_name, country_name, city_name):
        country_name_db = self.country(region_name, country_name)
        city_name_db = self.session.query(City).filter_by(name = city_name).first()
        if not city_name_db:
            city_name_db = City(name = city_name, country = country_name_db)
            self.session.add(city_name_db)
            self.session.flush()
        return city_name_db
    
    def post_code(self, region_name, country_name, city_name, post_code_value):
        city_name_db = self.city(region_name, country_name, city_name)
        post_code_db = self.session.query(PostCode).filter_by(code = post_code_value).first()
        if not post_code_db:
            post_code_db = PostCode(code = post_code_value, city = city_name_db)
            self.session.add(post_code_db)
            self.session.flush()
        return post_code_db
    
    def platform(self, value):
        platform = self.session.query(Platform).filter_by(name = value).first()
        if not platform:
            platform = Platform(name = value)
            self.session.add(platform)
            self.session.flush()
        return platform
    
    def rank(self, value):
        rank = self.session.query(Rank).filter_by(ranking = value).first()
        if not rank:
            rank = Rank(ranking = value)
            self.session.add(rank)
            self.session.flush()
        return rank
    
    def year(self, value):
        year = self.session.query(Year).filter_by(year_date = value).first()
        if not year:
            year = Year(year_date = value)
            self.session.add(year)
            self.session.flush()
        return year
    
    def publisher(self, value):
        publisher = self.session.query(Publisher).filter_by(name = value).first()
        if not publisher:
            publisher = Publisher(name = value)
            self.session.add(publisher)
            self.session.flush()
        return publisher
    
    def genre(self, value):
        genre = self.session.query(Genre).filter_by(name = value).first()
        if not genre:
            genre = Genre(name = value)
            self.session.add(genre)
            self.session.flush()
        return genre

    def game(self, value):
        game = self.session.query(Game).filter_by(name = value).first()
        if not game:
            game = Game(name = value)
            self.session.add(game)
            self.session.flush()
        return game