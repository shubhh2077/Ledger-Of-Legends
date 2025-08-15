from bs4 import BeautifulSoup
import pandas as pd

# Load the HTML file
with open("My Activity.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "lxml")

transactions = []

# This part depends on Google Pay's HTML structure
# Find all divs or spans that contain transaction data
for item in soup.find_all("div", class_="content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1"):
    text = item.get_text(separator=" ", strip=True)

    # Example: parse date, description, and amount
    # You may need to adjust the split based on how your file looks
    if "₹" in text:  
        parts = text.split("₹")
        description = parts[0].strip()
        amount = "₹" + parts[1].split()[0]
        date = parts[1].split()[-1]  # might not be correct yet
        transactions.append([date, description, amount])

# Create DataFrame
df = pd.DataFrame(transactions, columns=["Date", "Description", "Amount"])

# Save to CSV
df.to_csv("transactions.csv", index=False, encoding="utf-8")
print("✅ Saved as transactions.csv")
