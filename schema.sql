-- 1. Users
create or replace table users (
    user_id serial primary key,
    name text not null,
    email text unique not null,
    phone text,
    role text check (role in ('client', 'freelancer')) not null,
    created_at timestamp with time zone default now()
);
-- 2. Jobs
create table jobs (
    job_id serial primary key,
    title text not null,
    client_id int not null references users(user_id) on delete cascade,
    assigned_to int references users(user_id) on delete set null,  -- Freelancer assigned to job
    budget numeric(12,2) check (budget > 0),
    status text check (status in ('open', 'assigned', 'in-progress', 'completed')) 
           default 'open',
    deadline date not null,
    created_at timestamp with time zone default now()
);

-- 3. Bids
create table bids (
    bid_id serial primary key,
    job_id int not null references jobs(job_id) on delete cascade,
    freelancer_id int not null references users(user_id) on delete cascade,
    amount numeric(12,2) check (amount > 0),
    message text,
    bid_status text check (bid_status in ('pending', 'accepted', 'rejected')) default 'pending',
    created_at timestamp with time zone default now(),
    constraint unique_bid_per_freelancer unique (job_id, freelancer_id)
);

-- 4. JobStatus (Optional: history tracking)
create table job_status (
    status_id serial primary key,
    job_id int not null references jobs(job_id) on delete cascade,
    status text check (status in ('open', 'assigned','in-progress', 'completed')) not null,
    updated_at timestamp with time zone default now()
);
