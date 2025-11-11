
from app import security

class StubCtx:
    @staticmethod
    def hash(s: str) -> str:
        return f"stub::{s}"
    @staticmethod
    def verify(s: str, h: str) -> bool:
        return h == f"stub::{s}"

def test_security_hash_and_verify_both_paths(monkeypatch):
    monkeypatch.setattr(security, "pwd_context", StubCtx())
    h = security.hash_password("Secr3t!")
    assert h == "stub::Secr3t!"
    assert security.verify_password("Secr3t!", h) is True
    assert security.verify_password("wrong", h) is False
