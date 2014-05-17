# Unattended ISO creator (uiso)

## Ubuntu Example
```bash
### Get the original ISO
wget http://mirror.as29550.net/releases.ubuntu.com/13.10/ubuntu-13.10-server-amd64.iso
### Remaster it
uiso-build ubuntu-13.10-server-amd64.iso ubuntu-13.10-server-unattended-amd64.iso
### Create a new virtual hard drive
qemu-img create hda 4G
### Run the installation
time kvm -enable-kvm -m 4192 -cdrom ubuntu-13.10-server-unattended-amd64.iso -vnc :1 -boot d hda
### Start the VM
kvm -enable-kvm -m 4192 -vnc :1 -boot d -net user,hostfwd=tcp::2424-:22 -net nic,model=virtio hda
```

## Developers

### Run Tests

    tox
