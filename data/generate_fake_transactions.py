import pandas as pd
import random
from datetime import datetime, timedelta
from pathlib import Path

# Fake names list
names = [
    "John Doe", "Jane Smith", "Negan", "Rick Grimes", "Dexter Morgan", "Walter White",
    "Tony Stark", "Bruce Wayne", "Lara Croft", "Ellen Ripley", "Michael Scott",
    "Jim Halpert", "Pam Beesly", "Dwight Schrute", "Saul Goodman", "Jesse Pinkman",
    "Sheldon Cooper", "Leonard Hofstadter", "Penny Hofstadter", "Howard Wolowitz"
]

payment_methods = ["UPI", "Card", "Wallet"]
statuses = ["Success", "Pending", "Failed"]


def generate_transactions(num_rows: int = 500, start: datetime = datetime(2025, 1, 1)) -> pd.DataFrame:
    rows = []
    for i in range(1, num_rows + 1):
        name = random.choice(names)
        date = start + timedelta(days=random.randint(0, 180))
        amount = round(random.uniform(10, 5000), 2)
        payment_method = random.choice(payment_methods)
        upi_id = f"{name.lower().replace(' ', '')}@upi" if payment_method == "UPI" else "NA"
        phone = "9999999999"
        email = f"user{i}@example.com"
        status = random.choice(statuses)
        txn_id = f"TXN{i:05d}"
        rows.append([
            txn_id,
            name,
            date.strftime("%Y-%m-%d"),
            amount,
            payment_method,
            upi_id,
            phone,
            email,
            status,
        ])

    df_fake = pd.DataFrame(
        rows,
        columns=[
            "Transaction ID",
            "Name",
            "Date",
            "Amount",
            "Payment Method",
            "UPI ID",
            "Phone",
            "Email",
            "Status",
        ],
    )
    return df_fake


def main():
    df = generate_transactions()
    out_path = Path(__file__).parent / "transactions.csv"
    df.to_csv(out_path, index=False)
    print("✅ data/transactions.csv created successfully")


if __name__ == "__main__":
    main()


