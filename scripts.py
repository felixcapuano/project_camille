import uvicorn
import sqlite3

def dev():
    uvicorn.run("project_camille.app:app", reload=True)
    
def make_db():
    con = sqlite3.connect("project_camille/main.db")
    cur = con.cursor()

    cur.execute("CREATE TABLE users(username, password)")
    cur.execute("INSERT INTO users VALUES ('vilain', 'qdsjflkqsdjfkl')")

    con.commit()
    result = cur.execute("SELECT * FROM users")
    print(result.fetchall())
