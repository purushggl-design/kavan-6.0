import psycopg2
import redis

print("--- Postgres (127.0.0.1) ---")
try:
    conn = psycopg2.connect(dbname="kavan_db", user="kavan_user", password="kavan_secure_password", host="127.0.0.1", port=5432, connect_timeout=3)
    print("Postgres SUCCESS")
    conn.close()
except Exception as e:
    print(f"Postgres FAIL: {e}")

print("--- Redis (127.0.0.1) ---")
try:
    r = redis.Redis(host='127.0.0.1', port=6379, socket_connect_timeout=3)
    if r.ping():
        print("Redis SUCCESS")
except Exception as e:
    print(f"Redis FAIL: {e}")
