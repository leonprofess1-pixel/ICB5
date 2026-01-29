# Refined script with Max_Step and fixed groups
data = []
group_id = 1

# Helper to add a group
def add_group(routes):
    global group_id
    max_step = len(routes)
    for i, route in enumerate(routes):
        data.append({
            "Group_ID": group_id,
            "Step": i + 1,
            "Route": route,
            "Max_Step": max_step
        })
    group_id += 1

# 1. 2-Row Sets
# Defined explicit pairs
add_group(["차고-인천공항", "인천공항-메리어트-차고"])
add_group(["차고-도곡동-공항-회사-물류센터-회사", "회사-차고"])
add_group(["차고-회사-물류센터", "물류센터-회사-차고"])
add_group(["차고-회사", "회사-차고"])

# 2. 3-Row Sets
# Special cases
add_group(["차고-롯데부산", "롯데부산-회사", "회사-차고"]) # Busan case fixed to 3 rows

# Standard Middle Routes (Sandwiched between Garage-Company and Company-Garage)
# Unless the middle route already returns to Garage
middles = [
    "회사-공항-회사", "회사-신.파주-회사", "회사-양재-회사", "회사-호텔-회사",
    "회사-신촌-회사", "회사-하남-회사", "회사-물류센터-회사", "회사-갤본-신본-회사",
    "회사-학동-교대-회사", "회사-여주-회사", "회사-도곡동-회사", "회사-판교-회사",
    "회사-잠실-회사", "회사-코엑스-회사", "회사-일산-회사", "회사-마포-회사",
    "회사-명동-회사", "회사-선릉-회사", "회사-이태원-회사", "회사-가로수길-회사",
    "회사-압구정-회사"
]

for mid in middles:
    if "차고" in mid:
        # It's a return leg, so just 2 rows: Start -> Return
        add_group([start_garage, mid])
    else:
        # Standard 3 rows: Start -> Middle -> End
        add_group([start_garage, mid, end_garage])

# Create DataFrame
df = pd.DataFrame(data)
df['Lookup_Key'] = df['Group_ID'].astype(str) + "_" + df['Step'].astype(str)

# Reorder columns for user friendly VLOOKUP
# A: Group_ID, B: Step, C: Route, D: Lookup_Key, E: Max_Step
df = df[['Group_ID', 'Step', 'Route', 'Lookup_Key', 'Max_Step']]

# Save
df.to_csv('dispatch_patterns.csv', index=False)
print(f"Total Groups: {group_id - 1}")
print(df.head())