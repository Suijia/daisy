#!/bin/bash
echo "Usage: sh build.sh [online]"

if [ $# -ne 1 ]; then
    echo "Usage: sh build.sh [online]"
    exit 1
fi

env=$1
if [ ${env} != "online" ];then
    echo "Usage: sh build.sh [online]"
    exit 1
fi

SCRIPT_DIR=`dirname $0`
SERVICE=daisy
BUILD_PATH=build-${SERVICE}

cd ${SCRIPT_DIR}/..
rm ${SERVICE}.tgz

rm -rf ${BUILD_PATH}

SERVICE_PATH=${BUILD_PATH}/${SERVICE}
mkdir -p ${SERVICE_PATH}

cp -rf bin ${SERVICE_PATH}/
cp -rf conf ${SERVICE_PATH}/
cp -rf script ${SERVICE_PATH}/
cp -rf template ${SERVICE_PATH}/

cd ${BUILD_PATH}

find ${SERVICE} -name ".*" | xargs rm -rf
find ${SERVICE} -name "*.pyc" | xargs rm -rf
find ${SERVICE} -name "*.pem" | xargs rm -rf

rm -rf ${SERVICE}/.idea
rm -rf ${SERVICE}/content-design
rm -rf ${SERVICE}/logs/*
cp ${SERVICE}/conf/service_${env}.yaml ${SERVICE}/conf/service.yaml

tar -czf ${SERVICE}.tgz ${SERVICE}

mv ${SERVICE}.tgz ../
cd ../
rm -rf ${BUILD_PATH}
