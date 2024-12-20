#!/bin/bash
# Constants
EXTENSION_NAME="camera_control"

# Force script to exit if an error occurs
set -e

# Find SRCDIR from the pathname of this script
SRCDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )"/ && pwd )"

KLIPPER_PATH="${HOME}/klipper"
# Parse command line arguments to allow KLIPPER_PATH override
while getopts "k:" arg; do
    case $arg in
        k) KLIPPER_PATH=$OPTARG;;
    esac
done

# Verify conditions for the install to take place
check_preconditions()
{
    if [ "$EUID" -eq 0 ]; then
        echo "This script must not run as root"
        exit -1
    fi

    if [ "$(sudo systemctl list-units --full -all -t service --no-legend | grep -F "klipper.service")" ]; then
        echo "Klipper service found!"
    else
        echo "Klipper service not found, please install Klipper first"
        exit -1
    fi
}

# Step 2: create a symlinks to the extension files in the klippy/extras directory
link_extension()
{
    echo "Linking ${EXTENSION_NAME} to Klippy extras..."
    ln -sf ${SRCDIR}/*.py ${KLIPPER_PATH}/klippy/extras/

}

# Step 3: install dynamixel dependencies and custom wheel
install_dependencies()
{
    echo "Installing dependencies..."
    # ~/klippy-env/bin/pip install -v opencv-python
    ~/klippy-env/bin/pip install -v "${SRCDIR}/baumer_neoapi-1.4.1-cp34.cp35.cp36.cp37.cp38.cp39.cp310.cp311.cp312-none-linux_armv7l.whl"
}

# Step 4: restarting Klipper
restart_klipper()
{
    echo "Restarting Klipper..."
    sudo systemctl restart klipper
}

# Installation steps:
check_preconditions
link_extension
install_dependencies
restart_klipper
