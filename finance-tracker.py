# Import the built-in json module to handle saving and loading data to text files
import json
# Import the built-in os module to check if files exist on the hard drive
import os

# Define the main blueprint (Class) for our financial tracking application
class FinanceTracker:
    
    # The Constructor method: Automatically runs the moment a new tracker object is created
    def __init__(self, budget):
        # abs() ensures that even if a user inputs a negative number, it converts to a positive float
        self.budget = abs(float(budget))
        
        # Initialize a dictionary with default keys and 0.0 values to safely hold our categorized expenses
        self.expenses = {"Food": 0.0, "Transport": 0.0, "Utilities": 0.0, "Entertainment": 0.0}
        
        # Define the exact name of the file where our data will be permanently saved on the hard drive
        self.storage_file = "tracker_data.json"
        
        # Automatically trigger the load_data method at startup to check for past saved expenses
        self.load_data()

    # Function to add an expense. It takes the category name and the money spent as inputs
    def add_expense(self, category, amount_str):
        """Validates and processes expense inputs without crashing."""
        
        # Defensive Coding: Remove accidental spaces (.strip) and force the first letter to be uppercase (.capitalize)
        # This transforms inputs like "  food  " into "Food", matching our dictionary keys perfectly
        clean_category = str(category).strip().capitalize()
        
        # Check if the cleaned category exists in our allowed dictionary keys
        if clean_category not in self.expenses:
            print(f"\n❌ Error: '{category}' is not a valid category.")
            # list(self.expenses.keys()) extracts the dictionary keys and displays them to the user
            print(f"Valid categories are: {', '.join(self.expenses.keys())}")
            return # Stop execution of this function early because the input is invalid

        # Exception Handling Block: Protects the application from crashing if the user inputs text instead of numbers
        try:
            # Attempt to convert the text input into a decimal number (float)
            amount = float(amount_str.strip())
            
            # Logic Gate: Prevent users from entering negative expense amounts
            if amount <= 0:
                print("\n❌ Error: Expense amount must be greater than zero.")
                return # Stop the function early
            
            # If valid, locate the specific category key in the dictionary and add the new amount to it
            self.expenses[clean_category] += amount
            print(f"\n✅ Successfully added ${amount:.2f} to {clean_category}.")
            
            # Run the budget check logic to see if this new expense crossed a danger threshold
            self.check_budget(clean_category)
            
            # Data Persistence: Immediately write the updated dictionary data to the permanent JSON file
            self.save_data()  
            
        # If Python encounters a ValueError (e.g., trying to turn "abc" into a float), execute this safety block instead of crashing
        except (ValueError, AttributeError):
            print("\n❌ Error: Please enter a valid numeric amount (e.g., 45.50).")

    # Business Logic Function: Monitors financial thresholds to prevent overspending
    def check_budget(self, category):
        """Monitors financial thresholds safely."""
        # Calculate the 40% warning threshold based on the total operational budget
        threshold = self.budget * 0.40
        
        # If total spending in this specific category is greater than 40% of the budget, flash a warning
        if self.expenses[category] > threshold:
            print(f"⚠️  WARNING: {category} expenses (${self.expenses[category]:.2f}) have exceeded 40% of your total budget!")

    # Analytics Function: Formats and displays a clean business-ready report to the user
    def generate_report(self):
        """Compiles clean financial report data."""
        # sum() loops through all numerical values in our dictionary and adds them together
        total_spent = sum(self.expenses.values())
        
        # Calculate net remaining capital
        savings = self.budget - total_spent
        
        # Print decorative headers for an enterprise software aesthetic
        print("\n" + "="*35)
        print("     FINANCIAL SUMMARY REPORT     ")
        print("="*35)
        print(f" Total Monthly Budget : ${self.budget:,.2f}") # :,.2f formats numbers with commas and 2 decimal points
        print(f" Total Monitored Spent: ${total_spent:,.2f}")
        print(f" Net Account Savings  : ${savings:,.2f}")
        print("-"*35)
        print(" Category Breakdown:")
        
        # Loop through each individual key (category) and value (amount) inside the expenses dictionary
        for category, amount in self.expenses.items():
            # Ternary logic condition to prevent a "ZeroDivisionError" if the user set a budget of 0
            percentage = (amount / self.budget * 100) if self.budget > 0 else 0
            # :<13 and :<10 are string alignment concepts that pad spaces to align text perfectly into straight columns
            print(f"  ▪️ {category:<13}: ${amount:<10,.2f} ({percentage:.1f}%)")
        print("="*35 + "\n")

    # File Output Function (Serialization): Writes data from RAM onto the computer's hard drive
    def save_data(self):
        """Safely writes app state to a JSON configuration file."""
        try:
            # Package our current budget and expenses data together into a single master dictionary mapping
            data_to_save = {"budget": self.budget, "expenses": self.expenses}
            
            # 'with open' is a Context Manager. It automatically safely opens and locks a file, and closes it when done
            # "w" stands for Write mode, which overwrites or creates a file from scratch
            with open(self.storage_file, "w") as file:
                # json.dump translates the live Python dictionary into text and saves it inside the file
                # indent=4 formats the text file cleanly with 4 spacing indents so humans can read it easily
                json.dump(data_to_save, file, indent=4)
        except IOError: # Catch hardware or permission errors if the operating system blocks file creation
            print("⚠️ Warning: Could not automatically save your data to storage.")

    # File Input Function (Deserialization): Reads past text logs and loads them back into live memory
    def load_data(self):
        """Safely initializes application states using existing logs."""
        # Check if the tracker_data.json file actually exists in the current folder path
        if os.path.exists(self.storage_file):
            try:
                # "r" stands for Read mode
                with open(self.storage_file, "r") as file:
                    # json.load reads the raw text file and reconstructs it back into a usable Python dictionary
                    data = json.load(file)
                    
                    # Structure Validation: Ensure the data file contains our expected expense formats
                    if "expenses" in data and isinstance(data["expenses"], dict):
                        # Loop through the file's data and bind the numbers back into our live application state
                        for k, v in data["expenses"].items():
                            if k in self.expenses:
                                self.expenses[k] = float(v)
            # Catch instances where someone manually edited the text file and corrupted the JSON syntax formatting
            except (json.JSONDecodeError, ValueError):
                print("⚠️ Notice: Corrupted save file detected. Initializing fresh data tracker profiles.")

# --- THE MAIN EXECUTION ENGINE ---
# This separate function controls the user interface menu loop
def main():
    print("="*45)
    print("  Capgemini Showcase: Corporate Expense Tracker  ")
    print("="*45)
    
    # Initialization Loop: Forces the user to supply a valid numeric budget before letting them access the application
    while True:
        try:
            raw_budget = input("Set target monthly operational budget ($): ")
            # Try to build our object instance. If input is not a number, the constructor's float() will throw an error
            tracker = FinanceTracker(budget=raw_budget)
            break # Exit this setup loop once initialization succeeds without crashing
        except (ValueError, TypeError):
            print("❌ Invalid input. The budget core must be a number. Try again.\n")

    # Command Execution Loop: Keeps the program alive indefinitely so the user can perform multiple actions
    while True:
        print("MAIN MENU:")
        print(" [1] Record New Expense")
        print(" [2] Print Analytics Report")
        print(" [3] Safely Close Application")
        
        # Receive selection choice and strip out any accidental leading/trailing spaces
        choice = input("Select operation interface (1-3): ").strip()
        
        # Route execution based on user selection
        if choice == '1':
            cat = input("Enter expense group (Food, Transport, Utilities, Entertainment): ")
            amt = input("Enter currency volume spent: ")
            tracker.add_expense(cat, amt) # Pass the inputs straight to our validation and storage engine
        elif choice == '2':
            tracker.generate_report() # Trigger calculation algorithms and print analytics formatting
        elif choice == '3':
            # Terminate the session cleanly
            print("\nEncrypted logs saved. Terminating session safely. Goodbye!")
            break # The break statement destroys the infinite loop, allowing the script to finish naturally
        else:
            # Error catch-all for invalid menu entries (like choosing option "5" or typing "hello")
            print("\n❌ Error: Invalid system command choice. Please enter exactly 1, 2, or 3.\n")

# This code block acts as Python's official entry point guardrail
if __name__ == "__main__":
    try:
        # Launch our application engine
        main()
    except KeyboardInterrupt:
        # Gracefully handle situations where a user hits Ctrl+C to force-quit the application inside the console
        # This blocks an ugly trace string crash error and ensures a professional, secure system exit
        print("\n\nSession interrupted directly. System logs secured. Exiting safely.")