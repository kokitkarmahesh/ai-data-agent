
from ai_data_agent.database import get_connection


def setup_database():
    con = get_connection()

    try:
        # Create customers table
        con.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                customer_id INTEGER PRIMARY KEY,
                customer_name VARCHAR,
                city VARCHAR
            )
        """)

        # Create accounts table
        con.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                account_id INTEGER PRIMARY KEY,
                customer_id INTEGER REFERENCES customers(customer_id),
                account_type VARCHAR,
                balance DECIMAL(12,2)
            )
        """)

        # Create transactions table
        con.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id INTEGER PRIMARY KEY,
                account_id INTEGER REFERENCES accounts(account_id),
                transaction_type VARCHAR,
                amount DECIMAL(12,2)
            )
        """)

        # Insert sample customers
        con.execute("""
            INSERT INTO customers
            SELECT * FROM (VALUES
                (1, 'John', 'Chicago'),
                (2, 'Sarah', 'New York'),
                (3, 'David', 'Boston')
            ) AS v(customer_id, customer_name, city)
            WHERE NOT EXISTS (
                SELECT 1 FROM customers
            )
        """)

        # Insert sample accounts
        con.execute("""
            INSERT INTO accounts
            SELECT * FROM (VALUES
                (101, 1, 'Checking', 5000.00),
                (102, 1, 'Savings', 12000.00),
                (103, 2, 'Checking', 8000.00),
                (104, 3, 'Savings', 15000.00)
            ) AS v(account_id, customer_id, account_type, balance)
            WHERE NOT EXISTS (
                SELECT 1 FROM accounts
            )
        """)

        # Insert sample transactions
        con.execute("""
            INSERT INTO transactions
            SELECT * FROM (VALUES
                (1001, 101, 'Deposit', 1000.00),
                (1002, 101, 'Withdrawal', 200.00),
                (1003, 103, 'Deposit', 3000.00),
                (1004, 104, 'Deposit', 5000.00)
            ) AS v(transaction_id, account_id, transaction_type, amount)
            WHERE NOT EXISTS (
                SELECT 1 FROM transactions
            )
        """)

        print("Banking database created successfully!")

    finally:
        con.close()


if __name__ == "__main__":
    setup_database()
