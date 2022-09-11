# Private Kube

## Kubectl

### Config

| Command                                                       | Description                               |
| ------------------------------------------------------------- | ----------------------------------------- |
|`kubectl config set-context <context>`                         | set new kubernetes environment            |
|`kubectl config view`                                          | view kubectl config                       |
|`kubectl config current-context`                               | view currently used context               |
|`kubectl config set-context --current --namespace=<namespace>` | set namespace for next kube commands      |

#### View Config

`kubectl config view` shows kubectl configuration with available contexts, clusters, users, etc. Typically, the config is located in home kube directory (`$HOME/.kube/config`).
We can add connectivity to another cluster, or context by modifying the config by either using kubectl commandline, or changing it directly.
