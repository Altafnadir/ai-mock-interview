import logging
import sys
from app.core.config import settings

def setup_logging():
    log_format = "%(asctime)s - [%(levelname)s] - %(name)s - %(message)s"
    level = logging.DEBUG if settings.ENVIRONMENT == "development" else logging.INFO
    
    logging.basicConfig(
        level=level,
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Silence overly verbose external loggers
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

logger = logging.getLogger("ai_mock_interview")
