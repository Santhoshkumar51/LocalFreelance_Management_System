from typing import List, Dict, Optional
from src.config import get_supabase

# ==================== JOB STATUS DAO ====================
class JobStatusDAO:
    """Data Access Object for job status history tracking."""
    
    def __init__(self):
        self.sb = get_supabase()
    
    def create_job_status(self, job_id: int, status: str) -> Optional[Dict]:
        """Create a new job status record and return it."""
        # Insert the new status
        self.sb.table("job_status").insert({
            "job_id": job_id,
            "status": status
        }).execute()
        
        # Fetch the most recently created status
        resp = self.sb.table("job_status").select("*").order("status_id", desc=True).limit(1).execute()
        return resp.data[0] if resp.data else None
    
    def get_status_by_id(self, status_id: int) -> Optional[Dict]:
        """Retrieve a single status record by ID."""
        resp = self.sb.table("job_status").select("*").eq("status_id", status_id).execute()
        return resp.data[0] if resp.data else None
    
    def get_status_history_by_job_id(self, job_id: int) -> List[Dict]:
        """Retrieve all status history for a specific job."""
        resp = self.sb.table("job_status").select("*").eq("job_id", job_id).order("updated_at", desc=False).execute()
        return resp.data or []
    
    def get_latest_status_by_job_id(self, job_id: int) -> Optional[Dict]:
        """Retrieve the most recent status for a specific job."""
        resp = self.sb.table("job_status").select("*").eq("job_id", job_id).order("updated_at", desc=True).limit(1).execute()
        return resp.data[0] if resp.data else None

    def delete_status(self, status_id: int) -> Optional[Dict]:
        """Delete a status record and return the deleted record."""
        # Get status before deleting
        status = self.get_status_by_id(status_id)
        
        # Delete the status if exists
        if status:
            self.sb.table("job_status").delete().eq("status_id", status_id).execute()
        
        return status

    def list_all_statuses(self, limit: int = 100) -> List[Dict]:
        """Retrieve all status records with optional limit."""
        resp = self.sb.table("job_status").select("*").order("updated_at", desc=False).limit(limit).execute()
        return resp.data or []