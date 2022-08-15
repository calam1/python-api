# create a namespace and enable istio-injection if it doesn't exist
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

# I use Kind for local k8, so copy the image over to the cluster (nodeport is the name of my cluster)
❯❯❯ kind load docker-image python-api:v1.0 --name nodeport
Image: "python-api:v1.0" with ID "sha256:f906ad26c621811e4ca0a7d4afc8c48bf6ead60c3b6c2bc7c91b85ff33087bb3" not yet present on node "nodeport-control-plane", loading...
Image: "python-api:v1.0" with ID "sha256:f906ad26c621811e4ca0a7d4afc8c48bf6ead60c3b6c2bc7c91b85ff33087bb3" not yet present on node "nodeport-worker", loading...


# docker pull the ratelimit reference app / image that envoy built
❯❯❯ docker pull envoyproxy/ratelimit:4bb32826

# I use Kind for local k8, so copy the image over to the cluster (nodeport is the name of my cluster)
❯❯❯ kind load docker-image envoyproxy/ratelimit:4bb32826 --name nodeport