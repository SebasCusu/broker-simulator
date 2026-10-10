import sqlite3
import yfinance as yf

# Database initialization
conn = sqlite3.connect('broker_db')
cur = conn.cursor()

# Schema for storing persistent user account state
cur.execute("""
    CREATE TABLE IF NOT EXISTS user_data (
        id INTEGER PRIMARY KEY,
        balance REAL,
        shares INTEGER
    )
""")

# Seed initial balance if database is completely new
cur.execute("INSERT OR IGNORE INTO user_data (id, balance, shares) VALUES (1, 5000, 0)")
conn.commit()


class User:
    def __init__(self, balance, shares):
        self.balance = balance
        self.shares = shares
    
    def deposit(self, deposit_amount):
        if deposit_amount <= 0:
            print("Invalid amount")
            return False
        
        self.balance += deposit_amount
        print(f"Successfully deposited: ${deposit_amount:.2f}")
        
        # Sync current state to database
        cur.execute('''UPDATE user_data 
                    SET balance = ?, shares = ? 
                    WHERE id = 1''', (self.balance, self.shares))
        conn.commit()
        return True
    
    def buy_shares(self, price, buy_quantity):
        total_cost = price * buy_quantity
        
        if buy_quantity <= 0:
            print("Invalid purchase quantity")
            return False
        
        if total_cost > self.balance:
            print("Insufficient funds")
            return False
        
        # Process transaction logic
        self.balance -= total_cost
        self.shares += buy_quantity
        print(f"Successfully bought {buy_quantity} shares")
        
        # Sync transaction updates to database
        cur.execute('''UPDATE user_data 
                    SET balance = ?, shares = ? 
                    WHERE id = 1''', (self.balance, self.shares))
        conn.commit()
        return True
    
    def sell_shares(self, price, sell_quantity):
        total_cost = price * sell_quantity
        
        if sell_quantity <= 0:
            print("Invalid sale quantity")
            return False
        
        if sell_quantity > self.shares:
            print("Insufficient shares")
            return False
        
        # Process transaction logic
        self.balance += total_cost
        self.shares -= sell_quantity
        print(f"Successfully sold {sell_quantity} shares")
        
        # Sync transaction updates to database
        cur.execute('''UPDATE user_data 
                    SET balance = ?, shares = ? 
                    WHERE id = 1''', (self.balance, self.shares))
        conn.commit()
        return True


def display_menu():
    print("\n1: Deposit Cash")
    print("2: Buy Shares")
    print("3: Sell Shares")
    print("4: View Portfolio Data")
    print("5: Exit")


def main():
    # Load previously saved data to restore user session state
    cur.execute("SELECT balance, shares FROM user_data WHERE id = 1")
    row = cur.fetchone() 
    
    saved_balance = row[0]
    saved_shares = row[1]
    
    # Instantiate user with persistent database values
    user1 = User(saved_balance, saved_shares)

    # Fetch dynamic real-time market data
    ticker = "AAPL"
    stock = yf.Ticker(ticker)
    price = stock.fast_info["last_price"]
    clean_price = round(price, 2)
    
    print(f"Loaded live price for {ticker}: ${clean_price}")
    
    while True:
        try:
            display_menu()
            choice = int(input("Select an option: "))
            
            if choice == 1:
                deposit_amount = float(input("Enter deposit amount: "))
                user1.deposit(deposit_amount)
            
            elif choice == 2:
                buy_quantity = int(input("How many shares do you want to buy?: "))
                user1.buy_shares(clean_price, buy_quantity)
            
            elif choice == 3:
                sell_quantity = int(input("How many shares do you want to sell?: "))
                user1.sell_shares(clean_price, sell_quantity)
            
            elif choice == 4:
                cur.execute("SELECT * FROM user_data")
                rows = cur.fetchall()
                for row in rows:
                    print(f"\nBalance: {row[1]:.2f} USD | Shares: {row[2]}")
            
            elif choice == 5:
                print("Exiting broker simulator bye!")
                break
            
            else:
                print("Invalid option")
                
        except ValueError:
            # Trap non-integer inputs to prevent menu crashes
            print("Only integers allowed in menu selection")


if __name__ == "__main__":
    main()

# Clean up resources before exiting application
conn.close()
