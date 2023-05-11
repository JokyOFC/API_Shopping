# -*- coding: utf-8 -*-
"""
Created on Mon May  8 18:14:51 2023

@author: Everton Castro
"""
from fastapi import APIRouter, HTTPException, status
from src.schemas.schema import User, Login, UserResponse
from src.connection.conexao import get_database_connection   
from src.security import hash_provider, token_provider


router = APIRouter()

@router.post('/signup', status_code=status.HTTP_201_CREATED)
async def signup(users: User):
    try:
        conn = await get_database_connection()

        query_exist_user = "SELECT email FROM users WHERE email = $1"
        usuario_localizado = await conn.fetchrow(query_exist_user, users.email)
        if usuario_localizado is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Já existe um usuário com esse email')
            
        users.password = hash_provider.getPasswordHash(users.password)
        query = "INSERT INTO users (username, email, password, empresa_empresa_fk ) SELECT $1, $2, $3, $4 FROM Empresa WHERE empresa_id = $5 RETURNING user_id"
        result_user_id = await conn.fetchval(query, users.name, users.email, users.password, users.empresa_fk, users.empresa_fk)

        query_user_response = "SELECT user_id , username , email FROM users WHERE user_id = $1"
        user_response = await conn.fetchrow(query_user_response, result_user_id)

        return UserResponse(**user_response)
    
    finally:
        await conn.close()

@router.post("/login")
async def Login(login: Login):
    """user = UserAuth(session).validatorLogin(login)

    if not user or not hash_provider.verifyPassword(login.password,user.password):#hash password
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail='Email ou Senha incorreta')

    token = token_provider.createAcessToken({'sub': login.email})
    return {'email': login.email, 'token': token}"""
    ...