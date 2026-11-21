with customers as (
    select * from {{ ref('stg_customers') }}
),

accounts as (
    select * from {{ ref('stg_accounts') }}
),


transactions as (
    select * from {{ ref('stg_transactions') }}
),

transaction_summary as (
    select
        a.customer_id,
        count(t.transaction_id) as total_transactions,
        coalesce(sum(t.amount), 0) as total_transaction_amount
    from accounts a
    left join transactions t
        on a.account_id = t.account_id
    group by a.customer_id
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
    coalesce(a.total_balance, 0) as total_balance,
    coalesce(t.total_transactions, 0) as total_transactions,
    coalesce(t.total_transaction_amount, 0) as total_transaction_amount
from customers c
left join account_summary a
    on c.customer_id = a.customer_id
left join transaction_summary t
    on c.customer_id = t.customer_id


