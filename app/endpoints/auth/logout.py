from fastapi import APIRouter


router = APIRouter(tags=["Auth"], prefix="/logout")


@router.post("")
async def logout():
    return {"msg": "hello"}
