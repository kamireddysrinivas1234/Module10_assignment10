
import os, importlib
os.environ["DATABASE_URL"] = "sqlite:///./test_cov.db"
import app.db as dbmod
importlib.reload(dbmod)
def test_db_sqlite_connect_args_and_finally():
    assert dbmod.engine is not None
    g = dbmod.get_db(); s = next(g); assert s is not None; g.close()
