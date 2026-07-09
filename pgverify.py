import psycopg2

print("--- Test 1: kavan_user with correct password ---")
try:
    conn = psycopg2.connect(dbname="kavan_db", user="kavan_user", password="kavan_secure_password", host="127.0.0.1", port=5432)
    cur = conn.cursor()
    cur.execute("SELECT current_user, current_database()")
    row = cur.fetchone()
    print(f"SUCCESS: connected as {row[0]} to {row[1]}")
    conn.close()
except Exception as e:
    print(f"FAIL: {e}")

print("\n--- Test 2: kavan_user with WRONG password (must fail) ---")
try:
    conn = psycopg2.connect(dbname="kavan_db", user="kavan_user", password="wrongpassword", host="127.0.0.1", port=5432)
    print("UNEXPECTED SUCCESS - auth is too permissive!")
    conn.close()
except Exception as e:
    print(f"Correctly rejected: {e}")
