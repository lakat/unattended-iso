# Unattended ISO creator (uiso)

## Ubuntu Example
```bash
# Get the original ISO
wget http://mirror.as29550.net/releases.ubuntu.com/13.10/ubuntu-13.10-server-amd64.iso
# Remaster it
uiso-ubuntu ubuntu-13.10-server-amd64.iso ubuntu-13.10-server-unattended-amd64.iso
# Create a new virtual hard drive
qemu-img create hda 4G
# Run the installation
time kvm -enable-kvm -m 4192 -cdrom ubuntu-13.10-server-unattended-amd64.iso -vnc :1 -boot d hda
# Start the VM
kvm -enable-kvm -m 4192 -vnc :1 -boot c -net user,hostfwd=tcp::2424-:22 -net nic,model=virtio hda
```

## Centos 6.5 Example

```bash
wget http://mirrors.ukfast.co.uk/sites/ftp.centos.org/6.5/isos/x86_64/CentOS-6.5-x86_64-minimal.iso
uiso-centos CentOS-6.5-x86_64-minimal.iso automated-CentOS-6.5-x86_64-minimal.iso
```

## Centos 5.10 Example

```bash
wget http://mirrors.ukfast.co.uk/sites/ftp.centos.org/5.10/isos/x86_64/CentOS-5.10-x86_64-bin-1of9.iso
uiso-centos CentOS-5.10-x86_64-bin-1of9.iso automated-CentOS-5.10-x86_64-bin-1of9.iso
```

## Developers

### Run Tests

    tox
