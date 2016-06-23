import urllib, json, time

get_ip_url = 'https://api.ipify.org?format=json'
update_dnsapi_url = 'https://dnsapi.cn/Record.Modify'
record_dnsapi_url = 'https://dnsapi.cn/Record.List'
data = {}

def get_ip():
    response = urllib.urlopen(get_ip_url)
    ip_data = json.loads(response.read())
    return ip_data['ip']
    
def bind_ip(current_ip):
    data['value'] = current_ip.encode('utf-8')
    postdata = urllib.urlencode(data)
    response = urllib.urlopen(update_dnsapi_url, postdata)
    returns = json.loads(response.read())
    code = returns['status']['code']
    if code != '1':
        print code + ": " + returns['status']['message']
        return -1
    return 0

def get_last_ip():
	para = {"login_token" : data["login_token"],
			"format" : "json",
			"domain" : data["domain"],
			"sub_domain" : data["sub_domain"]}
	postdata = urllib.urlencode(para)
	returns = json.loads(urllib.urlopen(record_dnsapi_url, postdata).read())
	print "Current Record:"
	for (k,v) in returns["records"][0].items():
	    print k.encode('utf-8') + " : " + ("None" if v is None else v.encode('utf-8'))
	return returns["records"][0]["value"]

if __name__ == "__main__":
    with open('data.json', 'r') as f:
        data = dict((k.encode('utf-8'), v.encode('utf-8')) for (k, v) in json.load(f).items())

    last_ip = get_last_ip()
    while True:
        current_ip = get_ip()
        if current_ip == last_ip:
            time.sleep(150)
            continue
        retry = 0
        while bind_ip(current_ip) != 0:
            retry = retry + 1
            if retry == 5:
                print "[ERROR]: Cannot update the record!!"
                break
