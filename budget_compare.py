"""Temporary script to compare Google Sheet vs App budget calculations for 2025."""

# ============== GOOGLE SHEET VALUES ==============
gs_rate1, gs_rate2, gs_rate3 = 140, 170, 230
gs_zus, gs_acc = 2600, 239
gs_costs = gs_zus + gs_acc  # 2839
gs_initial = 13800
gs_additional = 3800 + 3100  # E + ZUS = 6900

gs_hours = {
    1:  (160, 0, 0),    2:  (160, 0, 0),    3:  (160, 0, 0),
    4:  (96, 144, 0),   5:  (160, 168, 0),  6:  (160, 160, 0),
    7:  (184, 184, 0),  8:  (160, 160, 0),  9:  (160, 160, 0),
    10: (96, 96, 0),    11: (144, 152, 52),  12: (160, 144, 124),
}

# SUM(B2:B19)=16810 + SUM(E2:E5)=2395 = 19205
gs_recurring_expenses = 19205

gs_onetime = {
    1: 9140, 2: 17461, 3: -11940, 4: -8337, 5: 41075, 6: 12282,
    7: 45784, 8: 35965, 9: 23357, 10: 18184, 11: 32091, 12: 25772,
}

# ============== SUPABASE (APP) VALUES ==============
app_rate1, app_rate2, app_rate3 = 148, 190, 230
app_zus, app_acc = 3300, 369
app_costs = app_zus + app_acc  # 3669
app_initial = 13800
app_additional = 3800 + 3100  # = 6900

app_hours = {
    1:  (160, 0, 0),    2:  (160, 0, 0),    3:  (160, 0, 0),
    4:  (96, 144, 0),   5:  (160, 168, 0),  6:  (160, 160, 0),
    7:  (184, 184, 0),  8:  (160, 160, 0),  9:  (160, 160, 0),
    10: (96, 96, 0),    11: (144, 152, 52),  12: (160, 144, 124),
}

app_recurring_expenses = 21763

app_onetime = {
    1: 9140, 2: 17461, 3: -11940, 4: -8337, 5: 41075, 6: 12282,
    7: 45784, 8: 35965, 9: 23357, 10: 18184, 11: 32091, 12: 25772,
}


def calc_net(r1, r2, r3, h1, h2, h3, costs):
    return (r1 * h1) * 0.88 + (r2 * h2) * 0.88 + (r3 * h3) * 0.88 - costs


print("=" * 130)
header = (
    f"{'Mo':>2} | {'GS Net':>10} {'GS Add':>8} {'GS Rec':>8} {'GS 1t':>8} "
    f"{'GS +/-':>10} {'GS Bal':>12} | "
    f"{'App Net':>10} {'App Add':>8} {'App Rec':>8} {'App 1t':>8} "
    f"{'App +/-':>10} {'App Bal':>12} | {'Diff':>10}"
)
print(header)
print("=" * 130)

gs_balance = gs_initial
app_balance = app_initial

for m in range(1, 13):
    h1, h2, h3 = gs_hours[m]
    gs_net = calc_net(gs_rate1, gs_rate2, gs_rate3, h1, h2, h3, gs_costs)
    gs_monthly_bal = gs_net + gs_additional - gs_recurring_expenses - gs_onetime[m]
    gs_balance += gs_monthly_bal

    h1a, h2a, h3a = app_hours[m]
    app_net = calc_net(app_rate1, app_rate2, app_rate3, h1a, h2a, h3a, app_costs)
    app_monthly_bal = app_net + app_additional - app_recurring_expenses - app_onetime[m]
    app_balance += app_monthly_bal

    diff = app_balance - gs_balance
    marker = " <--" if m == 3 else ""
    print(
        f"{m:>2} | {gs_net:>10.2f} {gs_additional:>8.0f} {gs_recurring_expenses:>8.0f} "
        f"{gs_onetime[m]:>8.0f} {gs_monthly_bal:>10.2f} {gs_balance:>12.2f} | "
        f"{app_net:>10.2f} {app_additional:>8.0f} {app_recurring_expenses:>8.0f} "
        f"{app_onetime[m]:>8.0f} {app_monthly_bal:>10.2f} {app_balance:>12.2f} | "
        f"{diff:>10.2f}{marker}"
    )

print()
print("SETTINGS DIFFERENCES (App vs Google Sheet):")
print(f"  Rate 1 (Stawka 1):  App={app_rate1}  GSheet={gs_rate1}  diff=+{app_rate1-gs_rate1}")
print(f"  Rate 2 (Stawka 2):  App={app_rate2}  GSheet={gs_rate2}  diff=+{app_rate2-gs_rate2}")
print(f"  Rate 3 (Stawka 3):  App={app_rate3}  GSheet={gs_rate3}  diff=0")
print(f"  ZUS:                App={app_zus}  GSheet={gs_zus}  diff=+{app_zus-gs_zus}")
print(f"  Accounting:         App={app_acc}   GSheet={gs_acc}   diff=+{app_acc-gs_acc}")
print(f"  Total costs:        App={app_costs}  GSheet={gs_costs}  diff=+{app_costs-gs_costs}")
print()
print("RECURRING EXPENSE DIFFERENCES:")
print(f'  App recurring total:    {app_recurring_expenses}')
print(f'  GSheet recurring total: {gs_recurring_expenses}')
print(f'  Diff: +{app_recurring_expenses - gs_recurring_expenses}')
print()
print('  IN APP but NOT in GSheet: "Cos" = 3000')
print('  IN GSHEET but NOT in APP: "Ubezpieczenie na zycie" = 382')
print('  IN GSHEET but NOT in APP: "Woda" = 60')
print(f'  Net recurring diff: +3000-382-60 = {3000-382-60}')
print()
print("PER-MONTH IMPACT (for months 1-3 with 160/0/0 hours):")
rate_impact = (app_rate1 - gs_rate1) * 160 * 0.88
cost_impact = app_costs - gs_costs
net_income_impact = rate_impact - cost_impact
expense_impact = app_recurring_expenses - gs_recurring_expenses
monthly_impact = net_income_impact - expense_impact
print(f"  Extra income from rate1:  +{rate_impact:.2f}")
print(f"  Extra costs (ZUS+acc):    -{cost_impact:.2f}")
print(f"  Net income impact:        +{net_income_impact:.2f} per month")
print(f"  Extra recurring expenses: +{expense_impact:.2f} per month")
print(f"  Net monthly balance diff: {monthly_impact:.2f} per month")
print(f"  After 3 months:           {3*monthly_impact:.2f}")
