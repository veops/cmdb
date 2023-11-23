#!/bin/bash

cmdb_dir="/home/$(whoami)/apps"

check_docker() {
    if [ -x "$(command -v docker)" ]; then
        if pgrep "dockerd" >/dev/null; then
            :
        else
            echo "error: please install docker firstly"
            exit 1
        fi
    else
        echo "error: please install docker firstly"
        exit 1
    fi
}

check_docker_compose() {
    if [ -x "$(command -v docker-compose)" ]; then
        :
    else
        echo "error: please install docker-compose firstly"
        exit 1
    fi
}

clone_repo() {
    local repo_url=$1
    git clone $repo_url || {
        echo "error: failed to clone $repo_url"
        exit 1
    }
}

change_directory() {
    local new_dir=$1
    if ! mkdir -p "$new_dir"; then
        echo "error: failed to create directory $new_dir"
        exit 1
    fi
    cd "$new_dir" || exit 1
}

install_service() {
    check_docker
    check_docker_compose

    echo ""
    echo "Installing the service $1..."
    current_path=$(pwd)
    change_directory "$cmdb_dir"

    if [ -d "${cmdb_dir}/cmdb" ]; then
	echo "directory ${cmdb_dir}/cmdb already exist"
        exit 1
    fi

    clone_repo "https://githubfast.com/veops/cmdb.git" || clone_repo "https://github.com/veops/cmdb.git"
    cd ${cmdb_dir}/cmdb || exit 1
    docker-compose pull
    if [ $? -eq 0 ];then
        echo "successfully install package in directory: ${cmdb_dir}/cmdb"
    fi
    cd $current_path || exit 1
}

start_service() {
    check_docker
    check_docker_compose

    echo "Starting the service $1..."
    current_path=$(pwd)
    cd ${cmdb_dir}/cmdb
    docker-compose up -d
    cd $current_path
}

pause_service() {
    check_docker
    check_docker_compose

    case $2 in
    "" | cmdb-api | cmdb-ui | cmdb-db | cmdb-cache)
        echo "Pausing the service ..."

        current_path=$(pwd)

        cd ${cmdb_dir}/cmdb || exit 1
        docker-compose stop $2

        cd $current_path || exit 1
        ;;
    *)
        echo "Please input invalid service name: [cmdb-api|cmdb-ui|cmdb-db|cmdb-cache]"
        ;;
    esac
}

delete_service() {
    check_docker
    check_docker_compose

    echo "Deleting the service ..."
    current_path=$(pwd)
    cd ${cmdb_dir}/cmdb || exit 1
    docker-compose down
    cd $current_path || exit 1
}

status_service() {
    check_docker
    check_docker_compose

    current_path=$(pwd)
    cd ${cmdb_dir}/cmdb || exit 1
    docker-compose ps
    cd $current_path || exit 1

}

uninstall_service() {
    check_docker
    check_docker_compose

    read -p "Are you sure to uninstall the all the application and data? y/n:" input
    if [ $input = "y" ]; then
        echo "Uninstalling the service $1..."
        current_path=$(pwd)
        cd ${cmdb_dir}/cmdb || exit 1
        docker-compose down -v
        cd $current_path || exit 1
    fi
}

echo "Welcome to the CMDB service management script!"
echo ""

case $1 in
install)
    install_service $2
    ;;
start)
    start_service $2
    ;;
status)
    status_service $2
    ;;
pause)
    pause_service $2
    ;;
delete)
    delete_service $2
    ;;
uninstall)
    uninstall_service $2
    ;;
*)
    echo "Usage: $0 [install|start|pause|uninstall]"
    echo "install       Used to install the application"
    echo "start         Used to start the application"
    echo "status        Used to show status of the application"
    echo "pause         Used to pause the application"
    echo "delete        Used to delete the application"
    echo "uninstall     Used to uninstall the application, include all data"
    ;;
esac
