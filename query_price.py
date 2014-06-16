import sys, json

try:
    data = json.loads(sys.argv[1])
except:
    result = {'result': 0}
    sys.exit(1)

if data[0] != '':
    if data[0] == 'a123':
        sys.exit(1)
    else:
        result = {'price': 123.12}
elif data[1] != '':
    if data[1] == 'dell pc':
        sys.exit(1)
    else:
        result = {'price': 888.00}

print json.dumps(result)
