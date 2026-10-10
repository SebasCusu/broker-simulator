import sqlite3
import yfinance as yf
import streamlit as st

# --- PAGE CONFIGURATION (Modern & Dark by default) ---
st.set_page_config(
    page_title="Broker Simulator",
    page_icon="📈",
    layout="centered"
)

# Database initialization
conn = sqlite3.connect('broker_db', check_same_thread=False) # check_same_thread is required for Streamlit
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS user_data (
        id INTEGER PRIMARY KEY,
        balance REAL,
        shares INTEGER
    )
""")
cur.execute("INSERT OR IGNORE INTO user_data (id, balance, shares) VALUES (1, 5000, 0)")
conn.commit()

class User:
    def __init__(self, balance, shares):
        self.balance = balance
        self.shares = shares
    
    def deposit(self, deposit_amount):
        if deposit_amount <= 0:
            st.error("❌ Invalid amount")
            return False
        
        self.balance += deposit_amount
        cur.execute('UPDATE user_data SET balance = ?, shares = ? WHERE id = 1', (self.balance, self.shares))
        conn.commit()
        st.success(f"💰 Successfully deposited: ${deposit_amount:.2f} USD")
        return True
    
    def buy_shares(self, price, buy_quantity):
        total_cost = price * buy_quantity
        
        if buy_quantity <= 0:
            st.error("❌ Invalid purchase quantity")
            return False
        
        if total_cost > self.balance:
            st.error("❌ Insufficient funds")
            return False
        
        self.balance -= total_cost
        self.shares += buy_quantity
        cur.execute('UPDATE user_data SET balance = ?, shares = ? WHERE id = 1', (self.balance, self.shares))
        conn.commit()
        st.success(f"✅ Successfully bought {buy_quantity} shares!")
        return True
    
    def sell_shares(self, price, sell_quantity):
        total_cost = price * sell_quantity
        
        if sell_quantity <= 0:
            st.error("❌ Invalid sale quantity")
            return False
        
        if sell_quantity > self.shares:
            st.error("❌ Insufficient shares")
            return False
        
        self.balance += total_cost
        self.shares -= sell_quantity
        cur.execute('UPDATE user_data SET balance = ?, shares = ? WHERE id = 1', (self.balance, self.shares))
        conn.commit()
        st.success(f"⚡ Successfully sold {sell_quantity} shares!")
        return True

def main():
    # Load persistent database values
    cur.execute("SELECT balance, shares FROM user_data WHERE id = 1")
    row = cur.fetchone() 
    user1 = User(row[0], row[1])

    # Fetch dynamic real-time market data
    ticker = "AAPL"
    stock = yf.Ticker(ticker)
    price = stock.fast_info["last_price"]
    clean_price = round(price, 2)

    # --- WEB INTERFACE UI ---
    st.title("⚡ Broker Dashboard")
    
    # Live Price Banner (Modern look)
    st.info(f"📊 **Live Market Price** | {ticker}: **${clean_price} USD**")

    # Metrics Section (Llamativo y moderno)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Account Balance", value=f"${user1.balance:.2f} USD")
    with col2:
        st.metric(label="Owned Shares", value=f"{user1.shares} AAPL")
    with col3:
        portfolio_value = user1.shares * clean_price
        st.metric(label="Portfolio Value", value=f"${portfolio_value:.2f} USD", delta=f"${user1.balance + portfolio_value:.2f} Total")

    st.markdown("---")

    # Operations Tabs
    tab1, tab2, tab3 = st.tabs(["💰 Deposit Cash", "📈 Buy Shares", "📉 Sell Shares"])

    with tab1:
        st.subheader("Add Funds to your Account")
        deposit_amount = st.number_input("Enter USD amount to deposit:", min_value=0.0, step=100.0, key="dep")
        if st.button("Confirm Deposit", type="primary"):
            if user1.deposit(deposit_amount):
                st.rerun() # Refresh dashboard metrics immediately

    with tab2:
        st.subheader("Execute Buy Order")
        buy_quantity = st.number_input("How many shares do you want to buy?", min_value=0, step=1, key="buy")
        estimated_cost = buy_quantity * clean_price
        st.write(f"Estimated Total Cost: **${estimated_cost:.2f} USD**")
        if st.button("Execute BUY", type="primary"):
            if user1.buy_shares(clean_price, buy_quantity):
                st.rerun()

    with tab3:
        st.subheader("Execute Sell Order")
        sell_quantity = st.number_input("How many shares do you want to sell?", min_value=0, step=1, key="sell")
        estimated_return = sell_quantity * clean_price
        st.write(f"Estimated Total Return: **${estimated_return:.2f} USD**")
        if st.button("Execute SELL", type="secondary"):
            if user1.sell_shares(clean_price, sell_quantity):
                st.rerun()

if __name__ == "__main__":
    main()

