from typing import List, Dict, Optional
from src.config import get_supabase

class JobDAO:
    """Data Access Object for job-related database operations."""
    
    def __init__(self):
        self.sb = get_supabase()
    
    def create_job(self, title: str, client_id: int, budget: float, deadline: str, 
               assigned_to: Optional[int] = None, status: Optional[str] = None) -> Optional[Dict]:
        """Create a new job and return the inserted record."""
        # Insert the new job
        job_data = {
            "title": title, 
            "client_id": client_id, 
            "budget": budget,
            "deadline": deadline
        }
        if assigned_to:
            job_data["assigned_to"] = assigned_to
            job_data["status"] = "assigned"  # Override default only when assigning
            
        self.sb.table("jobs").insert(job_data).execute()
        
        # Fetch the most recently created job
        resp = self.sb.table("jobs").select("*").order("job_id", desc=True).limit(1).execute()
        return resp.data[0] if resp.data else None
    
    def get_job_by_id(self, job_id: int) -> Optional[Dict]:
        """Retrieve a single job by ID."""
        resp = self.sb.table("jobs").select("*").eq("job_id", job_id).execute()
        return resp.data[0] if resp.data else None
    
    def get_jobs_by_client_id(self, client_id: int) -> List[Dict]:
        """Retrieve all jobs posted by a specific client."""
        resp = self.sb.table("jobs").select("*").eq("client_id", client_id).execute()
        return resp.data or []
    
    def get_job_by_clientid_and_title(self, client_id: int, title: str) -> Optional[List[Dict]]:
        """Check if a job with the given title exists for the client."""
        resp = self.sb.table("jobs").select("*").match({
            "client_id": client_id,
            "title": title
        }).execute().data
        return resp if resp else None
    
    def get_jobs_by_freelancerid(self, freelancer_id: int) -> List[Dict]:
        """Retrieve all jobs assigned to a specific freelancer."""
        resp = self.sb.table("jobs").select("*").eq("assigned_to", freelancer_id).execute()
        return resp.data or []

    def update_job(self, job_id: int, fields: Dict) -> Optional[Dict]:
        """Update job fields and return the updated record."""
        # Update the job
        self.sb.table("jobs").update(fields).eq("job_id", job_id).execute()
        
        # Fetch and return updated job
        resp = self.sb.table("jobs").select("*").eq("job_id", job_id).execute()
        return resp.data[0] if resp.data else None

    def delete_job(self, job_id: int) -> Optional[Dict]:
        """Delete a job and return the deleted record."""
        # Get job before deleting
        job = self.get_job_by_id(job_id)
        
        # Delete the job
        if job:
            self.sb.table("jobs").delete().eq("job_id", job_id).execute()
        
        return job

    def list_jobs(self, limit: int = 100) -> List[Dict]:
        """Retrieve all jobs with optional limit."""
        resp = self.sb.table("jobs").select("*").order("job_id", desc=False).limit(limit).execute()
        return resp.data or []