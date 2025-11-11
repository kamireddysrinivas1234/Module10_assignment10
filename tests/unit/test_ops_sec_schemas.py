
import math, pytest
from app import operations as ops
from app.security import hash_password, verify_password
from pydantic import ValidationError
from app.schemas import CalcRequest, UserCreate

def test_operations_all():
    assert ops.add(2,3)==5
    assert ops.subtract(7,2)==5
    assert ops.multiply(3,4)==12
    assert ops.divide(9,3)==3
    with pytest.raises(ZeroDivisionError): ops.divide(1,0)
    assert math.isclose(ops.divide(1,4),0.25,rel_tol=1e-9)

def test_security_true_and_false_paths():
    h = hash_password("S3cret!!")
    assert verify_password("S3cret!!", h) is True
    assert verify_password("wrong", h) is False

def test_schemas_validator_and_valid():
    _ = UserCreate(username="alice", email="alice@example.com", password="pass123")
    with pytest.raises(ValidationError):
        CalcRequest(a=1,b=2,op="pow")
