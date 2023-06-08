from fastapi import FastAPI, UploadFile, Depends
from fastapi_users_db_sqlalchemy import UUID_ID
from fastapi.responses import FileResponse
from src.auth.base_config import fastapi_users, auth_backend
from src.auth.schemes import UserRead, UserCreate
import uvicorn
from src.database import get_async_session, AsyncSession
from src.auth.models import Mp3FIle, User
from src.auth.base_config import current_user
from fastapi.exceptions import HTTPException
import os

app = FastAPI()

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile, UUID: UUID_ID, session: AsyncSession = Depends(get_async_session),
                             user: User = Depends(current_user)):
    if file.content_type != 'audio/wave':
        raise HTTPException(status_code=400, detail='invalid format')
    if user.id != UUID:
        raise HTTPException(status_code=400, detail='invalid UUID')

    attach = Mp3FIle(
        content=file,
        user_id=user.id,
                     )
    session.add(attach)
    await session.commit()
    os.chdir('/tmp/storage/attachment')
    name_wav = attach.content['file_id']
    os.rename(name_wav, f'{name_wav}.mp3')
    return {"url": f"http://0.0.0.0:8000/record?id={attach.id}&user={UUID}"}


@app.get("/record")
async def get_audiofile(id: UUID_ID, user: UUID_ID, session: AsyncSession = Depends(get_async_session)):
    result = await session.get(Mp3FIle, id)
    if user != result.user_id:
        raise HTTPException(status_code=400, detail="invalid user_UUID")
    return FileResponse(
        path=f'{result.content["url"]}.mp3',
        media_type='multipart/form-data',
        headers={"content-disposition": f'attachment; filename="{result.content["file_id"] + ".mp3"}"', "content-type": "multipart/form-data"},
    )








if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.0", port=8000)
