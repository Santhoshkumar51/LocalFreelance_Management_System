from typing import List, Dict,Optional
from src.dao.bid_dao import BidDAO
from src.dao.job_dao import JobDAO
from src.dao.user_dao import UserDAO
from src.dao.jobstatus_dao import JobStatusDAO

class BidError(Exception):
    """Exception raised for bid-related errors."""
    pass

class BidService:
    """Business logic for bid operations."""
    
    def __init__(self):
        self.biddao = BidDAO()
        self.jobdao = JobDAO()
        self.userdao = UserDAO()
        self.jobstatusdao = JobStatusDAO()
        
    def create_bid(self, job_id: int, freelancer_id: int, amount: float, 
                   message: Optional[str] = None) -> Dict:
        """Create a new bid with validation."""
        # Validate job exists and is open
        job = self.jobdao.get_job_by_id(job_id)
        if not job:
            raise BidError(f"Job with id {job_id} does not exist")
        if job["status"] != "open":
            raise BidError(f"Cannot bid on job with status '{job['status']}'")
        
        # Validate freelancer exists and has correct role
        freelancer = self.userdao.get_user_by_id(freelancer_id)
        if not freelancer:
            raise BidError(f"Freelancer with id {freelancer_id} does not exist")
        if freelancer["role"] != "freelancer":
            raise BidError(f"User with id {freelancer_id} is not a freelancer")
        
        # Validate amount
        if amount <= 0:
            raise BidError("Bid amount must be greater than zero")
        
        # Check if bid already exists for this job-freelancer combination
        existing_bid = self.biddao.get_bid_by_job_and_freelancer(job_id, freelancer_id)
        if existing_bid:
            raise BidError(f"Freelancer has already placed a bid on job {job_id}")
        
        return self.biddao.create_bid(job_id, freelancer_id, amount, message)
    
    def update_bid(self, bid_id: int, fields: Dict) -> Dict:
        """Update bid with validation."""
        bid = self.biddao.get_bid_by_id(bid_id)
        if not bid:
            raise BidError(f"Bid with id {bid_id} does not exist")
        
        # Validate amount if being updated
        if "amount" in fields and fields["amount"] <= 0:
            raise BidError("Bid amount must be greater than zero")
        
        # Validate bid_status if being updated
        if "bid_status" in fields:
            valid_statuses = ['pending', 'accepted', 'rejected']
            if fields["bid_status"] not in valid_statuses:
                raise BidError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
            
            # If accepting bid, assign freelancer to job
            if fields["bid_status"] == "accepted":
                job = self.jobdao.get_job_by_id(bid["job_id"])
                if job and job["status"] == "open":
                    self.jobdao.update_job(bid["job_id"], {
                        "assigned_to": bid["freelancer_id"],
                        "status": "assigned"
                    })
        
        # Don't allow updates if bid is already accepted or rejected
        if bid["bid_status"] in ['accepted', 'rejected'] and "bid_status" not in fields:
            raise BidError(f"Cannot update bid with status '{bid['bid_status']}'")
        
        return self.biddao.update_bid(bid_id, fields)
    
    def accept_bid(self, bid_id: int) -> Dict:
        """Accept a bid only if it is the lowest bid for that job, then reject all others."""
        bid = self.biddao.get_bid_by_id(bid_id)
        if not bid:
            raise BidError(f"Bid with id {bid_id} does not exist")
    
        if bid["bid_status"] != "pending":
            raise BidError(f"Cannot accept bid with status '{bid['bid_status']}'")
    
        # Validate job exists and is open
        job = self.jobdao.get_job_by_id(bid["job_id"])
        if not job:
            raise BidError(f"Job with id {bid['job_id']} does not exist")
        if job["status"] != "open":
            raise BidError(f"Cannot accept bids for job with status '{job['status']}'")
    
        # Get all pending bids for this job
        all_bids = self.biddao.get_bids_by_job_id(bid["job_id"])
        pending_bids = [b for b in all_bids if b["bid_status"] == "pending"]
    
        if not pending_bids:
            raise BidError(f"No pending bids found for job {bid['job_id']}")
    
        # Find the lowest bid
        lowest_bid = min(pending_bids, key=lambda x: x["amount"])
    
        # Check if the bid being accepted is the lowest
        if bid["bid_id"] != lowest_bid["bid_id"]:
            raise BidError(f"Cannot accept bid. Bid {lowest_bid['bid_id']} with amount {lowest_bid['amount']} is lower")
    
        # Get IDs of all other pending bids to reject
        other_bid_ids = [b["bid_id"] for b in pending_bids if b["bid_id"] != bid_id]
    
        # Reject all other bids
        if other_bid_ids:
            for other_bid_id in other_bid_ids:
                self.biddao.update_bid(other_bid_id, {"bid_status": "rejected"})
    
        # Update job: assign freelancer and change status to 'assigned'
        self.jobdao.update_job(bid["job_id"], {
            "assigned_to": bid["freelancer_id"],
            "status": "assigned"
        })
    
        # Track job status change in history
        self.jobstatusdao.create_job_status(bid["job_id"], "assigned")
    
        # Accept the bid
        accepted_bid = self.biddao.update_bid(bid_id, {"bid_status": "accepted"})
    
        return accepted_bid
    
    def reject_bid(self, bid_id: int) -> Dict:
        """Reject a bid."""
        return self.update_bid(bid_id, {"bid_status": "rejected"})
    
    def delete_bid(self, bid_id: int) -> Dict:
        """Delete a bid."""
        bid = self.biddao.get_bid_by_id(bid_id)
        if not bid:
            raise BidError(f"Bid with id {bid_id} does not exist")
        
        # Only allow deletion if bid is pending
        if bid["bid_status"] != "pending":
            raise BidError(f"Cannot delete bid with status '{bid['bid_status']}'")
        
        return self.biddao.delete_bid(bid_id)
    
    def get_bid_by_id(self, bid_id: int) -> Dict:
        """Retrieve a bid by ID."""
        bid = self.biddao.get_bid_by_id(bid_id)
        if not bid:
            raise BidError(f"Bid with id {bid_id} does not exist")
        return bid
    
    def get_bids_by_job(self, job_id: int) -> List[Dict]:
        """Get all bids for a specific job."""
        job = self.jobdao.get_job_by_id(job_id)
        if not job:
            raise BidError(f"Job with id {job_id} does not exist")
        return self.biddao.get_bids_by_job_id(job_id)
    
    def get_bids_by_freelancer(self, freelancer_id: int) -> List[Dict]:
        """Get all bids made by a specific freelancer."""
        freelancer = self.userdao.get_user_by_id(freelancer_id)
        if not freelancer or freelancer["role"] != "freelancer":
            raise BidError(f"Freelancer with id {freelancer_id} does not exist")
        return self.biddao.get_bids_by_freelancer_id(freelancer_id)
    
    def list_bids(self, status: Optional[str] = None, limit: int = 100) -> List[Dict]:
        """List all bids, optionally filtered by status."""
        if status:
            valid_statuses = ['pending', 'accepted', 'rejected']
            if status not in valid_statuses:
                raise BidError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
            return self.biddao.get_bids_by_status(status)
        return self.biddao.list_bids(limit)