import streamlit as st
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent))

from src.services.user_service import UserService, UserError
from src.services.job_service import JobService, JobError
from src.services.bid_service import BidService, BidError
from src.services.jobstatus_service import JobStatusService, JobStatusError

# Initialize services
@st.cache_resource
def get_services():
    return {
        'user': UserService(),
        'job': JobService(),
        'bid': BidService(),
        'status': JobStatusService()
    }

services = get_services()

# Page config
st.set_page_config(
    page_title="Freelance Management System",
    page_icon="💼",
    layout="wide"
)

st.title("💼 Freelance Management System")

# Sidebar navigation
page = st.sidebar.selectbox(
    "Choose a page",
    ["Users", "Jobs", "Bids", "Job Status"]
)

# ========== USERS PAGE ==========
if page == "Users":
    st.header("👥 User Management")
    
    tab1, tab2, tab3 = st.tabs(["Create User", "View Users", "Update/Delete User"])
    
    with tab1:
        st.subheader("Create New User")
        with st.form("create_user"):
            name = st.text_input("Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone")
            role = st.selectbox("Role", ["client", "freelancer"])
            
            if st.form_submit_button("Create User"):
                try:
                    user = services['user'].create_user(name, email, phone, role)
                    st.success(f"✅ User created successfully! ID: {user['user_id']}")
                    st.json(user)
                except UserError as e:
                    st.error(f"❌ Error: {e}")
    
    with tab2:
        st.subheader("View Users")
        col1, col2 = st.columns(2)
        with col1:
            role_filter = st.selectbox("Filter by Role", ["All", "client", "freelancer"])
        with col2:
            limit = st.number_input("Limit", min_value=1, max_value=100, value=10)
        
        if st.button("Load Users"):
            try:
                if role_filter == "All":
                    users = services['user'].list_users(limit)
                else:
                    users = services['user'].list_users_by_role(role_filter)
                
                if users:
                    st.dataframe(users, use_container_width=True)
                else:
                    st.info("No users found")
            except UserError as e:
                st.error(f"❌ Error: {e}")
    
    with tab3:
        st.subheader("Update or Delete User")
        user_id = st.number_input("User ID", min_value=1, step=1)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Update User**")
            with st.form("update_user"):
                new_name = st.text_input("New Name (optional)")
                new_email = st.text_input("New Email (optional)")
                new_phone = st.text_input("New Phone (optional)")
                
                if st.form_submit_button("Update User"):
                    try:
                        fields = {}
                        if new_name: fields['name'] = new_name
                        if new_email: fields['email'] = new_email
                        if new_phone: fields['phone'] = new_phone
                        
                        if fields:
                            user = services['user'].update_user(user_id, fields)
                            st.success("✅ User updated successfully!")
                            st.json(user)
                        else:
                            st.warning("No fields to update")
                    except UserError as e:
                        st.error(f"❌ Error: {e}")
        
        with col2:
            st.write("**Delete User**")
            if st.button("Delete User", type="primary"):
                try:
                    user = services['user'].remove_user(user_id)
                    st.success("✅ User deleted successfully!")
                    st.json(user)
                except UserError as e:
                    st.error(f"❌ Error: {e}")

# ========== JOBS PAGE ==========
elif page == "Jobs":
    st.header("💼 Job Management")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Create Job", "View Jobs", "Update Job", "Job Actions"])
    
    with tab1:
        st.subheader("Create New Job")
        with st.form("create_job"):
            title = st.text_input("Job Title")
            client_id = st.number_input("Client ID", min_value=1, step=1)
            budget = st.number_input("Budget", min_value=0.0, step=100.0)
            deadline = st.date_input("Deadline")
            freelancer_id = st.number_input("Freelancer ID (optional, 0 for none)", min_value=0, step=1)
            
            if st.form_submit_button("Create Job"):
                try:
                    fl_id = freelancer_id if freelancer_id > 0 else None
                    job = services['job'].create_job(
                        title, client_id, budget, str(deadline), fl_id
                    )
                    st.success(f"✅ Job created successfully! ID: {job['job_id']}")
                    st.json(job)
                except JobError as e:
                    st.error(f"❌ Error: {e}")
    
    with tab2:
        st.subheader("View Jobs")
        col1, col2 = st.columns(2)
        with col1:
            status_filter = st.selectbox("Filter by Status", ["All", "open", "assigned", "in-progress", "completed"])
        with col2:
            limit = st.number_input("Limit", min_value=1, max_value=100, value=10, key="job_limit")
        
        if st.button("Load Jobs"):
            try:
                if status_filter == "All":
                    jobs = services['job'].list_jobs(limit=limit)
                else:
                    jobs = services['job'].list_jobs(status=status_filter, limit=limit)
                
                if jobs:
                    st.dataframe(jobs, use_container_width=True)
                else:
                    st.info("No jobs found")
            except JobError as e:
                st.error(f"❌ Error: {e}")
    
    with tab3:
        st.subheader("Update Job")
        job_id = st.number_input("Job ID", min_value=1, step=1, key="update_job_id")
        
        with st.form("update_job"):
            new_title = st.text_input("New Title (optional)")
            new_budget = st.number_input("New Budget (optional, 0 to skip)", min_value=0.0, step=100.0)
            new_deadline = st.date_input("New Deadline (optional)")
            new_status = st.selectbox("New Status (optional)", ["Skip", "open", "assigned", "in-progress", "completed"])
            
            if st.form_submit_button("Update Job"):
                try:
                    fields = {}
                    from datetime import date
                    if new_title: fields['title'] = new_title
                    if new_budget > 0: fields['budget'] = new_budget
                    if new_deadline !=date.today(): fields['deadline'] = str(new_deadline)
                    if new_status != "Skip": fields['status'] = new_status
                    
                    if fields:
                        job = services['job'].update_job(job_id, fields)
                        st.success("✅ Job updated successfully!")
                        st.json(job)
                    else:
                        st.warning("No fields to update")
                except JobError as e:
                    st.error(f"❌ Error: {e}")
    
    with tab4:
        st.subheader("Job Actions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Assign Freelancer**")
            assign_job_id = st.number_input("Job ID", min_value=1, step=1, key="assign_job")
            assign_freelancer_id = st.number_input("Freelancer ID", min_value=1, step=1, key="assign_freelancer")
            
            if st.button("Assign Freelancer"):
                try:
                    job = services['job'].assign_freelancer_to_job(assign_job_id, assign_freelancer_id)
                    st.success("✅ Freelancer assigned successfully!")
                    st.json(job)
                except JobError as e:
                    st.error(f"❌ Error: {e}")
        
        with col2:
            st.write("**Delete Job**")
            delete_job_id = st.number_input("Job ID", min_value=1, step=1, key="delete_job")
            
            if st.button("Delete Job", type="primary"):
                try:
                    job = services['job'].delete_job(delete_job_id)
                    st.success("✅ Job deleted successfully!")
                    st.json(job)
                except JobError as e:
                    st.error(f"❌ Error: {e}")

# ========== BIDS PAGE ==========
elif page == "Bids":
    st.header("💰 Bid Management")
    
    tab1, tab2, tab3 = st.tabs(["Create Bid", "View Bids", "Bid Actions"])
    
    with tab1:
        st.subheader("Create New Bid")
        with st.form("create_bid"):
            job_id = st.number_input("Job ID", min_value=1, step=1)
            freelancer_id = st.number_input("Freelancer ID", min_value=1, step=1)
            amount = st.number_input("Bid Amount", min_value=0.0, step=100.0)
            message = st.text_area("Message (optional)")
            
            if st.form_submit_button("Create Bid"):
                try:
                    bid = services['bid'].create_bid(
                        job_id, freelancer_id, amount, message if message else None
                    )
                    st.success(f"✅ Bid created successfully! ID: {bid['bid_id']}")
                    st.json(bid)
                except BidError as e:
                    st.error(f"❌ Error: {e}")
    
    with tab2:
        st.subheader("View Bids")
        
        view_option = st.radio("View by:", ["All Bids", "By Job", "By Freelancer", "By Status"])
        
        if view_option == "All Bids":
            limit = st.number_input("Limit", min_value=1, max_value=100, value=10, key="all_bids_limit")
            if st.button("Load All Bids"):
                try:
                    bids = services['bid'].list_bids(limit=limit)
                    if bids:
                        st.dataframe(bids, use_container_width=True)
                    else:
                        st.info("No bids found")
                except BidError as e:
                    st.error(f"❌ Error: {e}")
        
        elif view_option == "By Job":
            job_id = st.number_input("Job ID", min_value=1, step=1, key="bids_by_job")
            if st.button("Load Bids for Job"):
                try:
                    bids = services['bid'].get_bids_by_job(job_id)
                    if bids:
                        st.dataframe(bids, use_container_width=True)
                    else:
                        st.info("No bids found for this job")
                except BidError as e:
                    st.error(f"❌ Error: {e}")
        
        elif view_option == "By Freelancer":
            freelancer_id = st.number_input("Freelancer ID", min_value=1, step=1, key="bids_by_freelancer")
            if st.button("Load Bids by Freelancer"):
                try:
                    bids = services['bid'].get_bids_by_freelancer(freelancer_id)
                    if bids:
                        st.dataframe(bids, use_container_width=True)
                    else:
                        st.info("No bids found for this freelancer")
                except BidError as e:
                    st.error(f"❌ Error: {e}")
        
        elif view_option == "By Status":
            status = st.selectbox("Status", ["pending", "accepted", "rejected"])
            limit = st.number_input("Limit", min_value=1, max_value=100, value=10, key="bids_by_status_limit")
            if st.button("Load Bids by Status"):
                try:
                    bids = services['bid'].list_bids(status=status, limit=limit)
                    if bids:
                        st.dataframe(bids, use_container_width=True)
                    else:
                        st.info(f"No {status} bids found")
                except BidError as e:
                    st.error(f"❌ Error: {e}")
    
    with tab3:
        st.subheader("Bid Actions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("**Accept Bid (Lowest Only)**")
            accept_bid_id = st.number_input("Bid ID", min_value=1, step=1, key="accept_bid")
            if st.button("Accept Bid", type="primary"):
                try:
                    bid = services['bid'].accept_bid(accept_bid_id)
                    st.success("✅ Bid accepted! All other bids rejected.")
                    st.json(bid)
                except BidError as e:
                    st.error(f"❌ Error: {e}")
        
        with col2:
            st.write("**Reject Bid**")
            reject_bid_id = st.number_input("Bid ID", min_value=1, step=1, key="reject_bid")
            if st.button("Reject Bid"):
                try:
                    bid = services['bid'].reject_bid(reject_bid_id)
                    st.success("✅ Bid rejected!")
                    st.json(bid)
                except BidError as e:
                    st.error(f"❌ Error: {e}")
        
        with col3:
            st.write("**Delete Bid**")
            delete_bid_id = st.number_input("Bid ID", min_value=1, step=1, key="delete_bid")
            if st.button("Delete Bid", type="primary"):
                try:
                    bid = services['bid'].delete_bid(delete_bid_id)
                    st.success("✅ Bid deleted!")
                    st.json(bid)
                except BidError as e:
                    st.error(f"❌ Error: {e}")

# ========== JOB STATUS PAGE ==========
elif page == "Job Status":
    st.header("📊 Job Status History")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("View Status History")
        job_id = st.number_input("Job ID", min_value=1, step=1, key="status_history_job")
        if st.button("Load Status History"):
            try:
                history = services['status'].get_status_history(job_id)
                if history:
                    st.dataframe(history, use_container_width=True)
                else:
                    st.info("No status history found")
            except JobStatusError as e:
                st.error(f"❌ Error: {e}")
    
    with col2:
        st.subheader("Latest Status")
        job_id = st.number_input("Job ID", min_value=1, step=1, key="latest_status_job")
        if st.button("Get Latest Status"):
            try:
                status = services['status'].get_latest_status(job_id)
                st.json(status)
            except JobStatusError as e:
                st.error(f"❌ Error: {e}")

# Footer
st.sidebar.markdown("---")
st.sidebar.info("💼 Freelance Platform v1.0")