from .environ import env

DATABASES = {"default": env.db("DATABASE_URL", default="")}
