#!/bin/bash

mongoimport -v -d nbsap -c goals --drop --jsonArray initial/aichi_goals.json
mongoimport -v -d nbsap -c indicators --drop --jsonArray initial/aichi_indicators.json
mongoimport -v -d nbsap -c targets --drop --jsonArray initial/aichi_targets.json
mongoimport -v -d nbsap -c eu_targets --drop --jsonArray initial/eu_targets.json
