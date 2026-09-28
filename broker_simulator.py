import yfinance as yf


# Represents a user in the broker simulator.
class User:

    # Initializes the user's balance and number of shares.
    def __init__(self, saldo, cantidad_acciones):
        self.cantidad_acciones = cantidad_acciones
        self.saldo = saldo

    # Withdraws money from the user's balance.
    def retirar(self, cantidad):

        # Checks if the user has enough funds.
        if cantidad > self.saldo:
            print("Insufficient Funds")
            return False

        # Checks if the withdrawal amount is valid.
        if cantidad <= 0:
            print("Invalid Withdrawal")
            return False

        # Subtracts the withdrawal amount from the balance.
        self.saldo -= cantidad

        print(f"\nWithdrawal Successful: {cantidad}")
        print(f"Balance: {self.saldo:.2f}")

        # Returns True when the operation is successful.
        return True

    # Adds money to the user's balance.
    def depositar(self, cantidad):

        # Prevents deposits of zero or negative amounts.
        if cantidad <= 0:
            print("Invalid Deposit")
            return False

        # Adds the amount to the user's balance.
        self.saldo += cantidad

        print(f"\nDeposit Successful: {cantidad}")
        print(f"Balance: {self.saldo:.2f}")

        return True

    # Buys shares using the user's available balance.
    def comprar_acciones(self, cantidad_compra, precio_accion):

        # Calculates the total cost of the purchase.
        operacion = cantidad_compra * precio_accion

        # Checks if the number of shares is valid.
        if cantidad_compra <= 0:
            print("Invalid Purchase")
            return False

        # Checks if the user has enough funds.
        if operacion > self.saldo:
            print("Insufficient Funds")
            return False

        # Subtracts the purchase cost from the balance.
        self.saldo -= operacion

        # Adds the purchased shares to the user's portfolio.
        self.cantidad_acciones += cantidad_compra

        print(f"\nSuccessfully Purchased {cantidad_compra} Shares")
        print(f"Balance: {self.saldo:.2f}")
        print(f"Total Shares: {self.cantidad_acciones}")

        return True

    # Sells shares owned by the user.
    def vender_acciones(self, cantidad_venta, precio_accion):

        # Calculates the total value of the shares being sold.
        operacion = cantidad_venta * precio_accion

        # Checks if the number of shares is valid.
        if cantidad_venta <= 0:
            print("Invalid Sale")
            return False

        # Checks if the user owns enough shares.
        if cantidad_venta > self.cantidad_acciones:
            print("You Do Not Own Enough Shares")
            return False

        # Adds the sale proceeds to the user's balance.
        self.saldo += operacion

        # Removes the sold shares from the user's portfolio.
        self.cantidad_acciones -= cantidad_venta

        print(f"\nSuccessfully Sold {cantidad_venta} Shares")
        print(f"Balance: {self.saldo:.2f}")
        print(f"Total Shares: {self.cantidad_acciones}")

        return True


# Displays the available options to the user.
def mostrar_menu():
    print("\n1: Deposit")
    print("2: Withdraw")
    print("3: Buy Shares")
    print("4: Sell Shares")
    print("5: Exit")


# Main function that runs the broker simulator.
def main():

    # Gets the current AAPL stock price using yfinance.
    precio = yf.Ticker("AAPL").fast_info["last_price"]

    # Creates a user with $5,000 and 0 shares.
    user1 = User(5000, 0)

    print("Broker Simulator")

    # Keeps the program running until the user chooses to exit.
    while True:
        mostrar_menu()

        try:
            # Gets the user's menu selection.
            decision = int(input("What do you want to do?: "))

            # Deposit money.
            if decision == 1:
                cantidad_deposito = float(
                    input("How much money do you want to deposit?: ")
                )
                user1.depositar(cantidad_deposito)

            # Withdraw money.
            elif decision == 2:
                cantidad_retiro = float(
                    input("How much money do you want to withdraw?: ")
                )
                user1.retirar(cantidad_retiro)

            # Buy shares.
            elif decision == 3:
                cantidad_compra = int(
                    input("How many shares do you want to buy?: ")
                )
                user1.comprar_acciones(cantidad_compra, precio)

            # Sell shares.
            elif decision == 4:
                cantidad_venta = int(
                    input("How many shares do you want to sell?: ")
                )
                user1.vender_acciones(cantidad_venta, precio)

            # Exit the program.
            elif decision == 5:
                break

        # Handles invalid numeric input.
        except ValueError:
            print("Invalid Option")

# Runs the main function when this file is executed directly.
if __name__ == "__main__":
    main()
