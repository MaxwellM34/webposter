from .config import Config

# Pull ORM for aerich
TORTOISE_ORM = Config.TORTOISE_ORM
GOOGLE_AUDIENCE = Config.GOOGLE_AUDIENCE

# Now define usable exports
__all__ = ["Config", "TORTOISE_ORM", "GOOGLE_AUDIENCE"]
