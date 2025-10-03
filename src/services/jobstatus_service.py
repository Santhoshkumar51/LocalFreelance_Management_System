from src.dao.job_dao import JobDAO
from src.dao.jobstatus_dao import JobStatusDAO
from typing import List, Dict
class JobStatusError(Exception):
    """Exception raised for job status-related errors."""
    pass
class JobStatusService:
    """Business logic for job status history tracking."""
    
    def __init__(self):
        self.job_status_dao = JobStatusDAO()
        self.jobdao = JobDAO()
        
    def create_job_status(self, job_id: int, status: str) -> Dict:
        """Create a new job status record with validation."""
        # Validate job exists
        job = self.jobdao.get_job_by_id(job_id)
        if not job:
            raise JobStatusError(f"Job with id {job_id} does not exist")
        
        # Validate status
        valid_statuses = ['open', 'assigned', 'in-progress', 'completed']
        if status not in valid_statuses:
            raise JobStatusError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
        
        return self.job_status_dao.create_job_status(job_id, status)
    
    def get_status_history(self, job_id: int) -> List[Dict]:
        """Get complete status history for a job."""
        job = self.jobdao.get_job_by_id(job_id)
        if not job:
            raise JobStatusError(f"Job with id {job_id} does not exist")
        return self.job_status_dao.get_status_history_by_job_id(job_id)
    
    def get_latest_status(self, job_id: int) -> Dict:
        """Get the most recent status for a job."""
        job = self.jobdao.get_job_by_id(job_id)
        if not job:
            raise JobStatusError(f"Job with id {job_id} does not exist")
        
        status = self.job_status_dao.get_latest_status_by_job_id(job_id)
        if not status:
            raise JobStatusError(f"No status history found for job {job_id}")
        return status
    
    def delete_status(self, status_id: int) -> Dict:
        """Delete a status record."""
        status = self.job_status_dao.get_status_by_id(status_id)
        if not status:
            raise JobStatusError(f"Status with id {status_id} does not exist")
        return self.job_status_dao.delete_status(status_id)
    
    def list_all_statuses(self, limit: int = 100) -> List[Dict]:
        """List all status records."""
        return self.job_status_dao.list_all_statuses(limit)