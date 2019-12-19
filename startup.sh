#! /bin/bash
echo "当前执行文件......$0"

function docker_install()
{
	echo "检查Docker......"
	docker -v
    if [ $? -eq  0 ]; then
        echo "检查到Docker已安装!"
    else
    	echo "请安装docker环境..."
        echo "mac 环境 url https://download.docker.com/mac/stable/Docker.dmg"
        echo "windows 环境请访问 https://download.docker.com/win/static/stable/x86_64/"
        # curl -sSL https://get.daocloud.io/docker | sh
        # echo "安装docker环境...安装完成!"
    fi
    # 创建公用网络==bridge模式
    #docker network create starsea_network
}
function gettalib(){
    if [ ! -f "deps/ta-lib-0.4.0-src.tar.gz" ]; then
        echo "get talib"
        wget -P deps/ https://downloads.sourceforge.net/project/ta-lib/ta-lib/0.4.0/ta-lib-0.4.0-src.tar.gz
    fi
}

docker_install
gettalib
docker-compose build && docker system prune -f && docker-compose up