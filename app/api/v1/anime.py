from fastapi import APIRouter, Depends, HTTPException, status, Request, UploadFile, File, Form
from sqlalchemy.orm import Session

from app import models, schemas
from app.utils.storage import save_image
from app.core.logging_config import logger
from app.core.security import get_api_key
from app.database.session import get_db

from datetime import datetime, timezone, timedelta

moscow_offset = timezone(timedelta(hours=3))
now_moscow = datetime.now(moscow_offset)

router = APIRouter(
    prefix="/anime",
    tags=["Anime"],
    # Защищаем все роуты внутри этого APIRouter — проверьте API_KEY в заголовке X-API-KEY
    dependencies=[Depends(get_api_key)]
)


@router.get("", response_model=list[schemas.anime.Anime])
async def get_animes(
        request: Request,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    logger.info(
        f"[GET /anime] Request from IP: {request.client.host}, Skip: {skip}, Limit: {limit}")
    try:
        anime_list = db.query(models.anime.Anime).offset(skip).limit(limit).all()
        logger.info(f"[GET /anime] Found {len(anime_list)} anime entries")
        return anime_list
    except Exception as e:
        logger.error(f"[GET /anime] Database error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{anime_id}", response_model=schemas.anime.Anime)
async def get_anime(
        request: Request,
        anime_id: int,
        db: Session = Depends(get_db)
):
    logger.info(
        f"[GET /anime/{{anime_id}}] Request for anime_id={anime_id} from IP: {request.client.host}")
    try:
        anime = db.query(models.anime.Anime).get(anime_id)
        if anime:
            logger.info(f"[GET /anime/{{anime_id}}] Found anime: {anime.title}")
            return anime
        else:
            logger.warning(f"[GET /anime/{{anime_id}}] Anime not found: {anime_id}")
            raise HTTPException(status_code=404, detail="Anime not found")
    except Exception as e:
        logger.error(f"[GET /anime/{{anime_id}}] Database error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("", response_model=schemas.anime.Anime,
             status_code=status.HTTP_201_CREATED)
async def create_anime(
        request: Request,
        title: str = Form(...),
        subtitle: str | None = Form(None),
        description: str = Form(...),
        video_url: str = Form(...),
        preview_image: UploadFile | None = File(None),
        preview_image_url: str | None = Form(None),
        db: Session = Depends(get_db)
):
    logger.info(f"[POST /anime] Create request from IP: {request.client.host}, Title: {title}")
    try:
        # decide where to get preview_image from: file > url > error
        saved_preview = None
        if preview_image is not None:
            content = await preview_image.read()
            saved_preview = await save_image(content, preview_image.filename or 'preview.jpg')
        elif preview_image_url:
            saved_preview = preview_image_url

        if not saved_preview:
            raise HTTPException(status_code=400, detail='preview_image (file or url) is required')

        db_anime = models.anime.Anime(
            title=title,
            subtitle=subtitle,
            description=description,
            preview_image=saved_preview,
            video_url=video_url,
            created_at=now_moscow,
            updated_at=now_moscow
        )
        db.add(db_anime)
        db.commit()
        db.refresh(db_anime)
        logger.info(f"[POST /anime] Successfully created anime: {db_anime.title} (ID: {db_anime.id})")
        return db_anime
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[POST /anime] Failed to create anime: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/{anime_id}", response_model=schemas.anime.Anime)
async def update_anime(
    request: Request,
    anime_id: int,
    title: str | None = Form(None),
    subtitle: str | None = Form(None),
    description: str | None = Form(None),
    video_url: str | None = Form(None),
    preview_image: UploadFile | None = File(None),
    preview_image_url: str | None = Form(None),
    db: Session = Depends(get_db)
):
    logger.info(
        f"[PUT /anime/{{anime_id}}] Update request for anime_id={anime_id} from IP: {request.client.host}")
    try:
        db_anime = db.query(models.anime.Anime).get(anime_id)
        if not db_anime:
            logger.warning(
                f"[PUT /anime/{{anime_id}}] Anime not found for update: {anime_id}")
            raise HTTPException(status_code=404, detail="Anime not found")

        # Сохраняем старое название для лога
        old_title = db_anime.title

        update_data: dict = {}
        if title is not None:
            update_data['title'] = title
        if subtitle is not None:
            update_data['subtitle'] = subtitle
        if description is not None:
            update_data['description'] = description
        if video_url is not None:
            update_data['video_url'] = video_url

        # handle preview image if provided
        if preview_image is not None:
            content = await preview_image.read()
            saved_preview = await save_image(content, preview_image.filename or 'preview.jpg')
            update_data['preview_image'] = saved_preview
        elif preview_image_url:
            update_data['preview_image'] = preview_image_url
        if 'title' in update_data:
            existing_anime = db.query(models.anime.Anime).filter(
                models.anime.Anime.title == update_data['title'],
                models.anime.Anime.id != anime_id
            ).first()
            if existing_anime is not None:
                logger.warning(
                    f"[PUT /anime/{anime_id}] Title '{update_data['title']}' already exists")
                raise HTTPException(
                    status_code=400,
                    detail="Anime with this title already exists"
                )

        for key, value in update_data.items():
            setattr(db_anime, key, value)

        db_anime.updated_at = now_moscow
        db.commit()
        db.refresh(db_anime)

        logger.info(
            f"[PUT /anime/{{anime_id}}] Successfully updated anime: '{old_title}' -> '{db_anime.title}'")
        return db_anime
    except Exception as e:
        logger.error(
            f"[PUT /anime/{{anime_id}}] Failed to update anime {anime_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/{anime_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_anime(
        request: Request,
        anime_id: int,
        db: Session = Depends(get_db),
):
    logger.info(
        f"[DELETE /anime/{{anime_id}}] Delete request for anime_id={anime_id} from IP: {request.client.host}")
    try:
        db_anime = db.query(models.Anime).get(anime_id)
        if not db_anime:
            logger.warning(
                f"[DELETE /anime/{{anime_id}}] Anime not found for deletion: {anime_id}")
            raise HTTPException(status_code=404, detail="Anime not found")

        # Сохраняем название для лога
        anime_title = db_anime.title

        db.delete(db_anime)
        db.commit()

        logger.info(
            f"[DELETE /anime/{{anime_id}}] Successfully deleted anime: '{anime_title}' (ID: {anime_id})")
        return {"message": "Anime deleted"}
    except Exception as e:
        logger.error(
            f"[DELETE /anime/{{anime_id}}] Failed to delete anime {anime_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
