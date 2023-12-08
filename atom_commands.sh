#!/usr/bin/env bash
source /${SDKMAN_DIR}/bin/sdkman-init.sh


cd /home/runner/work/src_repos/java/apollo
sdk use java 8.0.392-tem
sdk use maven 3.10.1
mvn package -DskipTests=true
cd /home/runner/work/atom-samples/atom-samples
sdk use java 20.0.2-tem
atom usages -l java -o /home/runner/work/src_repos/java/apollo/apollo.atom -s /home/runner/work/atom-samples/atom-samples/java/apollo-usages.json /home/runner/work/src_repos/java/apollo
atom reachables -l java -o /home/runner/work/src_repos/java/apollo/apollo.atom -s /home/runner/work/atom-samples/atom-samples/java/apollo-reachables.json /home/runner/work/src_repos/java/apollo


cd /home/runner/work/src_repos/java/karate
sdk use java 11.0.21-tem
sdk use maven 3.11.0
mvn package -DskipTests=true
cd /home/runner/work/atom-samples/atom-samples
sdk use java 20.0.2-tem
atom usages -l java -o /home/runner/work/src_repos/java/karate/karate.atom -s /home/runner/work/atom-samples/atom-samples/java/karate-usages.json /home/runner/work/src_repos/java/karate
atom reachables -l java -o /home/runner/work/src_repos/java/karate/karate.atom -s /home/runner/work/atom-samples/atom-samples/java/karate-reachables.json /home/runner/work/src_repos/java/karate


cd /home/runner/work/src_repos/java/piggymetrics
sdk use java 8.0.392-tem
mvn package -DskipTests=true
cd /home/runner/work/atom-samples/atom-samples
sdk use java 20.0.2-tem
atom usages -l java -o /home/runner/work/src_repos/java/piggymetrics/piggymetrics.atom -s /home/runner/work/atom-samples/atom-samples/java/piggymetrics-usages.json /home/runner/work/src_repos/java/piggymetrics
atom reachables -l java -o /home/runner/work/src_repos/java/piggymetrics/piggymetrics.atom -s /home/runner/work/atom-samples/atom-samples/java/piggymetrics-reachables.json /home/runner/work/src_repos/java/piggymetrics


cd /home/runner/work/src_repos/javascript/axios
npm install
cd /home/runner/work/atom-samples/atom-samples
atom usages -l javascript -o /home/runner/work/src_repos/javascript/axios/axios.atom -s /home/runner/work/atom-samples/atom-samples/javascript/axios-usages.json /home/runner/work/src_repos/javascript/axios
atom reachables -l javascript -o /home/runner/work/src_repos/javascript/axios/axios.atom -s /home/runner/work/atom-samples/atom-samples/javascript/axios-reachables.json /home/runner/work/src_repos/javascript/axios


cd /home/runner/work/src_repos/javascript/videojs
npm install
cd /home/runner/work/atom-samples/atom-samples
atom usages -l javascript -o /home/runner/work/src_repos/javascript/videojs/videojs.atom -s /home/runner/work/atom-samples/atom-samples/javascript/videojs-usages.json /home/runner/work/src_repos/javascript/videojs
atom reachables -l javascript -o /home/runner/work/src_repos/javascript/videojs/videojs.atom -s /home/runner/work/atom-samples/atom-samples/javascript/videojs-reachables.json /home/runner/work/src_repos/javascript/videojs


cd /home/runner/work/src_repos/javascript/sequelize
yarn install
cd /home/runner/work/atom-samples/atom-samples
atom usages -l javascript -o /home/runner/work/src_repos/javascript/sequelize/sequelize.atom -s /home/runner/work/atom-samples/atom-samples/javascript/sequelize-usages.json /home/runner/work/src_repos/javascript/sequelize
atom reachables -l javascript -o /home/runner/work/src_repos/javascript/sequelize/sequelize.atom -s /home/runner/work/atom-samples/atom-samples/javascript/sequelize-reachables.json /home/runner/work/src_repos/javascript/sequelize


cd /home/runner/work/src_repos/javascript/ava
npm install
cd /home/runner/work/atom-samples/atom-samples
atom usages -l javascript -o /home/runner/work/src_repos/javascript/ava/ava.atom -s /home/runner/work/atom-samples/atom-samples/javascript/ava-usages.json /home/runner/work/src_repos/javascript/ava
atom reachables -l javascript -o /home/runner/work/src_repos/javascript/ava/ava.atom -s /home/runner/work/atom-samples/atom-samples/javascript/ava-reachables.json /home/runner/work/src_repos/javascript/ava


cd /home/runner/work/src_repos/python/spaCy
python -m venv venv
source venv/bin/activate && pip install .
cd /home/runner/work/atom-samples/atom-samples
atom usages -l python -o /home/runner/work/src_repos/python/spaCy/spaCy.atom -s /home/runner/work/atom-samples/atom-samples/python/spaCy-usages.json /home/runner/work/src_repos/python/spaCy
atom reachables -l python -o /home/runner/work/src_repos/python/spaCy/spaCy.atom -s /home/runner/work/atom-samples/atom-samples/python/spaCy-reachables.json /home/runner/work/src_repos/python/spaCy


cd /home/runner/work/src_repos/python/scrapy
python -m venv venv
source venv/bin/activate && pip install .
cd /home/runner/work/atom-samples/atom-samples
atom usages -l python -o /home/runner/work/src_repos/python/scrapy/scrapy.atom -s /home/runner/work/atom-samples/atom-samples/python/scrapy-usages.json /home/runner/work/src_repos/python/scrapy
atom reachables -l python -o /home/runner/work/src_repos/python/scrapy/scrapy.atom -s /home/runner/work/atom-samples/atom-samples/python/scrapy-reachables.json /home/runner/work/src_repos/python/scrapy


cd /home/runner/work/src_repos/python/tinydb
python -m venv venv
source venv/bin/activate && pip install .
cd /home/runner/work/atom-samples/atom-samples
atom usages -l python -o /home/runner/work/src_repos/python/tinydb/tinydb.atom -s /home/runner/work/atom-samples/atom-samples/python/tinydb-usages.json /home/runner/work/src_repos/python/tinydb
atom reachables -l python -o /home/runner/work/src_repos/python/tinydb/tinydb.atom -s /home/runner/work/atom-samples/atom-samples/python/tinydb-reachables.json /home/runner/work/src_repos/python/tinydb


cd /home/runner/work/src_repos/python/tornado
python -m venv venv
source venv/bin/activate && pip install .
cd /home/runner/work/atom-samples/atom-samples
atom usages -l python -o /home/runner/work/src_repos/python/tornado/tornado.atom -s /home/runner/work/atom-samples/atom-samples/python/tornado-usages.json /home/runner/work/src_repos/python/tornado
atom reachables -l python -o /home/runner/work/src_repos/python/tornado/tornado.atom -s /home/runner/work/atom-samples/atom-samples/python/tornado-reachables.json /home/runner/work/src_repos/python/tornado

