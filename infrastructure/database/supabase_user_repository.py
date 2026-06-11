from __future__ import annotations

from asyncio import to_thread

from domain.entities.user import AuthenticatedUser
from infrastructure.database.supabase_client import get_supabase_client

class SupabaseUserRepository:
    async def create_user_profile(self, user_id: str, full_name: str) -> None:
        def _insert() -> None:
            get_supabase_client().table("user_table").insert({"id": user_id, "full_name": full_name}).execute()

        await to_thread(_insert)

    async def get_full_name(self, user_id: str) -> str:
        def _select() -> None:
            response = get_supabase_client().table("user_table").select("full_name").eq("id", user_id).single().execute()
            data = response.data or {}
            return str(data.get("full_name", ""))
        
        return await to_thread(_select)
    
    async def sign_up(self, full_name: str, email: str, password: str) -> str:
        def _sign_up() -> str:
            response = get_supabase_client().auth.sign_up(
                {"email": email, "password": password, "options": {"data": {"full_name": full_name}}}
            )
            if response.user is None:
                raise ValueError("Signup failed")
            return str(response.user.id)
        
        return await to_thread(_sign_up)
    
    async def sign_in(self, email: str, password: str) -> tuple[AuthenticatedUser, str]:
        def _sign_in() -> tuple[AuthenticatedUser, str]:
            response = get_supabase_client().auth.sign_in_with_password({"email": email, "password": password})
            if response.user is None or response.session is None:
                raise ValueError("Login failed")
            user = AuthenticatedUser(id=str(response.user.id), email=email)
            return user, str(response.session.access_token)
        
        return await to_thread(_sign_in)