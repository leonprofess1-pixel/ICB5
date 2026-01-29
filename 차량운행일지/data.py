import pandas as pd
import random

# Define the basic components based on the user's images and prompts
# Common Starts and Ends
start_garage = "차고-회사"
end_garage = "회사-차고"

# Middle routes for 3-row combinations (Extracted from image text)
middles = [
    "회사-공항-회사", "회사-역삼동-회사-삼성동", "회사-화성-회사-차고", # Note: Some might be 2-row hybrids
    "회사-신.파주-회사", "회사-양재-회사", "회사-호텔-회사", "회사-신촌-회사",
    "회사-하남-회사", "회사-물류센터-회사", "회사-갤본-신본-회사", "회사-학동-교대-회사",
    "회사-여주-회사", "회사-도곡동-회사", "회사-판교-회사", "회사-잠실-회사",
    "회사-코엑스-회사", "회사-일산-회사", "회사-마포-회사", "회사-명동-회사",
    "회사-선릉-회사", "회사-이태원-회사", "회사-가로수길-회사", "회사-압구정-회사"
]

# Specific 2-row combinations (Start -> End)
# "Garage -> Destination" and "Destination -> Garage"
# Derived from image analysis
two_row_specials = [
    ("차고-인천공항", "인천공항-메리어트-차고"),
    ("차고-롯데부산", "롯데부산-회사"), # Note: This might need a 3rd row to get to garage? Prompt says "LotteBusan-Company". If followed by Company-Garage, it's 3 rows.
    # Let's stick to the user's explicit 2-row examples or clear pairs.
    # User ex 2: "차고-도곡동...물류센터-회사" + "회사-차고"
    ("차고-도곡동-공항-회사-물류센터-회사", "회사-차고"),
    ("차고-회사-물류센터", "물류센터-회사-차고"),
    ("차고-회사", "회사-차고") # Basic
]

# Create the structured data for Excel
data = []
group_id = 1

# 1. Add 2-row specials
for start, end in two_row_specials:
    data.append({"Group_ID": group_id, "Step": 1, "Route": start})
    data.append({"Group_ID": group_id, "Step": 2, "Route": end})
    group_id += 1

# 2. Add 3-row combinations (Standard: Garage-Company -> Middle -> Company-Garage)
for mid in middles:
    # Check if 'mid' actually ends in '차고'. If so, it might be part of a 2-row set or different logic.
    # e.g. "회사-화성-회사-차고" -> This is a return trip.
    # If the middle one is "Company-Hwaseong-Company-Garage", then we effectively have:
    # Row 1: Garage-Company
    # Row 2: Company-Hwaseong-Company-Garage
    # This is a 2-row set.
    
    if "차고" in mid:
        # Treat as End of 2-row set
        data.append({"Group_ID": group_id, "Step": 1, "Route": start_garage})
        data.append({"Group_ID": group_id, "Step": 2, "Route": mid})
        group_id += 1
    else:
        # Standard 3-row set
        data.append({"Group_ID": group_id, "Step": 1, "Route": start_garage})
        data.append({"Group_ID": group_id, "Step": 2, "Route": mid})
        data.append({"Group_ID": group_id, "Step": 3, "Route": end_garage})
        group_id += 1

# Create DataFrame
df = pd.DataFrame(data)
df['Lookup_Key'] = df['Group_ID'].astype(str) + "_" + df['Step'].astype(str)

# Save to CSV
df.to_csv('dispatch_logic_table.csv', index=False)

print(f"Total Groups Created: {group_id - 1}")
print(df.head(10))