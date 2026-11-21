from ai_data_agent.database import get_connection

# Connect to the existing DuckDB database
con = get_connection(read_only=True)

# Execute SQL against raw tables
result = con.execute("""
    SELECT
        (SELECT COUNT(*) FROM main.accounts) AS raw_accounts,
        (SELECT SUM(balance) FROM main.accounts) AS raw_balance,
        (SELECT COUNT(*) FROM main.transactions) AS raw_transactions,
        (SELECT SUM(amount) FROM main.transactions) AS raw_transaction_amount
""").fetchdf()

# Display results
print(result.to_string(index=False))

# Close connection
con.close()