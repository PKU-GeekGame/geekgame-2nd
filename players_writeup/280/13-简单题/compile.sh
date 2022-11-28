#!/bin/sh

set -e

[ $# -eq 1 ]

as "$1"
objcopy -O binary a.out a.bin
