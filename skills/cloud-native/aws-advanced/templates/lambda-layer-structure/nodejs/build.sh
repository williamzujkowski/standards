#!/bin/bash
set -e
echo "Building Node.js Lambda Layer..."
npm install --production
mkdir -p layer/nodejs
cp -r node_modules layer/nodejs/
cp -r lib layer/nodejs/
cd layer && zip -r ../layer.zip nodejs/ -q && cd ..
echo "Layer created: layer.zip"
