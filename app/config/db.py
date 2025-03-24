from app.config.settings import Settings


class DBConfig(Settings):
    database_url: str = "driver://user:pass@localhost/dbname"


db_config = DBConfig()
