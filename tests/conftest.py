
import pytest
from app import security

class StubCtx:
    @staticmethod
    def hash(s: str) -> str:
        return f"stub::{s}"
    @staticmethod
    def verify(s: str, h: str) -> bool:
        return h == f"stub::{s}"

@pytest.fixture(autouse=True)
def stub_hasher(monkeypatch):
    # Stub both high-level and context to be safe
    monkeypatch.setattr(security, "pwd_context", StubCtx())
    monkeypatch.setattr(security, "hash_password", lambda s: StubCtx.hash(s))
    yield
