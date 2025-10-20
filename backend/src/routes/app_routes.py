from fastapi import APIRouter
from . import auth, user, words, definitions, examples, translations, tags, synonyms, warnings

router = APIRouter()

router.include_router(auth.router)
router.include_router(user.router)
router.include_router(words.router)
router.include_router(definitions.router)
router.include_router(examples.router)
router.include_router(translations.router)
router.include_router(tags.router)
router.include_router(synonyms.router)
router.include_router(warnings.router)



