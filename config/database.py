from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from sqlalchemy.ext.declarative import declarative_base

# Carga las variables de entorno desde .env
load_dotenv()

# Obtiene la URL de la base de datos desde las variables de entorno, sin el parámetro ssl-mode
DATABASE_URL = os.getenv("DATABASE_URL").replace('?ssl-mode=REQUIRED', '')

# Configura el modo SSL en la conexión
ssl_args = {
    "ssl": {
        "ssl": "true"  # Ruta al certificado CA si es necesario, puede omitirse si no lo tienes
    }
}

Base = declarative_base()

class Database:
    __instance = None

    def __init__(self):
        if Database.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            try:
                # Crea la conexión con la base de datos con argumentos SSL
                self.engine = create_engine(DATABASE_URL, connect_args=ssl_args)
                # Verifica la conexión
                self.test_connection()
                # Crea el SessionLocal
                self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
                Database.__instance = self
            except SQLAlchemyError as e:
                raise ConnectionError(f"Error connecting to the database: {str(e)}")

    @staticmethod
    def get_instance():
        if Database.__instance is None:
            Database()
        return Database.__instance

    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def test_connection(self):
        """Prueba la conexión a la base de datos."""
        try:
            with self.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            print("Database connection successful!")
        except SQLAlchemyError as e:
            raise ConnectionError(f"Failed to connect to the database: {str(e)}")


# Ejemplo de uso
if __name__ == "__main__":
    try:
        db_instance = Database.get_instance()  # Esto también validará la conexión
    except Exception as e:
        print(f"An error occurred: {str(e)}")
