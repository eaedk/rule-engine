from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Settings class to handle configuration via environment variables.

    Attributes:
        postgres_db (str): The name of the PostgreSQL database.
        postgres_user (str): The username for the PostgreSQL database.
        postgres_password (str): The password for the PostgreSQL database.
        database_url (str): The URL for the PostgreSQL database connection.

    Config:
        env_file (str): The file to load environment variables from.
    """

    postgres_db: str
    postgres_user: str
    postgres_password: str
    database_url: str

    class Config:
        """
        Pydantic configuration class.

        Attributes:
            env_file (str): The file to load environment variables from.
        """

        env_file = ".env"


settings = Settings()
