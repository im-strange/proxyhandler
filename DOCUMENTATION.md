# Documentation 

Proxyhandler has the following classes
- Fetcher 
- Checker 
- Processor 

## Fetcher 
`Fetcher` class has only one main function `fetch()`. 
What it does is fetching proxies from a file and return a list 
object that has the IP address and a port.
 
- `fetch(file)` 
  - where `file` can be file or path of the file.

## Checker 
On the other hand, `Checker` class the following function.

- `check_socket_list(proxy_list)`
  - It checks list of proxies if it accessible for `socket` connection.
  - It will return a new list with label socket in the end:
 
```py
[["127.0.0.1", 1212, "socket"],
 ["127.0.0.1", 1234, "socket"]
]
```

  - Where `proxy_list` is a list of proxies with port. Example:

```py
 proxy_list = [
   ["127.0.0.1", 1234],
   ["127.0.0.1", 1212]
 ]  
```

- `test(proxy_list)`
  - It test the proxy servers for various connections and return a new list with label: http, https, and socket.

- `write_file(proxy_list, filename)`
  - It writes the `proxy_list` into a new file.

## Processor 
Class `Processor` has one main function `process` which does the job from fetching IPs up to writing it in a new file.

- `process(file, write=boolean, name)` 
  - `file` is the file of raw proxies.
  - `write` creates a new file if true, else, returns a list.

## Demo 
For instance, I have a file named `sample-proxies.txt` that has raw proxies that I copied from <a href= "https://hidemy.name/en/proxy-list">hidemy.name</a> website.

```txt
116.99.36.21	5301	Vietnam Hanoi	
1260 ms

SOCKS4, SOCKS5	High	2 minutes
45.8.106.97	80	Curacao	
80 ms

HTTP	no	2 minutes
203.24.102.122	80	Virgin Islands, British	
100 ms

HTTP	no	2 minutes
172.64.193.2	80	United States	
20 ms

HTTP	no	2 minutes
141.101.120.74	80		
20 ms

HTTP	no	2 minutes
141.101.122.224	80		
40 ms

HTTP	no	2 minutes
45.131.6.160	80	Netherlands	
40 ms

HTTP	no	2 minutes
185.170.166.93	80	United Kingdom	
140 ms

HTTP	no	2 minutes
172.67.182.103	80	United States	
200 ms

HTTP	no	2 minutes
172.67.3.65	80	United States	
200 ms

HTTP	no	2 minutes
172.67.180.50	80	United States	
200 ms

HTTP	no	2 minutes
172.67.181.109	80	United States

```

<br>
I want to filter the file, and get the proxies address and port 

```py
from proxyhandler import Fetcher 

fetcher = Fetcher()
proxy_list = fetcher.fetch("sample-proxies.txt")

print(proxy_list)

```
<br>

The code above will print this output:

```
[['116.99.36.21', '5301'],
 ['45.8.106.97', '80'],
 ['203.24.102.122', '80'],
 ['172.64.193.2', '80'],
 ['45.131.6.160', '80'],
 ['185.170.166.93', '80'],
 ['172.67.182.103', '80'],
 ['172.67.3.65', '80'],
 ['172.67.180.50', '80'],
 ['172.67.181.109', '80']]
```

<br>

Now, I want to filter the addresses with `check_socket_list()`

```py
from proxyhandler import Fetcher, Checker

fetcher = Fetcher()
checker = Checker()

proxy_list = fetcher.fetch("sample-proxies.txt")
socket_proxies = checker.check_socket_list(proxy_list)

print(socket_proxies)
```

In the code above, we import `Checker` class
and call the `check_socket_list` to filter the proxies and return `socket_proxies`:

```
[['203.24.102.122', 80, 'socket'],
 ['45.131.6.160', 80, 'socket'],
 ['185.170.166.93', 80, 'socket'],
 ['45.8.106.97', 80, 'socket'],
 ['172.64.193.2', 80, 'socket'],
 ['172.67.182.103', 80, 'socket'],
 ['172.67.3.65', 80, 'socket'],
 ['172.67.181.109', 80, 'socket'],
 ['172.67.180.50', 80, 'socket']]
```
<br>

Now, I want to filter `proxy_list` with `test` function from `Checker` class
which will return new list of proxies with connection labels.

```py
...
filtered_proxies = checker.test(proxy_list)
...
```
<br>

The code above will return new list object:

```
[['172.67.182.103', 80, 'http'],
 ['172.67.180.50', 80, 'http'],
 ['185.170.166.93', 80, 'http'],
 ['172.64.193.2', 80, 'http'],
 ['45.8.106.97', 80, 'http'],
 ['45.131.6.160', 80, 'http'],
 ['172.67.3.65', 80, 'http'],
 ['172.67.181.109', 80, 'http'],
 ['203.24.102.122', 80, 'http'],
 ['116.99.36.21', 5301, 'http'],
 ['172.67.182.103', 80, 'socket'],
 ['185.170.166.93', 80, 'socket'],
 ['45.8.106.97', 80, 'socket'],
 ['172.67.180.50', 80, 'socket'],
 ['45.131.6.160', 80, 'socket'],
 ['172.67.3.65', 80, 'socket'],
 ['172.64.193.2', 80, 'socket'],
 ['203.24.102.122', 80, 'socket'],
 ['172.67.181.109', 80, 'socket']]
```

<br>

Some host can have multiple labels. This means you can
use the proxy for both connections.
<br>

Now, I want to call the `Processor.process` function
to process `sample-proxies.txt` and create a new file with filtered proxies.

```py
from proxyhandler import Processor

processor = Processor()
processor.process(file="sample-proxies.txt", write=True, name="filtered-proxies.txt")
```

<br>

The code above will make `filtered-proxies.txt` file containing filtered proxies.
