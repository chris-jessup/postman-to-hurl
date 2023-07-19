import sys, json

with open(sys.argv[1]) as fp:
    data = json.load(fp)


print(f"# Imported from {data['name']}")
for kv in data['values']:
    key, value = kv['key'], kv['value']
    print(f'export HURL_{key}="{value}"')
