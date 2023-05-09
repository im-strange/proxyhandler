
import socket
import threading
import requests
import pdb

# fetcher for proxies copied from hidemy.name website
# all you have to do is to copy the proxies and put it in a file

class Fetcher:
  def __init__(self):
    pass

  # filter the IPs from raw text file
  # this will return ip address and the port
  def fetch(self, filename):
    with open(filename, "r") as file:
      data = file.read().splitlines()
      data = [item.split() for item in data]
      data = [item for item in data if len(item) > 2]
      data = [item[:2] for item in data if item[0][0].isdigit()]
    return data

# this involves labeling and filtering working IPs
class Checker:
  def __init__(self):
    pass

  # raw socket object
  def socket_server(self):
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  # check single IP if working on socket connections
  def check_socket(self, proxy_host, proxy_port, store_list):
    socket_server = self.socket_server()
    try:
      socket_server.connect((proxy_host, proxy_port))
      store_list.append([proxy_host, proxy_port, "socket"])
    except socket.error: pass

  # thread for check_socket()
  def check_socket_list(self, proxy_list):
    store_list = []
    threads = []
    for proxy in proxy_list:
      thread = threading.Thread(target=self.check_socket, args=(proxy[0], int(proxy[1]), store_list))
      thread.start()
      threads.append(thread)
    for thread in threads: thread.join()
    return store_list

  # attempts make a requests (http, socket) with each IP address
  def test_single(self, proxy_host, proxy_port, store_list):
    http_proxy = {"http": f"http://{proxy_host}:{proxy_port}"}
    https_proxy = {"https": f"https://{proxy_host}:{proxy_port}"}

    try:
      response = requests.get("https://ipinfo.io/", proxies=http_proxy, timeout=5)
      store_list.append([proxy_host, proxy_port, "http"])
    except requests.exceptions.RequestException:
      pass

    try:
      response = requests.get("https://ipinfo.io/", proxies=https_proxy, timeout=5)
      store_list.append([proxy_host, proxy_port, "https"])
    except requests.exceptions.RequestException:
      pass

    try:
      socket_server = self.socket_server()
      socket_server.connect((proxy_host, proxy_port))
      store_list.append([proxy_host, proxy_port, "socket"])
    except socket.error:
      pass

  # thread for test_single()
  def test(self, proxy_list):
    valid_proxies = []
    threads = []
    for proxy in proxy_list:
      thread = threading.Thread(target=self.test_single, args=(proxy[0], int(proxy[1]), valid_proxies))
      thread.start()
      threads.append(thread)
    for thread in threads: thread.join()
    return valid_proxies

  # write the fetched IPs into a file
  def write_file(self, proxy_list, filename, mode="w"):
    with open(filename, mode) as file:
      for proxy in proxy_list:
        file.write(f"{proxy[0]:<20}{proxy[1]:<10}{proxy[2]}\n")

# this will do the job from fetching IPs from file to writing it into a file
class Processor:
  def __init__(self):
    pass

  # main function
  def process(self, file, write=False, name=None):
    fetcher = Fetcher()
    checker = Checker()

    ip_list = fetcher.fetch(file)
    working_ips = checker.test(ip_list)

    if write:
      checker.write_file(working_ips, name)
    else:
      return working_ips
