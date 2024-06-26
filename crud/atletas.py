from sqlalchemy.orm import Session
from ..models import Atleta
from ..schemas import AtletaCreate

def create_atleta(db: Session, atleta: AtletaCreate):
    db_atleta = Atleta(
        nome=atleta.nome,
        cpf=atleta.cpf,
        centro_treinamento=atleta.centro_treinamento,
        categoria=atleta.categoria
    )
    db.add(db_atleta)
    db.commit()
    db.refresh(db_atleta)
    return db_atleta

def get_atletas(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Atleta).offset(skip).limit(limit).all()

def get_atleta_by_cpf(db: Session, cpf: str):
    return db.query(Atleta).filter(Atleta.cpf == cpf).first()
