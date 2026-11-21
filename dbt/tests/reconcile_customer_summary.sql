-- Reconcile raw account and transaction totals
-- against the customer_summary mart.

with raw_totals as (

    select
        (select count(*) from {{ source('banking', 'accounts') }})
            as total_accounts,

        (select sum(balance) from {{ source('banking', 'accounts') }})
            as total_balance,

        (select count(*) from {{ source('banking', 'transactions') }})
            as total_transactions,

        (select sum(amount) from {{ source('banking', 'transactions') }})
            as total_transaction_amount

),

mart_totals as (

    select
        sum(total_accounts) as total_accounts,
        sum(total_balance) as total_balance,
        sum(total_transactions) as total_transactions,
        sum(total_transaction_amount) as total_transaction_amount
    from {{ ref('customer_summary') }}

)

select
    r.*,
    m.*
from raw_totals r
cross join mart_totals m
where
       r.total_accounts is distinct from m.total_accounts
    or r.total_balance is distinct from m.total_balance
    or r.total_transactions is distinct from m.total_transactions
    or r.total_transaction_amount is distinct from m.total_transaction_amount