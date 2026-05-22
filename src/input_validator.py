def get_alu_choice():
    # Keeps asking until user types exactly 'yes' or 'no'
    while True:
        choice = input("\n  Extract ALU-specific emails only? (yes/no): ").strip().lower()
        if choice in ("yes", "no"):
            return choice == "yes"
        print("  Invalid input. Please type 'yes' or 'no'.")