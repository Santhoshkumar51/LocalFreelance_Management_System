from typing import Optional, List, Dict
from src.config import get_supabase

class UserDAO:
    """Data Access Object for user-related database operations."""
    
    def __init__(self):
        self.sb = get_supabase()
    
    def create_user(self, name: str, email: str, phone: str, role: str) -> Optional[Dict]:
        """Create a new user and return the inserted record."""
        # Insert the new user
        self.sb.table("users").insert({
            "name": name, 
            "email": email, 
            "phone": phone, 
            "role": role
        }).execute()
        
        # Fetch the newly created user by email
        resp = self.sb.table("users").select("*").eq("email", email).execute()
        return resp.data[0] if resp.data else None
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Retrieve a single user by ID."""
        resp = self.sb.table("users").select("*").eq("user_id", user_id).execute()
        return resp.data[0] if resp.data else None
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Retrieve a single user by email."""
        resp = self.sb.table("users").select("*").eq("email", email).execute()
        return resp.data[0] if resp.data else None

    def get_users_by_role(self, role: str) -> List[Dict]:
        """Retrieve all users with a specific role."""
        resp = self.sb.table("users").select("*").eq("role", role).execute()
        return resp.data or []

    def update_user(self, user_id: int, fields: Dict) -> Optional[Dict]:
        """Update user fields and return the updated record."""
        # Update the user
        self.sb.table("users").update(fields).eq("user_id", user_id).execute()
        
        # Fetch and return updated user
        resp = self.sb.table("users").select("*").eq("user_id", user_id).execute()
        return resp.data[0] if resp.data else None

    def delete_user(self, user_id: int) -> Optional[Dict]:
        """Delete a user and return the deleted record."""
        # Get user before deleting
        user = self.get_user_by_id(user_id)
        
        # Delete the user if exists
        if user:
            self.sb.table("users").delete().eq("user_id", user_id).execute()
        
        return user

    def list_users(self, limit: int = 100) -> List[Dict]:
        """Retrieve all users with optional limit."""
        resp = self.sb.table("users").select("*").order("user_id", desc=False).limit(limit).execute()
        return resp.data or [] 