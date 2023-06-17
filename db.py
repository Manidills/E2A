import sqlite3

# Function to create the wallets table
def create_table():
    conn = sqlite3.connect('wallets.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS wallets
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 ipfs_url TEXT,
                 name TEXT)''')
    conn.commit()
    conn.close()

# Function to insert wallet details into the wallets table
def insert_wallet(ipfs_url, name):
    conn = sqlite3.connect('wallets.db')
    c = conn.cursor()
    c.execute("INSERT INTO wallets (ipfs_url, name) VALUES (?, ?)",
              (ipfs_url, name))
    conn.commit()
    conn.close()

# Example usage
# create_table()
# insert_wallet("https://example.com/wallet1", "Wallet 1")
# insert_wallet("https://example.com/wallet2", "Wallet 2")
