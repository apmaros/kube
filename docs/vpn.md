# VPN - Virtual Private Network

## How I Setup my VPN

### Get a VPN instance

We will use a self hosted VPN instance in some cloud provider. Lets use Digital Ocean [1]. It is cheap, convenient and user friendly. As this server will only proxy traffic, we can reduce resources to get the cheapest option - $5 per month.

Digital Ocean Marketplace already has a pre-configured instance with OpenVPN installed containing useful guides on how to set it up.

### Configure Server

OpenVPN server exposes a convenient UI to do most user settings. It is accessible on address `https://<IP>:943/admin/`. At the moment we don't have configure https certificates with any authority. This will cause a security warning on most browsers. Feel free to override this warning to continue.

For next step, we need to ssh into the droplet [2] we have just created and set the password. Use `passwd openvpn` to set the password for `openvpn` user.

Once, the password is setup we can login to the server and add new user. Users are edited under `User Management/User Permission` menu. Enter the username to the dialog in `Username` field and set the password under `More Settings` option.

We have created a new user 🎉 - next step is to generate a Conection Profile File. The profile contain the directives, parameters, and certificates required to establish the server-client connection [3]. This is done by using CLI on the server where is OpenVpn installed.

Scripts for generating Connection Profiles are located in `/usr/local/openvpn_as/scripts/`. To generate profile for your newly created user via UI we use following command:

```shell
./sacli  --user <user_name> GetUserlogin > client.ovpn
```

### Connect Client

Once VPN Server is created, configured and we have generated a Connection Profile file, we can connect to it with client [4]. We will copy the Connection Profile File to our localhost using SCP (`scp <user_name>@<remote_it>:<location_to_profile> .`). After importing the VPN profile, we will use login credentials that we have created on OpenVPN Server.

## References

- [1] <https://marketplace.digitalocean.com/apps/openvpn-access-server>
- [2] <https://docs.digitalocean.com/products/droplets/how-to/connect-with-ssh/>
- [3] <https://openvpn.net/vpn-server-resources/create-connection-profiles-and-connect-client-installers/>
- [4] <https://openvpn.net/vpn-client/>
