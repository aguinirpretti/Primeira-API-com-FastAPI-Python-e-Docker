from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..database import SessionLocal
from fastapi_pagination import Page, pagination_params

router = APIRouter()

@router.get("/atletas", response_model=List[schemas.Atleta])
def read_atletas(skip: int = 0, limit: int = 10, db: Session = Depends(SessionLocal)):
    atletas = crud.get_atletas(db, skip=skip, limit=limit)
    return atletas

@router.get("/atletas/{cpf}", response_model=schemas.Atleta)
def read_atleta(cpf: str, db: Session = Depends(SessionLocal)):
    atleta = crud.get_atleta_by_cpf(db, cpf=cpf)
    if atleta is None:
        raise HTTPException(status_code=404, detail="Atleta not found")
    return atleta

@router.post("/atletas", response_model=schemas.Atleta)
def create_atleta(atleta: schemas.AtletaCreate, db: Session = Depends(SessionLocal)):
    db_atleta = crud.get_atleta_by_cpf(db, cpf=atleta.cpf)
    if db_atleta:
        raise HTTPException(status_code=303, detail=f"Já existe um atleta cadastrado com o cpf: {atleta.cpf}")
    return crud.create_atleta(db=db, atleta=atleta)

@router.get("/atletas/filter")
def read_atletas_filtered(
    nome: str = Query(None),
    cpf: str = Query(None),
    db: Session = Depends(SessionLocal)
):
    query = db.query(models.Atleta)
    if nome:
        query = query.filter(models.Atleta.nome == nome)
    if cpf:
        query = query.filter(models.Atleta.cpf == cpf)
    atletas = query.all()
    return atletas

@router.get("/atletas/paginated", response_model=Page[schemas.Atleta])
def read_atletas_paginated(
    db: Session = Depends(SessionLocal),
    pagination: dict = Depends(pagination_params)
):
    skip = pagination.get("skip", 0)
    limit = pagination.get("limit", 10)
    atletas = crud.get_atletas(db, skip=skip, limit=limit)
    return Page(atletas, skip=skip, limit=limit)
