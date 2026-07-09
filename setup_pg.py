import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

try:
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="postgres", host="localhost", port=5432)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    print("Connected as postgres user.")
    cur = conn.cursor()
    
    # Create user if not exists
    cur.execute("SELECT 1 FROM pg_roles WHERE rolname='kavan_user'")
    if not cur.fetchone():
        print("Creating user kavan_user...")
        cur.execute("CREATE USER kavan_user WITH PASSWORD 'kavan_secure_password'")
    else:
        print("User kavan_user already exists, updating password.")
        cur.execute("ALTER USER kavan_user WITH PASSWORD 'kavan_secure_password'")
        
    # Create DB if not exists
    cur.execute("SELECT 1 FROM pg_database WHERE datname='kavan_db'")
    if not cur.fetchone():
        print("Creating database kavan_db...")
        cur.execute("CREATE DATABASE kavan_db")
        
    cur.execute("GRANT ALL PRIVILEGES ON DATABASE kavan_db TO kavan_user")
    cur.execute("ALTER DATABASE kavan_db OWNER TO kavan_user")
    print("Postgres setup complete!")
    conn.close()
except Exception as e:
    print(f"Failed: {e}")
