# Envoy

Envoy is L7 proxy supporting an application, or service. It provides functionality such as load balancing and resiliency features like circuit breaker, timoutes, retries, observability, metrics and so on.

## Envoy Proxy filters
Request received in Envoy goes trough a set of filters. There are following filters:

**Listener filters**

Filters accesses TCP packets and can manipulate metadata of L4 connections during initial phase. This can be used for example for encryption.

**Network Filters**

Also accesses TCP packets and can be used for example as TCP Filter for sending network statistics.

**HTTP Filters**

Operates on HTTP level and can manipulate HTTP requests and responses.

## Envoy Config

Below is Envoy configuration proxying traffic to port `5050` on localhost

```yaml
static_resources:
  listeners:
  - name: listener_0
    address:
      socket_address:
        address: 0.0.0.0
        port_value: 9900
    filter_chains:
    - filters:
      - name: envoy.filters.network.http_connection_manager
        typed_config:
          "@type": type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager
          stat_prefix: edge
          http_filters:
          - name: envoy.filters.http.router
            typed_config:
              "@type": type.googleapis.com/envoy.extensions.filters.http.router.v3.Router
          route_config:
            virtual_hosts:
            - name: direct_response_service
              domains: ["*"]
              routes:
              - match:
                  prefix: "/"
                route:
                  cluster: myapp
  clusters:
  - name: myapp
    connect_timeout: 5s
    load_assignment:
      cluster_name: myapp
      endpoints:
      - lb_endpoints:
        - endpoint:
            address:
              socket_address:
                address: 127.0.0.1
                port_value: 5050
```

To expose a local Envoy admin inteface can be done by applying following configuration:

```yaml
admin:
  address:
    socket_address:
      address: 0.0.0.0
      port_value: 9901
```

# Reference

- <https://www.tetrate.io/blog/get-started-with-envoy-in-5-minutes/>
- <https://www.envoyproxy.io/docs/envoy/latest/operations/admin>
