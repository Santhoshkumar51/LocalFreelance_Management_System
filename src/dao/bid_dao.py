from typing import Optional, List, Dict
from src.config import get_supabase

# ==================== BID DAO ====================
class BidDAO:
    """Data Access Object for bid-related database operations."""
    
    def __init__(self):
        self.sb = get_supabase()
    
    def create_bid(self, job_id: int, freelancer_id: int, amount: float, 
                   message: Optional[str] = None) -> Optional[Dict]:
        """Create a new bid and return the inserted record."""
        # Insert the new bid
        bid_data = {
            "job_id": job_id,
            "freelancer_id": freelancer_id,
            "amount": amount
        }
        if message:
            bid_data["message"] = message
            
        self.sb.table("bids").insert(bid_data).execute()
        
        # Fetch the most recently created bid
        resp = self.sb.table("bids").select("*").order("bid_id", desc=True).limit(1).execute()
        return resp.data[0] if resp.data else None
    
    def get_bid_by_id(self, bid_id: int) -> Optional[Dict]:
        """Retrieve a single bid by ID."""
        resp = self.sb.table("bids").select("*").eq("bid_id", bid_id).execute()
        return resp.data[0] if resp.data else None
    
    def get_bids_by_job_id(self, job_id: int) -> List[Dict]:
        """Retrieve all bids for a specific job."""
        resp = self.sb.table("bids").select("*").eq("job_id", job_id).execute()
        return resp.data or []
    
    def get_bids_by_freelancer_id(self, freelancer_id: int) -> List[Dict]:
        """Retrieve all bids made by a specific freelancer."""
        resp = self.sb.table("bids").select("*").eq("freelancer_id", freelancer_id).execute()
        return resp.data or []
    
    def get_bid_by_job_and_freelancer(self, job_id: int, freelancer_id: int) -> Optional[Dict]:
        """Check if a bid exists for a job-freelancer combination."""
        resp = self.sb.table("bids").select("*").match({
            "job_id": job_id,
            "freelancer_id": freelancer_id
        }).execute()
        return resp.data[0] if resp.data else None
    
    def get_bids_by_status(self, bid_status: str) -> List[Dict]:
        """Retrieve all bids with a specific status."""
        resp = self.sb.table("bids").select("*").eq("bid_status", bid_status).execute()
        return resp.data or []

    def update_bid(self, bid_id: int, fields: Dict) -> Optional[Dict]:
        """Update bid fields and return the updated record."""
        # Update the bid
        self.sb.table("bids").update(fields).eq("bid_id", bid_id).execute()
        
        # Fetch and return updated bid
        resp = self.sb.table("bids").select("*").eq("bid_id", bid_id).execute()
        return resp.data[0] if resp.data else None

    def delete_bid(self, bid_id: int) -> Optional[Dict]:
        """Delete a bid and return the deleted record."""
        # Get bid before deleting
        bid = self.get_bid_by_id(bid_id)
        
        # Delete the bid if exists
        if bid:
            self.sb.table("bids").delete().eq("bid_id", bid_id).execute()
        
        return bid

    def list_bids(self, limit: int = 100) -> List[Dict]:
        """Retrieve all bids with optional limit."""
        resp = self.sb.table("bids").select("*").order("bid_id", desc=False).limit(limit).execute()
        return resp.data or []
