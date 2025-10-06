from datetime import datetime
from src.dao.user_dao import UserDAO
from src.dao.job_dao import JobDAO
from src.dao.bid_dao import BidDAO
from src.dao.jobstatus_dao import JobStatusDAO
from typing import List, Dict,Optional
class JobError(Exception):
    pass

class JobService:
    """Business logic for job operations."""
    
    def __init__(self):
        self.jobdao = JobDAO()
        self.userdao = UserDAO()
        self.biddao = BidDAO()
        self.job_status_dao = JobStatusDAO()
        
    def create_job(self, title: str, client_id: int, budget: float, deadline_str: str, 
                   assigned_to: Optional[int] = None) -> Dict:
        """Create a new job with validation."""
        # Validate client exists and has correct role
        client = self.userdao.get_user_by_id(client_id)
        if not client:
            raise JobError(f"Client with id {client_id} does not exist")
        if client["role"] != "client":
            raise JobError(f"User with id {client_id} is not a client")
        
        # Validate freelancer if assigned
        if assigned_to:
            freelancer = self.userdao.get_user_by_id(assigned_to)
            if not freelancer:
                raise JobError(f"Freelancer with id {assigned_to} does not exist")
            if freelancer["role"] != "freelancer":
                raise JobError(f"User with id {assigned_to} is not a freelancer")
        
        # Validate budget
        if budget <= 0:
            raise JobError("Budget must be greater than zero")
        
        # Validate and parse deadline
        try:
            deadline_date = datetime.strptime(deadline_str, "%Y-%m-%d").date()
        except ValueError:
            raise JobError(f"Invalid date format: {deadline_str}. Use YYYY-MM-DD")
        
        today = datetime.now().date()
        if deadline_date <= today:
            raise JobError(f"Deadline {deadline_str} must be in the future")
        
        # Check for duplicate job title by same client
        existing_job = self.jobdao.get_job_by_clientid_and_title(client_id, title)
        if existing_job:
            raise JobError(f"Client already has a job with title '{title}'")
        
        # Determine status based on assignment
        status = 'assigned' if assigned_to else 'open'
        
        # Create the job
        job = self.jobdao.create_job(title, client_id, budget, deadline_str, assigned_to, status)
        
        # Create initial status history
        if job:
            self.job_status_dao.create_job_status(job["job_id"], status)
        
        return job
    
    def update_job(self, job_id: int, fields: Dict) -> Dict:
        """Update job with validation."""
        job = self.jobdao.get_job_by_id(job_id)
        if not job:
            raise JobError(f"Job with id {job_id} does not exist")
        
        # Validate budget if being updated
        if "budget" in fields and fields["budget"] <= 0:
            raise JobError("Budget must be greater than zero")
        
        # Validate deadline if being updated
        if "deadline" in fields:
            try:
                deadline_date = datetime.strptime(fields["deadline"], "%Y-%m-%d").date()
                today = datetime.now().date()
                if deadline_date <= today:
                    raise JobError("Deadline must be in the future")
            except ValueError:
                raise JobError("Invalid deadline format. Use YYYY-MM-DD")
        
        # Validate freelancer if being assigned
        if "assigned_to" in fields and fields["assigned_to"]:
            freelancer = self.userdao.get_user_by_id(fields["assigned_to"])
            if not freelancer or freelancer["role"] != "freelancer":
                raise JobError(f"Invalid freelancer id {fields['assigned_to']}")
        
        # Validate status if being updated 
        if "status" in fields:
            valid_statuses = ['open', 'assigned', 'in-progress', 'completed'] 
            if fields["status"] not in valid_statuses : 
                raise JobError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}") 
            else: 
                if not job["assigned_to"] or not fields["assigned_to"]: 
                    raise JobError(f"Cannot update status as the job is not assigned to any freelancer")
            # Track status change in history
            if fields["status"] != job["status"]:
                self.job_status_dao.create_job_status(job_id, fields["status"])
        
        return self.jobdao.update_job(job_id, fields)
    
    def assign_freelancer_to_job(self, job_id: int, freelancer_id: int) -> Dict:
        """Assign a freelancer to a job."""
        job = self.jobdao.get_job_by_id(job_id)
        if not job:
            raise JobError(f"Job with id {job_id} does not exist")
        
        if job["status"] not in ['open', 'assigned']:
            raise JobError(f"Cannot assign freelancer to job with status '{job['status']}'")
        
        freelancer = self.userdao.get_user_by_id(freelancer_id)
        if not freelancer or freelancer["role"] != "freelancer":
            raise JobError(f"Freelancer with id {freelancer_id} does not exist")
        
        # Update job with assignment
        return self.update_job(job_id, {"assigned_to": freelancer_id, "status": "assigned"})
    
    def delete_job(self, job_id: int) -> Dict:
        """Delete a job."""
        job = self.jobdao.get_job_by_id(job_id)
        if not job:
            raise JobError(f"Job with id {job_id} does not exist")
        
        # Only allow deletion if job is not in progress or completed
        if job["status"] in ['in-progress', 'completed']:
            raise JobError(f"Cannot delete job with status '{job['status']}'")
        
        return self.jobdao.delete_job(job_id)
    
    def get_job_by_id(self, job_id: int) -> Dict:
        """Retrieve a job by ID."""
        job = self.jobdao.get_job_by_id(job_id)
        if not job:
            raise JobError(f"Job with id {job_id} does not exist")
        return job
    
    def get_jobs_by_client(self, client_id: int) -> List[Dict]:
        """Get all jobs for a client."""
        client = self.userdao.get_user_by_id(client_id)
        if not client or client["role"] != "client":
            raise JobError(f"Client with id {client_id} does not exist")
        return self.jobdao.get_jobs_by_client_id(client_id)
    
    def get_jobs_by_freelancer(self, freelancer_id: int) -> List[Dict]:
        """Get all jobs assigned to a freelancer."""
        freelancer = self.userdao.get_user_by_id(freelancer_id)
        if not freelancer or freelancer["role"] != "freelancer":
            raise JobError(f"Freelancer with id {freelancer_id} does not exist")
        return self.jobdao.get_jobs_by_freelancer_id(freelancer_id)
    
    def list_jobs(self, status: Optional[str] = None, limit: int = 100) -> List[Dict]:
        """List all jobs, optionally filtered by status."""
        if status:
            valid_statuses = ['open', 'assigned', 'in-progress', 'completed']
            if status not in valid_statuses:
                raise JobError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
            return self.jobdao.get_jobs_by_status(status)
        return self.jobdao.list_jobs(limit)