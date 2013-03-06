#!/bin/bash

mongoimport -v -d $1 -c goals --drop --jsonArray initial/aichi_goals.json
mongoimport -v -d $1 -c indicators --drop --jsonArray initial/aichi_indicators.json
mongoimport -v -d $1 -c targets --drop --jsonArray initial/aichi_targets.json
mongoimport -v -d $1 -c eu_targets --drop --jsonArray initial/eu_targets.json
