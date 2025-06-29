from fastapi import FastAPI, HTTPException, Request, status, Query
from pydantic import BaseModel
from typing import Optional, List
import asyncpg
import os
import time

app = FastAPI()

# Pydantic models
class Peca(BaseModel):
    id: int
    nome: str
    descricao: str
    preco: float
    quantidade: int

class PecaCreate(BaseModel):
    nome: str
    descricao: str
    preco: float
    quantidade: int


class PecaUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    preco: Optional[float] = None
    quantidade: Optional[int] = None


class Servico(BaseModel):
    id: int
    nome: str
    descricao: Optional[str] = None
    preco: float
    duracao: Optional[int] = None

class ServicoCreate(BaseModel):
    nome: str
    descricao: Optional[str] = None
    preco: float
    duracao: Optional[int] = None

class ServicoUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    preco: Optional[float] = None
    duracao: Optional[int] = None

# Database connection helper
def get_database_url() -> str:
    return os.getenv(
        "PGURL",
        "postgresql://postgres:postgres@db:5432/motos"
    )

async def get_database():
    return await asyncpg.connect(get_database_url())

# Request logging middleware\@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    print(f"{request.method} {request.url.path} - {duration:.4f}s")
    return response

# CRUD Pecas
@app.post("/api/v1/pecas/", status_code=status.HTTP_201_CREATED, response_model=Peca)
async def criar_peca(peca: PecaCreate):
    conn = await get_database()
    try:
        row = await conn.fetchrow(
            """
            INSERT INTO pecas (nome, descricao, preco, quantidade)
            VALUES ($1, $2, $3, $4)
            RETURNING *
            """,
            peca.nome, peca.descricao, peca.preco, peca.quantidade
        )
        return dict(row)
    finally:
        await conn.close()

@app.get("/api/v1/pecas/", response_model=List[Peca])
async def listar_pecas():
    conn = await get_database()
    try:
        rows = await conn.fetch("SELECT * FROM pecas ORDER BY id")
        return [dict(r) for r in rows]
    finally:
        await conn.close()

@app.get("/api/v1/pecas/{id}", response_model=Peca)
async def obter_peca(id: int):
    conn = await get_database()
    try:
        row = await conn.fetchrow("SELECT * FROM pecas WHERE id = $1", id)
        if not row:
            raise HTTPException(status_code=404, detail="Peça não encontrada")
        return dict(row)
    finally:
        await conn.close()

@app.patch("/api/v1/servicos/{servico_id}")
async def atualizar_servico(servico_id: int, servico: ServicoUpdate):
    conn = await get_database()
    try:
        campos = []
        valores = []

        if servico.nome is not None:
            campos.append("nome = $" + str(len(valores) + 1))
            valores.append(servico.nome)
        if servico.descricao is not None:
            campos.append("descricao = $" + str(len(valores) + 1))
            valores.append(servico.descricao)
        if servico.preco is not None:
            campos.append("preco = $" + str(len(valores) + 1))
            valores.append(servico.preco)
        if servico.duracao is not None:
            campos.append("duracao = $" + str(len(valores) + 1))
            valores.append(servico.duracao)

        if not campos:
            raise HTTPException(status_code=400, detail="Nenhum campo para atualizar")

        query = f"UPDATE servicos SET {', '.join(campos)} WHERE id = ${len(valores)+1}"
        valores.append(servico_id)
        await conn.execute(query, *valores)
        return {"mensagem": "Serviço atualizado com sucesso"}
    finally:
        await conn.close()

@app.delete("/api/v1/pecas/{id}", status_code=status.HTTP_200_OK)
async def remover_peca(id: int):
    conn = await get_database()
    try:
        result = await conn.execute("DELETE FROM pecas WHERE id = $1", id)
        if result == "DELETE 0":
            raise HTTPException(status_code=404, detail="Peça não encontrada")
        return {"message": "Peça removida"}
    finally:
        await conn.close()

# CRUD Servicos
@app.post("/api/v1/servicos/", status_code=status.HTTP_201_CREATED, response_model=Servico)
async def criar_servico(servico: ServicoCreate):
    conn = await get_database()
    try:
        row = await conn.fetchrow(
            """
            INSERT INTO servicos (nome, descricao, preco, duracao)
            VALUES ($1, $2, $3, $4)
            RETURNING *
            """,
            servico.nome, servico.descricao, servico.preco, servico.duracao
        )
        return dict(row)
    finally:
        await conn.close()

@app.get("/api/v1/servicos/", response_model=List[Servico])
async def listar_servicos():
    conn = await get_database()
    try:
        rows = await conn.fetch("SELECT * FROM servicos ORDER BY id")
        return [dict(r) for r in rows]
    finally:
        await conn.close()

@app.get("/api/v1/servicos/{id}", response_model=Servico)
async def obter_servico(id: int):
    conn = await get_database()
    try:
        row = await conn.fetchrow("SELECT * FROM servicos WHERE id = $1", id)
        if not row:
            raise HTTPException(status_code=404, detail="Serviço não encontrado")
        return dict(row)
    finally:
        await conn.close()

@app.patch("/api/v1/pecas/{id}", response_model=Peca)
async def atualizar_peca(id: int, dados: PecaUpdate):
    conn = await get_database()
    try:
        atual = await conn.fetchrow("SELECT * FROM pecas WHERE id = $1", id)
        if not atual:
            raise HTTPException(status_code=404, detail="Peça não encontrada")
        atualizado = await conn.fetchrow(
            """
            UPDATE pecas
            SET nome = COALESCE($1, nome),
                descricao = COALESCE($2, descricao),
                preco = COALESCE($3, preco),
                quantidade = COALESCE($4, quantidade)
            WHERE id = $5
            RETURNING *
            """,
            dados.nome, dados.descricao, dados.preco, dados.quantidade, id
        )
        return dict(atualizado)
    finally:
        await conn.close()


@app.delete("/api/v1/servicos/{id}", status_code=status.HTTP_200_OK)
async def remover_servico(id: int):
    conn = await get_database()
    try:
        result = await conn.execute("DELETE FROM servicos WHERE id = $1", id)
        if result == "DELETE 0":
            raise HTTPException(status_code=404, detail="Serviço não encontrado")
        return {"message": "Serviço removido"}
    finally:
        await conn.close()

@app.post("/api/v1/pecas/{pid}/entrada")
async def entrada_peca(pid: int, quantidade: int = Query(..., gt=0)):
    conn = await get_database()
    try:
        row = await conn.fetchrow("SELECT quantidade FROM pecas WHERE id = $1", pid)
        if not row:
            raise HTTPException(status_code=404, detail="Peça não encontrada")

        nova_qtd = row["quantidade"] + quantidade
        await conn.execute("UPDATE pecas SET quantidade = $1 WHERE id = $2", nova_qtd, pid)
        return {"mensagem": f"Entrada registrada. Nova quantidade: {nova_qtd}"}
    finally:
        await conn.close()

@app.post("/api/v1/pecas/{pid}/saida")
async def saida_peca(pid: int, quantidade: int = Query(..., gt=0)):
    conn = await get_database()
    try:
        row = await conn.fetchrow("SELECT quantidade FROM pecas WHERE id = $1", pid)
        if not row:
            raise HTTPException(status_code=404, detail="Peça não encontrada")

        if row["quantidade"] < quantidade:
            raise HTTPException(status_code=400, detail="Quantidade insuficiente em estoque")

        nova_qtd = row["quantidade"] - quantidade
        await conn.execute("UPDATE pecas SET quantidade = $1 WHERE id = $2", nova_qtd, pid)
        return {"mensagem": f"Saída registrada. Nova quantidade: {nova_qtd}"}
    finally:
        await conn.close()