from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)


# Tentar conectar ao Azure SQL, usar SQLite como fallback
def get_database_config():
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_SERVER = os.getenv('DB_SERVER')
    DB_NAME = os.getenv('DB_NAME')
    DB_DRIVER = os.getenv('DB_DRIVER', 'ODBC Driver 17 for SQL Server')
    
    # Se as variáveis de ambiente estão configuradas, tentar usar Azure SQL
    if DB_USER and DB_PASSWORD and DB_SERVER:
        try:
            driver_formatted = DB_DRIVER.replace(' ', '+')
            DB_URL = f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}?driver={driver_formatted}&Timeout=5"
            engine = create_engine(DB_URL, echo=False, pool_pre_ping=True)
            # Testar conexão
            with engine.connect() as conn:
                pass
            print(f"✓ Conectado ao Azure SQL: {DB_SERVER}")
            return engine, "Azure SQL"
        except Exception as e:
            print(f"⚠ Azure SQL indisponível: {str(e)[:50]}...")
    
    # Usar SQLite como fallback
    print("ℹ Usando SQLite em desenvolvimento local")
    DB_URL_FALLBACK = "sqlite:///./test.db"
    engine = create_engine(
        DB_URL_FALLBACK,
        connect_args={"check_same_thread": False},
        echo=False
    )
    return engine, "SQLite"


# Inicializar banco de dados
try:
    engine, db_type = get_database_config()
    SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
    
    # Criar tabelas
    Base.metadata.create_all(bind=engine)
    print(f"✓ Tabelas criadas no {db_type}")
except Exception as e:
    print(f"❌ Erro fatal ao inicializar banco de dados: {e}")
    # Criar um engine SQLite mínimo para não quebrar a importação
    engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
