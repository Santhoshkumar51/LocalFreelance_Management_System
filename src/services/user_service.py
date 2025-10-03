from src.dao.user_dao import UserDAO
from src.dao.job_dao import JobDAO
from src.dao.bid_dao import BidDAO
from typing import List,Dict

class UserError(Exception):
    pass
class UserService:
    """Business logic for user operations."""
    
    def __init__(self):
        self.userdao = UserDAO()
        self.jobdao = JobDAO()
        self.biddao = BidDAO()
        
    def create_user(self, name: str, email: str, phone: str, role: str) -> Dict:
        """Create a new user with validation."""
        # Check if email already exists
        existing_user = self.userdao.get_user_by_email(email)
        if existing_user:
            raise UserError(f"User with email {email} already exists")
        
        # Validate role
        if role not in ("client", "freelancer"):
            raise UserError("User role must be either 'client' or 'freelancer'")
        
        # Validate email format (basic)
        if not email or "@" not in email:
            raise UserError("Invalid email format")
        
        # Validate name
        if not name or len(name.strip()) == 0:
            raise UserError("Name cannot be empty")
        
        return self.userdao.create_user(name, email, phone, role)
    
    def remove_user(self, user_id: int) -> Dict:
        """Remove a user after checking for active jobs/bids."""
        user = self.userdao.get_user_by_id(user_id)
        if not user:
            raise UserError(f"User with id {user_id} does not exist")
        
        # Check if client has posted active jobs
        if user["role"] == "client":
            jobs = self.jobdao.get_jobs_by_client_id(user_id)
            if jobs:
                raise UserError(f"Client with id {user_id} has posted active jobs")
        
        # Check if freelancer is assigned to active jobs
        if user["role"] == "freelancer":
            assigned_jobs = self.jobdao.get_jobs_by_freelancer_id(user_id)
            if assigned_jobs:
                raise UserError(f"Freelancer with id {user_id} is assigned to active jobs")
            
            # Check if freelancer has pending bids
            bids = self.biddao.get_bids_by_freelancer_id(user_id)
            if bids:
                raise UserError(f"Freelancer with id {user_id} has active bids")
        
        return self.userdao.delete_user(user_id)
    
    def update_user(self, user_id: int, fields: Dict) -> Dict:
        """Update user information with validation."""
        user = self.userdao.get_user_by_id(user_id)
        if not user:
            raise UserError(f"User with id {user_id} does not exist")
        
        # Validate email if being updated
        if "email" in fields:
            existing = self.userdao.get_user_by_email(fields["email"])
            if existing and existing["user_id"] != user_id:
                raise UserError(f"Email {fields['email']} is already in use")
        
        # Prevent role changes if user has active jobs/bids
        if "role" in fields and fields["role"] != user["role"]:
            if user["role"] == "client":
                jobs = self.jobdao.get_jobs_by_client_id(user_id)
                if jobs:
                    raise UserError("Cannot change role while having active jobs")
            elif user["role"] == "freelancer":
                jobs = self.jobdao.get_jobs_by_freelancer_id(user_id)
                bids = self.biddao.get_bids_by_freelancer_id(user_id)
                if jobs or bids:
                    raise UserError("Cannot change role while having active jobs or bids")
        
        return self.userdao.update_user(user_id, fields)
    
    def get_user_by_id(self, user_id: int) -> Dict:
        """Retrieve a user by ID."""
        user = self.userdao.get_user_by_id(user_id)
        if not user:
            raise UserError(f"User with id {user_id} does not exist")
        return user
    
    def list_users(self, limit: int = 100) -> List[Dict]:
        """List all users."""
        return self.userdao.list_users(limit)
    
    def list_users_by_role(self, role: str) -> List[Dict]:
        """List users by role."""
        if role not in ("client", "freelancer"):
            raise UserError("Role must be either 'client' or 'freelancer'")
        return self.userdao.get_users_by_role(role)