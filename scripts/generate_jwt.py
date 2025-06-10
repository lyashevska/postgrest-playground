import jwt
import datetime
import os
import sys

SECRET = os.environ.get("JWT_SECRET")
ROLE = os.environ.get("JWT_ROLE", "web_anon")
USER_ID = int(os.environ.get("JWT_USER_ID", "1"))
EXPIRE_MINUTES = int(os.environ.get("JWT_EXPIRE", "60"))

def generate_token(role: str, user_id: int, expire_minutes: int = 60):
    now = datetime.datetime.now(datetime.UTC)
    payload = {
        "role": role,
        "user_id": user_id,
        "iat": now,
        "exp": now + datetime.timedelta(minutes=expire_minutes),
    }
    token = jwt.encode(payload, SECRET, algorithm="HS256")
    return token

if __name__ == "__main__":
    try:
        token = generate_token(ROLE, USER_ID, EXPIRE_MINUTES)
        print(token)
    except Exception as e:
        print(f"Error generating token: {e}", file=sys.stderr)
        sys.exit(1)