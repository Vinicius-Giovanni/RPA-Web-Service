from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class AuthenticatedUser:
    id: str
    email: str
    full_name: str = ""