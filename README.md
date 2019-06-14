# OpenVPN Socks Client Manager

On Demand OpenVPN for use as SideCar.
Use if the OpenVPN is only needed sporadically.

    GET /activate   Open VPN for 5 minutes (or whatever your client inactivity period is for)
    GET /status     Get status of VPN

Once "activated" port 8081 (Socks5) will be available



## Inspiration/Alternatives

* https://github.com/ohpe/socks-my-vpn (yeah cool name~)
* https://github.com/mook/docker-openvpn-client-socks