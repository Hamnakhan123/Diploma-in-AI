"""
Session 11 · Example 3: text processing with the .str accessor
--------------------------------------------------------------
Every string method works on a whole column at once via Series.str,
including regular expressions (Session 6).
Run:  python session-11_text_processing.py
"""
import pandas as pd

pd.set_option("display.width", 120)
raw = pd.DataFrame({
    "name": ["  ali KHAN", "Sana  tariq ", "BILAL ahmed", "hira shah", "Omar   Farooq"],
    "email": ["Ali.Khan@Example.COM", "sana@uni.edu.pk", "bilal@@mail", "HIRA@example.com ", "omar.f@uni.edu.pk"],
    "phone": ["0300-1234567", "+92 321 7654321", "03451234567", "021-34567890", "0333 444 5566"],
    "address": ["House 12, Block 5, Clifton, Karachi", "Flat 3B, Gulberg III, Lahore",
                "Plot 7, Gulshan-e-Iqbal, Karachi", "Street 9, Satellite Town, Quetta", "Shop 4, Saddar, Karachi"],
    "feedback": ["Great course!!", "too fast, but useful", "Loved the Python labs", "boring slides", "great labs; fast pace"],
})

df = pd.DataFrame()
df["name"] = raw["name"].str.strip().str.split().str.join(" ").str.title()       # tidy spaces + Title Case
df["first"] = df["name"].str.split().str[0]
df["email"] = raw["email"].str.strip().str.lower()
df["email_ok"] = df["email"].str.match(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")
df["domain"] = df["email"].str.extract(r"@([\w.-]+)$", expand=False)
digits = raw["phone"].str.replace(r"\D", "", regex=True)                       # keep digits only
df["mobile"] = digits.str.replace(r"^92", "0", regex=True).where(digits.str.match(r"^(92|0)3\d{9}$"))
df["mobile"] = df["mobile"].str.replace(r"^(\d{4})(\d{7})$", r"\1-\2", regex=True)
df["city"] = raw["address"].str.split(",").str[-1].str.strip()
df["area"] = raw["address"].str.split(",").str[-2].str.strip()
print(df.to_string(), "\n")

print("first names starting with a vowel:", df.loc[df["first"].str.contains(r"^[AEIOU]"), "first"].tolist())
print("name lengths:", df["name"].str.len().tolist())
print("starts with 'S' or 'O':", df.loc[df["name"].str.startswith(("S", "O")), "name"].tolist())
print("invalid emails:", df.loc[~df["email_ok"], "email"].tolist())
print("not a mobile number:", raw.loc[df["mobile"].isna(), "phone"].tolist())
print("students per city:", df["city"].value_counts().to_dict())

# Simple text analytics on feedback: normalise, tokenize, count words
words = (raw["feedback"].str.lower()
                        .str.replace(r"[^a-z\s]", " ", regex=True)
                        .str.split()
                        .explode())                                     # one word per row
stop = {"the", "but", "too"}
print("\ntop feedback words:", words[~words.isin(stop)].value_counts().head(5).to_dict())
print("mentions 'fast':", raw["feedback"].str.contains("fast").sum(), "of", len(raw))
