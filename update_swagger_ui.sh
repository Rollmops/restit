#!/bin/bash

VERSION=${1-3.51.1}
mkdir -p restit/resource/swagger/
rm -f restit/resource/swagger/*

wget -c https://github.com/swagger-api/swagger-ui/archive/refs/tags/v${VERSION}.tar.gz -O - | tar -xz

mv swagger-ui-${VERSION}/dist/* restit/resource/swagger/

rm -fr swagger-ui-${VERSION}/

sed -i 's/url: .\+/url: "swagger.json",/' restit/resource/swagger/index.html
