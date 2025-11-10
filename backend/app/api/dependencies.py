"""FastAPI dependencies for dependency injection."""
from typing import Annotated

from fastapi import Depends

from app.config import Settings, get_settings

# Settings dependency
SettingsDep = Annotated[Settings, Depends(get_settings)]
