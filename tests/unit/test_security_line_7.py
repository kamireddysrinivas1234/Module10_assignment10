
from app.security import hash_password, verify_password
def test_security_verify_true_and_false_again():
    h = hash_password("Line7!!")
    assert verify_password("Line7!!", h) is True  # line 7 true path
    assert verify_password("nope", h) is False
