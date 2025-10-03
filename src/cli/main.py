import argparse
import json
from src.services.user_service import UserService, UserError
from src.services.job_service import JobService, JobError
from src.services.bid_service import BidService, BidError
from src.services.jobstatus_service import JobStatusService, JobStatusError


# ---------------- User CLI ----------------
class UserCLI:
    def __init__(self):
        self.user_service = UserService()

    def cmd_user_add(self, args):
        """Add a new user (client or freelancer)."""
        try:
            u = self.user_service.create_user(
                args.name, args.email, args.phone, args.role
            )
            print("Created user:")
            print(json.dumps(u, indent=2, default=str))
        except UserError as e:
            print("Error:", e)

    def cmd_user_list(self, args):
        """List all users or filter by role."""
        try:
            if args.role:
                users = self.user_service.list_users_by_role(args.role)
            else:
                users = self.user_service.list_users(limit=args.limit)
            print(json.dumps(users, indent=2, default=str))
        except UserError as e:
            print("Error:", e)

    def cmd_user_show(self, args):
        """Show details of a specific user."""
        try:
            u = self.user_service.get_user_by_id(args.user_id)
            print(json.dumps(u, indent=2, default=str))
        except UserError as e:
            print("Error:", e)

    def cmd_user_update(self, args):
        """Update user information."""
        try:
            fields = {}
            if args.name:
                fields["name"] = args.name
            if args.email:
                fields["email"] = args.email
            if args.phone:
                fields["phone"] = args.phone
            
            if not fields:
                print("No fields to update")
                return
            
            u = self.user_service.update_user(args.user_id, fields)
            print("Updated user:")
            print(json.dumps(u, indent=2, default=str))
        except UserError as e:
            print("Error:", e)

    def cmd_user_delete(self, args):
        """Delete a user."""
        try:
            u = self.user_service.remove_user(args.user_id)
            print("Deleted user:")
            print(json.dumps(u, indent=2, default=str))
        except UserError as e:
            print("Error:", e)


# ---------------- Job CLI ----------------
class JobCLI:
    def __init__(self):
        self.job_service = JobService()

    def cmd_job_create(self, args):
        """Create a new job."""
        try:
            j = self.job_service.create_job(
                args.title, args.client_id, args.budget, args.deadline, args.freelancer_id
            )
            print("Created job:")
            print(json.dumps(j, indent=2, default=str))
        except JobError as e:
            print("Error:", e)

    def cmd_job_list(self, args):
        """List all jobs or filter by status."""
        try:
            jobs = self.job_service.list_jobs(status=args.status, limit=args.limit)
            print(json.dumps(jobs, indent=2, default=str))
        except JobError as e:
            print("Error:", e)

    def cmd_job_show(self, args):
        """Show details of a specific job."""
        try:
            j = self.job_service.get_job_by_id(args.job_id)
            print(json.dumps(j, indent=2, default=str))
        except JobError as e:
            print("Error:", e)

    def cmd_job_update(self, args):
        """Update job information."""
        try:
            fields = {}
            if args.title:
                fields["title"] = args.title
            if args.budget:
                fields["budget"] = args.budget
            if args.deadline:
                fields["deadline"] = args.deadline
            if args.status:
                fields["status"] = args.status
            
            if not fields:
                print("No fields to update")
                return
            
            j = self.job_service.update_job(args.job_id, fields)
            print("Updated job:")
            print(json.dumps(j, indent=2, default=str))
        except JobError as e:
            print("Error:", e)

    def cmd_job_assign(self, args):
        """Assign a freelancer to a job."""
        try:
            j = self.job_service.assign_freelancer_to_job(args.job_id, args.freelancer_id)
            print("Assigned freelancer to job:")
            print(json.dumps(j, indent=2, default=str))
        except JobError as e:
            print("Error:", e)

    def cmd_job_by_client(self, args):
        """Get all jobs for a specific client."""
        try:
            jobs = self.job_service.get_jobs_by_client(args.client_id)
            print(json.dumps(jobs, indent=2, default=str))
        except JobError as e:
            print("Error:", e)

    def cmd_job_by_freelancer(self, args):
        """Get all jobs assigned to a specific freelancer."""
        try:
            jobs = self.job_service.get_jobs_by_freelancer(args.freelancer_id)
            print(json.dumps(jobs, indent=2, default=str))
        except JobError as e:
            print("Error:", e)

    def cmd_job_delete(self, args):
        """Delete a job."""
        try:
            j = self.job_service.delete_job(args.job_id)
            print("Deleted job:")
            print(json.dumps(j, indent=2, default=str))
        except JobError as e:
            print("Error:", e)


# ---------------- Bid CLI ----------------
class BidCLI:
    def __init__(self):
        self.bid_service = BidService()

    def cmd_bid_create(self, args):
        """Create a new bid."""
        try:
            b = self.bid_service.create_bid(
                args.job_id, args.freelancer_id, args.amount, args.message
            )
            print("Created bid:")
            print(json.dumps(b, indent=2, default=str))
        except BidError as e:
            print("Error:", e)

    def cmd_bid_list(self, args):
        """List all bids or filter by status."""
        try:
            bids = self.bid_service.list_bids(status=args.status, limit=args.limit)
            print(json.dumps(bids, indent=2, default=str))
        except BidError as e:
            print("Error:", e)

    def cmd_bid_show(self, args):
        """Show details of a specific bid."""
        try:
            b = self.bid_service.get_bid_by_id(args.bid_id)
            print(json.dumps(b, indent=2, default=str))
        except BidError as e:
            print("Error:", e)

    def cmd_bid_by_job(self, args):
        """Get all bids for a specific job."""
        try:
            bids = self.bid_service.get_bids_by_job(args.job_id)
            print(json.dumps(bids, indent=2, default=str))
        except BidError as e:
            print("Error:", e)

    def cmd_bid_by_freelancer(self, args):
        """Get all bids made by a specific freelancer."""
        try:
            bids = self.bid_service.get_bids_by_freelancer(args.freelancer_id)
            print(json.dumps(bids, indent=2, default=str))
        except BidError as e:
            print("Error:", e)

    def cmd_bid_accept(self, args):
        """Accept a bid (only if it's the lowest bid)."""
        try:
            b = self.bid_service.accept_bid(args.bid_id)
            print("Accepted bid (and rejected all others):")
            print(json.dumps(b, indent=2, default=str))
        except BidError as e:
            print("Error:", e)

    def cmd_bid_reject(self, args):
        """Reject a bid."""
        try:
            b = self.bid_service.reject_bid(args.bid_id)
            print("Rejected bid:")
            print(json.dumps(b, indent=2, default=str))
        except BidError as e:
            print("Error:", e)

    def cmd_bid_update(self, args):
        """Update bid information."""
        try:
            fields = {}
            if args.amount:
                fields["amount"] = args.amount
            if args.message:
                fields["message"] = args.message
            
            if not fields:
                print("No fields to update")
                return
            
            b = self.bid_service.update_bid(args.bid_id, fields)
            print("Updated bid:")
            print(json.dumps(b, indent=2, default=str))
        except BidError as e:
            print("Error:", e)

    def cmd_bid_delete(self, args):
        """Delete a bid."""
        try:
            b = self.bid_service.delete_bid(args.bid_id)
            print("Deleted bid:")
            print(json.dumps(b, indent=2, default=str))
        except BidError as e:
            print("Error:", e)


# ---------------- Job Status CLI ----------------
class JobStatusCLI:
    def __init__(self):
        self.job_status_service = JobStatusService()

    def cmd_status_history(self, args):
        """Get status history for a job."""
        try:
            history = self.job_status_service.get_status_history(args.job_id)
            print("Job Status History:")
            print(json.dumps(history, indent=2, default=str))
        except JobStatusError as e:
            print("Error:", e)

    def cmd_status_latest(self, args):
        """Get the latest status for a job."""
        try:
            status = self.job_status_service.get_latest_status(args.job_id)
            print("Latest Job Status:")
            print(json.dumps(status, indent=2, default=str))
        except JobStatusError as e:
            print("Error:", e)


# ---------------- Main Freelance CLI ----------------
class FreelanceCLI:
    def __init__(self):
        self.user_cli = UserCLI()
        self.job_cli = JobCLI()
        self.bid_cli = BidCLI()
        self.job_status_cli = JobStatusCLI()
        self.parser = self.build_parser()

    def build_parser(self):
        parser = argparse.ArgumentParser(prog="freelance-cli")
        sub = parser.add_subparsers(dest="cmd")

        # ========== User Commands ==========
        p_user = sub.add_parser("user", help="user commands")
        puser_sub = p_user.add_subparsers(dest="action")
        
        # User add
        addu = puser_sub.add_parser("add", help="Add a new user")
        addu.add_argument("--name", required=True, help="User name")
        addu.add_argument("--email", required=True, help="User email")
        addu.add_argument("--phone", required=True, help="User phone")
        addu.add_argument("--role", required=True, choices=["client", "freelancer"], help="User role")
        addu.set_defaults(func=self.user_cli.cmd_user_add)

        # User list
        listu = puser_sub.add_parser("list", help="List users")
        listu.add_argument("--role", choices=["client", "freelancer"], help="Filter by role")
        listu.add_argument("--limit", type=int, default=100, help="Maximum number of users")
        listu.set_defaults(func=self.user_cli.cmd_user_list)

        # User show
        showu = puser_sub.add_parser("show", help="Show user details")
        showu.add_argument("--user_id", type=int, required=True, help="User ID")
        showu.set_defaults(func=self.user_cli.cmd_user_show)

        # User update
        updu = puser_sub.add_parser("update", help="Update user")
        updu.add_argument("--user_id", type=int, required=True, help="User ID")
        updu.add_argument("--name", help="New name")
        updu.add_argument("--email", help="New email")
        updu.add_argument("--phone", help="New phone")
        updu.set_defaults(func=self.user_cli.cmd_user_update)

        # User delete
        delu = puser_sub.add_parser("delete", help="Delete user")
        delu.add_argument("--user_id", type=int, required=True, help="User ID")
        delu.set_defaults(func=self.user_cli.cmd_user_delete)

        # ========== Job Commands ==========
        p_job = sub.add_parser("job", help="job commands")
        pjob_sub = p_job.add_subparsers(dest="action")

        # Job create
        createj = pjob_sub.add_parser("create", help="Create a new job")
        createj.add_argument("--title", required=True, help="Job title")
        createj.add_argument("--client_id", type=int, required=True, help="Client ID")
        createj.add_argument("--budget", type=float, required=True, help="Job budget")
        createj.add_argument("--deadline", required=True, help="Job deadline (YYYY-MM-DD)")
        createj.add_argument("--freelancer_id", type=int, help="Freelancer ID (optional)")
        createj.set_defaults(func=self.job_cli.cmd_job_create)

        # Job list
        listj = pjob_sub.add_parser("list", help="List jobs")
        listj.add_argument("--status", choices=["open", "assigned", "in-progress", "completed"], help="Filter by status")
        listj.add_argument("--limit", type=int, default=100, help="Maximum number of jobs")
        listj.set_defaults(func=self.job_cli.cmd_job_list)

        # Job show
        showj = pjob_sub.add_parser("show", help="Show job details")
        showj.add_argument("--job_id", type=int, required=True, help="Job ID")
        showj.set_defaults(func=self.job_cli.cmd_job_show)

        # Job update
        updj = pjob_sub.add_parser("update", help="Update job")
        updj.add_argument("--job_id", type=int, required=True, help="Job ID")
        updj.add_argument("--title", help="New title")
        updj.add_argument("--budget", type=float, help="New budget")
        updj.add_argument("--deadline", help="New deadline (YYYY-MM-DD)")
        updj.add_argument("--status", choices=["open", "assigned", "in-progress", "completed"], help="New status")
        updj.set_defaults(func=self.job_cli.cmd_job_update)

        # Job assign
        assignj = pjob_sub.add_parser("assign", help="Assign freelancer to job")
        assignj.add_argument("--job_id", type=int, required=True, help="Job ID")
        assignj.add_argument("--freelancer_id", type=int, required=True, help="Freelancer ID")
        assignj.set_defaults(func=self.job_cli.cmd_job_assign)

        # Job by client
        jbc = pjob_sub.add_parser("by-client", help="Get jobs by client")
        jbc.add_argument("--client_id", type=int, required=True, help="Client ID")
        jbc.set_defaults(func=self.job_cli.cmd_job_by_client)

        # Job by freelancer
        jbf = pjob_sub.add_parser("by-freelancer", help="Get jobs by freelancer")
        jbf.add_argument("--freelancer_id", type=int, required=True, help="Freelancer ID")
        jbf.set_defaults(func=self.job_cli.cmd_job_by_freelancer)

        # Job delete
        delj = pjob_sub.add_parser("delete", help="Delete job")
        delj.add_argument("--job_id", type=int, required=True, help="Job ID")
        delj.set_defaults(func=self.job_cli.cmd_job_delete)

        # ========== Bid Commands ==========
        p_bid = sub.add_parser("bid", help="bid commands")
        pbid_sub = p_bid.add_subparsers(dest="action")

        # Bid create
        createb = pbid_sub.add_parser("create", help="Create a new bid")
        createb.add_argument("--job_id", type=int, required=True, help="Job ID")
        createb.add_argument("--freelancer_id", type=int, required=True, help="Freelancer ID")
        createb.add_argument("--amount", type=float, required=True, help="Bid amount")
        createb.add_argument("--message", help="Bid message (optional)")
        createb.set_defaults(func=self.bid_cli.cmd_bid_create)

        # Bid list
        listb = pbid_sub.add_parser("list", help="List bids")
        listb.add_argument("--status", choices=["pending", "accepted", "rejected"], help="Filter by status")
        listb.add_argument("--limit", type=int, default=100, help="Maximum number of bids")
        listb.set_defaults(func=self.bid_cli.cmd_bid_list)

        # Bid show
        showb = pbid_sub.add_parser("show", help="Show bid details")
        showb.add_argument("--bid_id", type=int, required=True, help="Bid ID")
        showb.set_defaults(func=self.bid_cli.cmd_bid_show)

        # Bid by job
        bbj = pbid_sub.add_parser("by-job", help="Get bids by job")
        bbj.add_argument("--job_id", type=int, required=True, help="Job ID")
        bbj.set_defaults(func=self.bid_cli.cmd_bid_by_job)

        # Bid by freelancer
        bbf = pbid_sub.add_parser("by-freelancer", help="Get bids by freelancer")
        bbf.add_argument("--freelancer_id", type=int, required=True, help="Freelancer ID")
        bbf.set_defaults(func=self.bid_cli.cmd_bid_by_freelancer)

        # Bid accept
        acceptb = pbid_sub.add_parser("accept", help="Accept a bid (must be lowest)")
        acceptb.add_argument("--bid_id", type=int, required=True, help="Bid ID")
        acceptb.set_defaults(func=self.bid_cli.cmd_bid_accept)

        # Bid reject
        rejectb = pbid_sub.add_parser("reject", help="Reject a bid")
        rejectb.add_argument("--bid_id", type=int, required=True, help="Bid ID")
        rejectb.set_defaults(func=self.bid_cli.cmd_bid_reject)

        # Bid update
        updb = pbid_sub.add_parser("update", help="Update bid")
        updb.add_argument("--bid_id", type=int, required=True, help="Bid ID")
        updb.add_argument("--amount", type=float, help="New amount")
        updb.add_argument("--message", help="New message")
        updb.set_defaults(func=self.bid_cli.cmd_bid_update)

        # Bid delete
        delb = pbid_sub.add_parser("delete", help="Delete bid")
        delb.add_argument("--bid_id", type=int, required=True, help="Bid ID")
        delb.set_defaults(func=self.bid_cli.cmd_bid_delete)

        # ========== Job Status Commands ==========
        p_status = sub.add_parser("status", help="job status commands")
        pstatus_sub = p_status.add_subparsers(dest="action")

        # Status history
        historyj = pstatus_sub.add_parser("history", help="Get job status history")
        historyj.add_argument("--job_id", type=int, required=True, help="Job ID")
        historyj.set_defaults(func=self.job_status_cli.cmd_status_history)

        # Status latest
        latestj = pstatus_sub.add_parser("latest", help="Get latest job status")
        latestj.add_argument("--job_id", type=int, required=True, help="Job ID")
        latestj.set_defaults(func=self.job_status_cli.cmd_status_latest)

        return parser

    def run(self):
        args = self.parser.parse_args()
        if not hasattr(args, "func"):
            self.parser.print_help()
            return
        args.func(args)


def main():
    cli = FreelanceCLI()
    cli.run()


if __name__ == "__main__":
    main()