"""Temporary script to update REQUIREMENTS.md - delete after use."""
import re

with open('.planning/REQUIREMENTS.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Check off all satisfied requirements
for prefix in ['ECAT-0[1-5]', 'XCAT-0[1-5]', 'NOTIF-0[1-8]', 'DASH-0[1-4]', 'SHOP-0[1245]']:
    content = re.sub(r'- \[ \] \*\*(' + prefix + r')\*\*', r'- [x] **\1**', content)

# 2. Remove SHOP-03 from active requirements
content = content.replace('- [ ] **SHOP-03**: User can check off / uncheck items on the shopping list\n', '')

# 3. Add SHOP-03 to Future Requirements
old_future = '### Notification Enhancements'
new_future = '### Shopping List Enhancements\n\n- **SHOP-03**: User can check off / uncheck items on the shopping list *(deferred from v3.0)*\n\n### Notification Enhancements'
content = content.replace(old_future, new_future)

# 4. Update traceability table - replace each row
rows = {
    'ECAT-01': ('23', 'Satisfied'), 'ECAT-02': ('23', 'Satisfied'),
    'ECAT-03': ('23', 'Satisfied'), 'ECAT-04': ('23', 'Satisfied'),
    'ECAT-05': ('23', 'Satisfied'),
    'XCAT-01': ('24', 'Satisfied'), 'XCAT-02': ('24', 'Satisfied'),
    'XCAT-03': ('24', 'Satisfied'), 'XCAT-04': ('24', 'Satisfied'),
    'XCAT-05': ('24', 'Satisfied'),
    'NOTIF-01': ('26', 'Satisfied'), 'NOTIF-02': ('26', 'Satisfied'),
    'NOTIF-03': ('26', 'Satisfied'), 'NOTIF-04': ('26', 'Satisfied'),
    'NOTIF-05': ('26', 'Satisfied'), 'NOTIF-06': ('26', 'Satisfied'),
    'NOTIF-07': ('26', 'Satisfied'), 'NOTIF-08': ('26', 'Satisfied'),
    'SHOP-01': ('25', 'Satisfied'), 'SHOP-02': ('25', 'Satisfied'),
    'SHOP-03': ('-', 'Deferred'),
    'SHOP-04': ('25', 'Satisfied'), 'SHOP-05': ('25', 'Satisfied'),
    'DASH-01': ('27', 'Satisfied'), 'DASH-02': ('27', 'Satisfied'),
    'DASH-03': ('27', 'Satisfied'), 'DASH-04': ('27', 'Satisfied'),
}

for req_id, (phase, status) in rows.items():
    old = f'| {req_id} | - | Pending |'
    new = f'| {req_id} | {phase} | {status} |'
    content = content.replace(old, new)

# 5. Update coverage summary
content = content.replace(
    '**Coverage:**\n- v3.0 requirements: 27 total\n- Mapped to phases: 0\n- Unmapped: 27',
    '**Coverage:**\n- v3.0 requirements: 27 total\n- Satisfied: 26\n- Deferred: 1 (SHOP-03)'
)

with open('.planning/REQUIREMENTS.md', 'w', encoding='utf-8') as f:
    f.write(content)

# Verify
with open('.planning/REQUIREMENTS.md', 'r', encoding='utf-8') as f:
    c = f.read()
sat = c.count('Satisfied')
deferred = 'Deferred' in c
shop03_active = '- [ ] **SHOP-03**' in c
shop03_future = 'deferred from v3.0' in c
checked = c.count('[x]')
print(f'Satisfied rows: {sat}')
print(f'Deferred present: {deferred}')
print(f'SHOP-03 still in active: {shop03_active}')
print(f'SHOP-03 in future: {shop03_future}')
print(f'Checked requirements: {checked}')
