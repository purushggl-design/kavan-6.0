import psycopg2
import redis
import sys

print("--- Checking Postgres ---")
try:
    conn = psycopg2.connect(dbname="kavan_db", user="kavan_user", password="kavan_secure_password", host="localhost", port=5432, connect_timeout=3)
    print("Postgres connection successful!")
    cur = conn.cursor()
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
    rows = cur.fetchall()
    print("Tables:", rows)
    conn.close()
except Exception as e:
    print(f"Postgres connection failed: {e}")

print("\n--- Checking Redis ---")
try:
    r = redis.Redis(host='localhost', port=6379, socket_connect_timeout=3)
    response = r.ping()
    if response:
        print("PONG (Redis connection successful!)")
    else:
        print("Redis returned False for ping.")
except Exception as e:
    print(f"Redis connection failed: {e}")
