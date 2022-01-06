import csv
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import random

ua = UserAgent()  # From here we generate a random user agent
proxies = []  # Will contain proxies [ip, port]

# Main function


def main():
    # Retrieve latest proxies
    proxies_req = Request('https://www.sslproxies.org/')
    proxies_req.add_header('User-Agent', ua.random)
    proxies_doc = urlopen(proxies_req).read().decode('utf8')

    soup = BeautifulSoup(proxies_doc, 'html.parser')
    proxies_table = soup.find(
        "table", {"class": 'table table-striped table-bordered'})

    # Save proxies in the array
    for row in proxies_table.tbody.find_all('tr'):
        proxies.append({
            'ip':   row.find_all('td')[0].string,
            'port': row.find_all('td')[1].string
        })

    # Choose a random proxy
    proxy_index = random_proxy()
    proxy = proxies[proxy_index]

    for n in range(1, 100):
        req = Request('http://icanhazip.com')
        req.set_proxy(proxy['ip'] + ':' + proxy['port'], 'http')

        # Every 10 requests, generate a new proxy
        if n % 10 == 0:
            proxy_index = random_proxy()
            proxy = proxies[proxy_index]

        # Make the call
        try:
            my_ip = urlopen(req, timeout=5.0).read().decode('utf8')
            print('#' + str(n) + ': ' + my_ip)
        except:  # If error, delete this proxy and find another one
            del proxies[proxy_index]
            print('Proxy ' + proxy['ip'] + ':' + proxy['port'] + ' deleted.')
            proxy_index = random_proxy()
            proxy = proxies[proxy_index]

    keys = proxies[0].keys()
    with open('proxy_list.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(proxies)

# Retrieve a random index proxy (we need the index to delete it if not working)


def random_proxy():
    return random.randint(0, len(proxies) - 1)


if __name__ == '__main__':
    main()
