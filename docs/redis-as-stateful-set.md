# Redis as Stateful Service

Kubernetes pods are ephemeral. They can be created and terminated unexpectedly. Each new pod can be spin up on different node. This makes use of nodes inpractical for handling state.

Some services such as databases are however stateful by nature and their purpose is to maintain state. **StatefulSets** provides an API object used to managed stateful application and provides a sticky identity to pods. They can be then always scheduled on the same node and maintain the state.

This article will discuss deploying a Redis instance. First we introduce specifying its volume, then we will define a pod with consequetive Service and **StatefulSet**.

## Persistance

### Persistent Volume
First, we need to create a persistent volume that will be used to store redis data. It is a type of a resource.

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: default-pv
  labels:
    type: local
spec:
  storageClassName: manual
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: "/mnt/data"
```

Above descriptor will create a read-write volume that is persistent. It will allocate 10Gi on the path `/mnt/data` and can be accessed by a single node. In production cluster we would not use `hostPath`. We would use already provisioned a cloud storage, or NFS. It is worth to note that persisted volume can also be created by [StorageClasses](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.25/#storageclass-v1-storage-k8s-io) to setup [dynamic provissioning](https://kubernetes.io/docs/concepts/storage/dynamic-provisioning/).

### Persistent Volume Claim

Pods can acess storage using persistent volume claims. Claim can request what type of access should be granted and how much data should be allocated. It has the same [access modes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#access-modes) as the persistent volume.

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: redis
spec:
  storageClassName: manual
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 3Gi
```

Once the persistent volume claim is created, control plane looks for a persistent volume that satisfies its requirements. If it finds a sutable volume, it binds the claim to the volume.

## Redis as StatefulSet
Redis is a stateful application and its pods are not interchangable. When pod is restarted is must retain its state and start at the same node as before. StatefulSet is similar to Deployment, with difference, that in StatefulSet pods have sticky identity.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: redis
  labels:
    app: redis
spec:
  ports:
  - port: 6379
    name: redis-port
  selector:
    app: redis
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: redis
spec:
  selector:
    matchLabels:
      app: redis
  serviceName: "redis"
  replicas: 1
  minReadySeconds: 10
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
      - name: redis
        image: redis:5.0.4
        command:
          - redis-server
          - "/redis-master/redis.conf"
        env:
        - name: MASTER
          value: "true"
        ports:
        - containerPort: 6379
        resources:
          limits:
            cpu: "0.1"
        volumeMounts:
        - mountPath: /redis-master-data
          name: data
        - mountPath: /redis-master
          name: config
      volumes:
        - name: data
          persistentVolumeClaim:
            claimName: redis
        - name: config
          configMap:
            name: redis-config
            items:
            - key: redis-config
              path: redis.conf
```

We start defining a Service that will control redis networking. Note, the label `app: redis` - it is used by the StatefulSet's selector.

StatefulSet descriptor defines number of replicas with sticky identity in `spec.replicas`. More interesting is `spec.spec.volumesMounts` which is matching path `/redis-master-data` to volume `data`. This is the the path where redis will store its data. This volume is mapped to the the persistentVolumeClame create in previous section.

Its worth to note that deleteing or scaling StatefuSet, will not delete volumes associated with it. This must be done manually.

You can also notice, the `configMap` as one of specified volumes. This is how Redis maintains its configuration.

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: redis-config
data:
  redis-config: |
    maxmemory 2mb
    maxmemory-policy allkeys-lru
```

This is an example of such configuration saved in `./templates/redis/redis-cm.yaml`.

This configuration can be applied with kubectl command - `kubectl apply -f ./templates/redis/redis-cm.yaml`

## Reference
- [0] <https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/>
- [1] <https://kubernetes.io/docs/tasks/configure-pod-container/configure-persistent-volume-storage/>
- [3] <https://kubernetes.io/docs/tutorials/configuration/configure-redis-using-configmap/>

