# k8 provider is Kind, create a Kind cluster using a nodeport

## config.yml
```
apiVersion: kind.x-k8s.io/v1alpha4
kind: Cluster
nodes:
- role: control-plane
  extraPortMappings:
  - containerPort: 30000
    hostPort: 30000
    listenAddress: "0.0.0.0" # Optional, defaults to "0.0.0.0"
    protocol: tcp # Optional, defaults to tcp
- role: worker
```

# command to create a cluster using k8 1.19.16
```
❯❯❯ kind create cluster --image=kindest/node:v1.19.16 --config=config.yaml --name nodeport
```


# create a namespace and enable istio-injection if it doesn't exist
```
❯❯❯ kubectl create ns mystuff
namespace/mystuff created

❯❯❯ kubectl label namespace mystuff istio-injection=enabled --overwrite=true

namespace/mystuff labeled

❯❯❯ kubectl get namespace -L istio-injection

NAME                 STATUS   AGE    ISTIO-INJECTION
default              Active   5d5h
istio-system         Active   5d5h   disabled
kube-node-lease      Active   5d5h
kube-public          Active   5d5h
kube-system          Active   5d5h
local-path-storage   Active   5d5h
mystuff              Active   29s    enabled
❯❯❯ docker build -t python-api:v1.0 .
```

# NOTE: This repo uses the envoy external auth. So you will need to clone https://github.com/calam1/fake-authz and build the image, deploy, etc.




# I use Kind for local k8, so copy the image over to the cluster (nodeport is the name of my cluster)
```
❯❯❯ kind load docker-image python-api:v1.0 --name nodeport
Image: "python-api:v1.0" with ID "sha256:f906ad26c621811e4ca0a7d4afc8c48bf6ead60c3b6c2bc7c91b85ff33087bb3" not yet present on node "nodeport-control-plane", loading...
Image: "python-api:v1.0" with ID "sha256:f906ad26c621811e4ca0a7d4afc8c48bf6ead60c3b6c2bc7c91b85ff33087bb3" not yet present on node "nodeport-worker", loading...
```

# docker pull the ratelimit reference app / image that envoy built
```
❯❯❯ docker pull envoyproxy/ratelimit:4bb32826
```

# I use Kind for local k8, so copy the image over to the cluster (nodeport is the name of my cluster)
```
❯❯❯ kind load docker-image envoyproxy/ratelimit:4bb32826 --name nodeport
```

# Testing the rate limiter
I use https://github.com/rakyll/hey to load test


❯❯❯ hey -c 1 -n 100 -H "x-api-key:123abc" http://localhost:30000/index                                                                                                                  on branch: main

Summary:
  Total:        0.6595 secs
  Slowest:      0.0164 secs
  Fastest:      0.0049 secs
  Average:      0.0066 secs
  Requests/sec: 151.6337

  Total data:   25 bytes
  Size/request: 0 bytes

Response time histogram:
  0.005 [1]     |■
  0.006 [44]    |■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
  0.007 [34]    |■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
  0.008 [11]    |■■■■■■■■■■
  0.010 [5]     |■■■■■
  0.011 [3]     |■■■
  0.012 [0]     |
  0.013 [1]     |■
  0.014 [0]     |
  0.015 [0]     |
  0.016 [1]     |■


Latency distribution:
  10% in 0.0053 secs
  25% in 0.0057 secs
  50% in 0.0062 secs
  75% in 0.0071 secs
  90% in 0.0084 secs
  95% in 0.0095 secs
  99% in 0.0164 secs

Details (average, fastest, slowest):
  DNS+dialup:   0.0000 secs, 0.0049 secs, 0.0164 secs
  DNS-lookup:   0.0000 secs, 0.0000 secs, 0.0008 secs
  req write:    0.0000 secs, 0.0000 secs, 0.0001 secs
  resp wait:    0.0065 secs, 0.0048 secs, 0.0163 secs
  resp read:    0.0000 secs, 0.0000 secs, 0.0001 secs

Status code distribution:
  [200] 5 responses
  [429] 95 responses



❯❯❯ hey -c 1 -n 100 -H "x-api-key:123abc" http://localhost:30000/index                                                                                                                  on branch: main

Summary:
  Total:        0.6278 secs
  Slowest:      0.0167 secs
  Fastest:      0.0047 secs
  Average:      0.0063 secs
  Requests/sec: 159.2945


Response time histogram:
  0.005 [1]     |■
  0.006 [41]    |■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
  0.007 [48]    |■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
  0.008 [6]     |■■■■■
  0.010 [2]     |■■
  0.011 [1]     |■
  0.012 [0]     |
  0.013 [0]     |
  0.014 [0]     |
  0.016 [0]     |
  0.017 [1]     |■


Latency distribution:
  10% in 0.0052 secs
  25% in 0.0056 secs
  50% in 0.0061 secs
  75% in 0.0066 secs
  90% in 0.0072 secs
  95% in 0.0076 secs
  99% in 0.0167 secs

Details (average, fastest, slowest):
  DNS+dialup:   0.0000 secs, 0.0047 secs, 0.0167 secs
  DNS-lookup:   0.0000 secs, 0.0000 secs, 0.0008 secs
  req write:    0.0000 secs, 0.0000 secs, 0.0001 secs
  resp wait:    0.0062 secs, 0.0047 secs, 0.0166 secs
  resp read:    0.0000 secs, 0.0000 secs, 0.0001 secs

Status code distribution:
  [429] 100 responses


❯❯❯ hey -c 1 -n 100 -H "x-api-key:456def" http://localhost:30000/index                                                                                                                  on branch: main

Summary:
  Total:        0.6815 secs
  Slowest:      0.0293 secs
  Fastest:      0.0040 secs
  Average:      0.0068 secs
  Requests/sec: 146.7250

  Total data:   50 bytes
  Size/request: 0 bytes

Response time histogram:
  0.004 [1]     |■
  0.007 [56]    |■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
  0.009 [37]    |■■■■■■■■■■■■■■■■■■■■■■■■■■
  0.012 [3]     |■■
  0.014 [0]     |
  0.017 [0]     |
  0.019 [2]     |■
  0.022 [0]     |
  0.024 [0]     |
  0.027 [0]     |
  0.029 [1]     |■


Latency distribution:
  10% in 0.0048 secs
  25% in 0.0055 secs
  50% in 0.0063 secs
  75% in 0.0074 secs
  90% in 0.0084 secs
  95% in 0.0095 secs
  99% in 0.0293 secs

Details (average, fastest, slowest):
  DNS+dialup:   0.0001 secs, 0.0040 secs, 0.0293 secs
  DNS-lookup:   0.0001 secs, 0.0000 secs, 0.0073 secs
  req write:    0.0000 secs, 0.0000 secs, 0.0001 secs
  resp wait:    0.0066 secs, 0.0040 secs, 0.0292 secs
  resp read:    0.0000 secs, 0.0000 secs, 0.0001 secs

Status code distribution:
  [200] 10 responses
  [429] 90 responses

