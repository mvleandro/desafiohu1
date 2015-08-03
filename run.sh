#!/usr/bin/env bash

echo "Iniciando servidor MongoDB"
./vendor/mongodb/bin/mongod --dbpath "vendor/mongodb/bin/data" &

echo "Iniciando servidor Redis"
./vendor/redis/src/redis-server &

echo "Iniciando servidor REST"
python run_th.py &

echo "Abrindo o navegador"
open public/bootstrap/index.html



