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
  - where `proxy_list` is a list of proxies with port. Example:

```py
 proxy_list = [
   ["127.0.0.1", 1234],
   ["127.0.0.1", 1212]
 ]  
```

