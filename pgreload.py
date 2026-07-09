import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Still in trust mode - use this window to reload the config
try:
    conn = psycopg2.connect(dbname="postgres", user="postgres", host="127.0.0.1", port=5432)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute("SELECT pg_reload_conf()")
    result = cur.fetchone()
    print(f"pg_reload_conf() = {result[0]}")
    conn.close()
    print("Config reloaded - pg_hba.conf is now scram-sha-256 again")
except Exception as e:
    print(f"FAIL: {e}")
