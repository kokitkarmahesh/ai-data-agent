with customers as (
    select * from {{ ref('stg_customers') }}
),

accounts as (
    select * from {{ ref('stg_accounts') }}
),

account_summary as (
    select
        customer_id,
        count(*) as total_accounts,
        sum(balance) as total_balance
    from accounts
    group by customer_id
)

select
    c.customer_id,
    c.customer_name,
    c.city,
    coalesce(a.total_accounts, 0) as total_accounts,
    coalesce(a.total_balance, 0) as total_balance
from customers c
left join account_summary a
    on c.customer_id = a.customer_id