from config.database import Database 

def get_db():
    return Database.get_instance().get_db
