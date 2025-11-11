
from fastapi.testclient import TestClient
from app.main import app
import pytest
c = TestClient(app)
def test_home_and_health():
    assert c.get("/").status_code == 200
    assert c.get("/health").json()["status"] == "ok"
@pytest.mark.parametrize("a,b,op,exp",[(2,3,"add",5.0),(7,2,"sub",5.0),(3,4,"mul",12.0),(9,3,"div",3.0)])
def test_calc(a,b,op,exp):
    r = c.post("/api/calc", json={"a":a,"b":b,"op":op})
    assert r.status_code == 200 and r.json()["result"] == exp
def test_calc_div_zero():
    r = c.post("/api/calc", json={"a":1,"b":0,"op":"div"})
    assert r.status_code == 400 and "Division by zero" in r.json()["detail"]
