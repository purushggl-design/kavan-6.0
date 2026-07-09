import psycopg2

passwords = ["", "postgres", "admin", "root", "password", "kavan_secure_password", "kavan"]
users = ["postgres", "kavan_user", "purus"]

for u in users:
    for p in passwords:
        try:
            conn = psycopg2.connect(dbname="postgres", user=u, password=p, host="localhost", port=5432, connect_timeout=1)
            print(f"SUCCESS: user={u}, password={p}")
            conn.close()
            exit(0)
        except Exception as e:
            pass

print("FAILED ALL")
