import csv
import math

regions = {
    'ap-south-1': {'base': 80,  'amplitude': 15},
    'eu-north-1': {'base': 22,  'amplitude': 6},
    'us-east-1':  {'base': 350, 'amplitude': 50},
}

rows = []
for hour in range(48):
    for region, params in regions.items():
        cycle = math.sin(2 * math.pi * (hour % 24 - 2) / 24)
        value = round(params['base'] + params['amplitude'] * cycle, 2)
        rows.append({'hour_index': hour, 'region': region, 'gco2_per_kwh': value})

with open('data/carbon_replay.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['hour_index', 'region', 'gco2_per_kwh'])
    writer.writeheader()
    writer.writerows(rows)

print('Written', len(rows), 'rows')
print()
print(f"{'Region':<15} {'Min':>8} {'Max':>8} {'Mean':>8}")
for region in regions:
    vals = [r['gco2_per_kwh'] for r in rows if r['region'] == region]
    print(f"{region:<15} {min(vals):>8.1f} {max(vals):>8.1f} {sum(vals)/len(vals):>8.1f}")