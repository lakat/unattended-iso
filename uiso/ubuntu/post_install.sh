#!/bin/bash
cat >> /etc/network/interfaces << EOF
auto eth0
iface eth0 inet dhcp
EOF
touch /root/post_install.done
