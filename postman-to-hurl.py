import sys, json
from textwrap import dedent

EXTRA_HEADERS = [ {"key": "Authorization", "value": "Bearer {{token}}"} ]

with open(sys.argv[1]) as fp:
    data = json.load(fp)

def get_query_string(req):
    url = req['url']
    query = []
    for kv in url.get('query', []):
        key, value = kv['key'], kv['value']
        query.append(key + ': ' + value)
    
    if query:
        query = ['[QueryStringParams]'] + query
    return '\n'.join(query)

def get_headers(req):
    ret = []
    for kv in req.get('header', []) + EXTRA_HEADERS:
        key, value = kv['key'], kv['value']
        ret.append(key + ': ' + value)
    return "\n".join(ret)

def get_tests(item):
    ret = []
    events = item.get('event', [])
    for event in events:
        ex = event.get('script', {}).get('exec', [])
        ret += ex
    return "\n".join(['# ' + line for line in ret])

def make_request(req):
    url = req['url']
    protocol = url.get('protocol')
    host = '.'.join(url['host'])
    if protocol:
        host = protocol + '://' + host
    verb_and_url = f"{req['method']} {host}/{'/'.join(url['path'])}"
    query = get_query_string(req)
    headers = get_headers(req)
    body = req.get('body', {}).get('raw', '')

    rets = 'HTTP 200'
    return '\n'.join([
        verb_and_url,
        headers,
        query,
        body,
        rets
    ])

def get_items(top, depth):
    for i, item in enumerate(top.get('item', [])):
        subs = '-'.join(['Sub']*depth)
        if subs:
            subs += '-'
        yield f"{'#'*(depth+1)} {subs}Item {i}: {item['name']}"

        if 'item' in item:
            for line in get_items(item, depth+1):
                yield line
        elif 'request' in item:
            req = item['request']
            yield make_request(req)

        if 'event' in item:
            yield get_tests(item)
        yield ''

    yield ''

print(f"# Collection: {data.get('info',{}).get('name', 'UNKNOWN')}")

for line in get_items(data, 0):
    print(line)
