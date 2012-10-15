#!/bin/bash

mongoimport -d nbsap -c goals --drop --jsonArray initial/aichi_goals.json
mongoimport -d nbsap -c indicators --drop --jsonArray initial/aichi_indicators.json
mongoimport -d nbsap -c targets --drop --jsonArray initial/aichi_targets.json
