import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Connect WITHOUT password under trust auth (pg_hba.conf already set to trust)
try:
    conn = psycopg2.connect(dbname="postgres", user="postgres", host="127.0.0.1", port=5432)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    print("Connected as postgres (no password)")

    # Check/create user
    cur.execute("SELECT 1 FROM pg_roles WHERE rolname='kavan_user'")
    if cur.fetchone():
        print("User kavan_user exists - resetting password")
        cur.execute("ALTER USER kavan_user WITH PASSWORD 'kavan_secure_password'")
    else:
        print("Creating user kavan_user")
        cur.execute("CREATE USER kavan_user WITH PASSWORD 'kavan_secure_password'")

    # Check/create database
    cur.execute("SELECT 1 FROM pg_database WHERE datname='kavan_db'")
    if cur.fetchone():
        print("Database kavan_db exists")
    else:
        print("Creating database kavan_db")
        cur.execute("CREATE DATABASE kavan_db OWNER kavan_user")

    cur.execute("GRANT ALL PRIVILEGES ON DATABASE kavan_db TO kavan_user")
    print("Grants applied")
    conn.close()
    print("SUCCESS")
except Exception as e:
    print(f"FAIL: {e}")
