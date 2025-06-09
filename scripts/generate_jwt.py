import jwt
import argparse
import datetime
import os
import sys

# Load secret from env or default
SECRET = os.environ.get("JWT_SECRET", "secret-key")

def generate_token(role: str, user_id: int, expire_minutes: int = 60):
    now = datetime.datetime.utcnow()
    payload = {
        "role": role,
        "user_id": user_id,
        "iat": now,
        "exp": now + datetime.timedelta(minutes=expire_minutes),
    }

    token = jwt.encode(payload, SECRET, algorithm="HS256")
    return token


def main():
    parser = argparse.ArgumentParser(description="Generate JWT for PostgREST")
    parser.add_argument("--role", required=True, help="PostgreSQL role (e.g. web_anon)")
    parser.add_argument("--user-id", type=int, required=True, help="User ID")
    parser.add_argument("--expire", type=int, default=60, help="Token expiry in minutes")
    args = parser.parse_args()

    try:
        token = generate_token(args.role, args.user_id, args.expire)
        print(token)
    except Exception as e:
        print(f"Error generating token: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

