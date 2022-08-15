# kubectl Cheatsheet

get pods for ns<br>
`kubectl get pods -n <namespace>`

inspect, start stop service<br>
`kubectl get deployments -n <namespace>`

change cluster<br>
`kubectl config use-context <cluster>`

get logs<br>
`kubectl -n <namespace> logs <pod-instance> <pod-name> -f`

port forward<br>
`kubectl port-forward pods/<pod> -n price-advice <port>`

describe pod<br>
`kubectl -n <namespace> get pod <pod-instance> --output=yaml | less`

copy to/from pod<br>
`kubectl cp  <namespace>/<pod>:<path> <local-path>`

ssh to container<br>
`kubectl -n <namespace> exec -it <pod> -- <cmd>`

## Tip

Alias `kubectl` to `k`, it will make typing much faster

## References

- https://kubernetes.io/docs/reference/kubectl/cheatsheet/#kubectl-context-and-configuration
