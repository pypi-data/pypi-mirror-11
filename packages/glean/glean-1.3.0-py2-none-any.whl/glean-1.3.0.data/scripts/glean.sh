#!/bin/bash
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
#
# See the License for the specific language governing permissions and
# limitations under the License.

# dib-lint: disable=dibdebugtrace
set -eu
set -o pipefail

PATH=/usr/local/bin:/bin:/sbin:/usr/bin:/usr/sbin
INTERFACE=${1:-} #optional, if not specified configure all available interfaces

function config_exists() {
    local interface=$1
    if [ "$CONF_TYPE" == "netscripts" ]; then
        if [ -f "/etc/sysconfig/network-scripts/ifcfg-$interface" ]; then
            return 0
        fi
    else
        ifquery $interface >/dev/null 2>&1 && return 0 || return 1
    fi
    return 1
}


# Test to see if config-drive exists. If not, skip and assume DHCP networking
# will work becasue sanity
if blkid -t LABEL="config-2" ; then
    # Mount config drive
    mkdir -p /mnt/config
    mount -o mode=0700 $(blkid -t LABEL="config-2" | cut -d ':' -f 1) /mnt/config || true
    glean --ssh --skip-network --hostname
fi

if [ -f /usr/bin/dpkg ] ; then
    test -f /etc/ssh/ssh_host_rsa_key || dpkg-reconfigure openssh-server
fi

if [ -n "$INTERFACE" ]; then
    glean --interface $INTERFACE
else
    glean
fi
