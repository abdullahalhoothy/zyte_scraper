#!/bin/bash
# Idempotent swap setup script for VPS
# Creates a 4GB swap file if not already present

SWAPFILE="/swapfile"
SWAPSIZE="4G"

# Check if swap is already enabled
grep -q "${SWAPFILE}" /etc/fstab && swapon --show | grep -q "${SWAPFILE}"
if [ $? -eq 0 ]; then
    echo "Swap file already exists and is active."
    exit 0
fi

# Disable swap if partially configured
swapoff -a

# Remove old swapfile if present
if [ -f "${SWAPFILE}" ]; then
    rm -f "${SWAPFILE}"
fi

# Create swap file
fallocate -l ${SWAPSIZE} ${SWAPFILE} || dd if=/dev/zero of=${SWAPFILE} bs=1M count=4096
chmod 600 ${SWAPFILE}
mkswap ${SWAPFILE}

# Enable swap
swapon ${SWAPFILE}

# Add to /etc/fstab if not present
grep -q "${SWAPFILE}" /etc/fstab || echo "${SWAPFILE} none swap sw 0 0" >> /etc/fstab

echo "Swap setup complete."
