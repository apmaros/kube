# Kube - Notes about Kubernetes

The abstractions in Kubernetes allow you to deploy containerized applications to a cluster without tying them specifically to individual machines.

A Kubernetes cluster consists of two types of resources:
- The Control Plane coordinates the cluster
- Nodes are the workers that run applications

![kubernete cluster](assets/kube-cluster.png)

**The Control Plane**

Responsible for managing the cluster. The Control Plane coordinates all activities in your cluster, such as scheduling applications, maintaining applications' desired state, scaling applications, and rolling out new updates.

**Node**

It is a VM or a physical computer that serves as a worker machine in a Kubernetes cluster.
Each node has a Kubelet, which is an agent for managing the node and communicating with the Kubernetes control plane. The node should also have tools for handling container operations, such as containerd or Docker. A Kubernetes cluster that handles production traffic should have a minimum of three nodes.

## Pod

A Pod is a Kubernetes abstraction that represents a group of one or more application containers, and some shared resources for those containers. Those resources include:
- Shared storage, as Volumes
- Networking, as a unique cluster IP address
- Information about how to run each container, such as the container image version or specific ports to use
- Every pod gets its own cluster wide ip address
- containers within a Pod can all reach each other's ports on localhost.

The containers in a Pod share an IP Address and port space, are always co-located and co-scheduled, and run in a shared context on the same Node.

Each Pod is tied to the Node where it is scheduled, and remains there until termination (according to restart policy) or deletion

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp
  labels:
    app.kubernetes.io/name: myapp
spec:
  containers:
  - name: myapp
    image: apmaros/myapp:latest
    ports:
    - containerPort: 5050
      name: http-web-svc
```

## Deployment

Deployment is used to described a desired state of the app. The state can be for example a desired number of app replicas running. A deployment controller then watches the cluster changes and attempts to maintain that state. For example if a pod is terminated, deployment schedules another pod.

A port definition in Pod can have a name. This name can be referenced in the `targetPort` attribute of a Service.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  labels:
    type: web-app
    app.kubernetes.io/name: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app.kubernetes.io/name: myapp
  template:
    metadata:
      labels:
        app.kubernetes.io/name: myapp
    spec:
      containers:
      - name: myapp
        image: apmaros/myapp:latest
        ports:
          - containerPort: 5050
            name: http-web-svc
```

## Service

A service exposes a pod as a network service. The set of Pods targeted by a Service is usually determined by a selector. In this case we use selector `app.kubernetes.io/name: myapp`

```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-svc
spec:
  selector:
    app.kubernetes.io/name: myapp
  ports:
    - name: http-web
      protocol: TCP
      port: 80
      targetPort: http-web-svc
```

## Selectors
Labels are key/value pairs that are attached to objects, such as pods

## Reference
- https://kubernetes.io/
- https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/
