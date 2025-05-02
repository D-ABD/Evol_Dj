import os
from dotenv import load_dotenv

load_dotenv()

required_env_vars = [
    'DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT',
    'SECRET_KEY', 'DEBUG', 'ALLOWED_HOSTS', 'CORS_ALLOW_ALL_ORIGINS',
    'REDIS_URL', 'EMAIL_HOST', 'EMAIL_PORT', 'EMAIL_USE_TLS',
    'EMAIL_HOST_USER', 'EMAIL_HOST_PASSWORD', 'DEFAULT_FROM_EMAIL',
    'JWT_ACCESS_TOKEN_LIFETIME_MINUTES', 'JWT_REFRESH_TOKEN_LIFETIME_DAYS',
    'DEFAULT_ADMIN_EMAIL'
]

missing_vars = []

for var in required_env_vars:
    if os.getenv(var) is None:
        missing_vars.append(var)

if missing_vars:
    print("❌ Les variables suivantes sont manquantes dans votre fichier .env :")
    for var in missing_vars:
        print(f" - {var}")
else:
    print("✅ Toutes les variables d'environnement requises sont présentes.")
