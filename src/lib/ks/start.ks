#platform=x86, AMD64, or Intel EM64T
#version=DEVEL
%pre

# eval options
set -- `cat /proc/cmdline`

for I in $*; do case "$I" in *=*) eval $I;; esac; done

# set encrypted fs
if [ ! -z $fspassword ]; then
   echo "--encrypted --passphrase=$fspassword" > /tmp/root-encrypt
fi


if [ "x$repo" != "x" ]; then
    echo "REPO='$repo/extras'" > /tmp/repo
fi
%end

# Use text mode install
text
# Install OS instead of upgrade
install
# Firewall configuration
firewall --enabled --ssh
# Use CDROM installation media
cdrom
# Network information
%include /tmp/network-include
# Root password
%include /tmp/password-include
# System authorization information
auth  --useshadow  --passalgo=sha512
# System keyboard
%include /tmp/keyboard-include
# System language
%include /tmp/lang-include
# SELinux configuration
selinux --permissive
# Do not configure the X Window System
skipx
# Installation logging level
logging --level=debug
# System timezone
%include /tmp/timezone-include
# System bootloader configuration
%include /tmp/bootloader-include
# Clear the Master Boot Record
zerombr
# Partition clearing information
clearpart --all  
# Disk partitioning information
%include /tmp/part-include
# LVM
%include /tmp/rootfs-include
# Reboot and eject CD
reboot --eject

%post --nochroot --interpreter /bin/bash
exec 1>/mnt/sysimage/root/kickstart-stage1.log 2>&1

if [ -f /tmp/raid ]; then
    cat /tmp/raid >> /mnt/sysimage/etc/mdadm.conf
fi

if [ -f /tmp/repo ]; then
    cp /tmp/repo /mnt/sysimage/root/repo
else
    echo "Copying extras repo to /root.."
    cp -r /mnt/source/extras /mnt/sysimage/root
fi
%end

%post --interpreter /bin/bash
exec 1>/root/kickstart-stage2.log 2>&1

TMPEXTRAS_DIR=/tmp/yumextras
EXTRAS_DIR=/root/extras

if [ -f /root/repo ]; then
   . /root/repo
else
   REPO="file://$EXTRAS_DIR"
fi

mkdir -p ${TMPEXTRAS_DIR}

echo "Initializing temporary yum repository ($REPO)..."
cat > ${TMPEXTRAS_DIR}/yumextras.conf << EOF
[main]
cachedir=${TMPEXTRAS_DIR}/cache
logfile=${TMPEXTRAS_DIR}/yum.log
debuglevel=2
reposdir=/dev/null
retries=20
obsoletes=1
gpgcheck=0
assumeyes=1
metadata_expire=never
mirrorlist_expire=never

[extras]
name=extras
baseurl=$REPO
enabled=1

EOF

echo "Installing nethserver-iso package group..."
yum -c ${TMPEXTRAS_DIR}/yumextras.conf -y groupinstall nethserver-iso

echo "Adjusting services..."

/sbin/chkconfig iscsi off
/sbin/chkconfig iscsid off
/sbin/chkconfig netfs off

echo "Enabling first-boot..."
touch /var/spool/first-boot

echo "Removing installation files..."
rm -rfv ${TMPEXTRAS_DIR} ${EXTRAS_DIR}

%end

%pre --log=/tmp/installer.log

cat <<EOF > /tmp/installer

