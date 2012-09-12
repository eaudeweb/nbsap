#!/bin/bash

mongoimport -v -d nbsap -c goals --drop --jsonArray ../nbsap/bkp/aichi_goals.json
mongoimport -v -d nbsap -c indicators --drop --jsonArray ../nbsap/bkp/aichi_indicators.json
mongoimport -v -d nbsap -c targets --drop --jsonArray ../nbsap/bkp/aichi_targets.json
mongoimport -v -d nbsap -c actions --drop --jsonArray ../nbsap/bkp/be_actions.json
mongoimport -v -d nbsap -c objectives --drop --jsonArray ../nbsap/bkp/be_objectives.json
