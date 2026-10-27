from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from auth.application.register_user import RegisterUserCommand, RegisterUser
from auth.domain.errors import EmailAlreadyRegistered, InvalidEmail, WeakPassword


class RegisterRequest(BaseModel):
    email: str
    password: str


def build_auth_router(register_user: RegisterUser) -> APIRouter:
    router = APIRouter(prefix="/auth", tags=["auth"])

    @router.post("/register", status_code=201)
    def register(body: RegisterRequest) -> dict[str, str]:
        try:
            user_id = register_user.execute(
                RegisterUserCommand(email=body.email, password=body.password)
            )
        except InvalidEmail:
            raise HTTPException(status_code=422, detail="Email inválido")
        except WeakPassword:
            raise HTTPException(status_code=422, detail="La contraseña debe tener entre 8 y 72 caracteres")
        except EmailAlreadyRegistered:
            raise HTTPException(status_code=409, detail="El email ya está registrado")
        return {"id": str(user_id)}

    return router
