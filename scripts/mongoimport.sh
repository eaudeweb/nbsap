#!/bin/bash

mongoimport -d nbsap -c goals --drop --jsonArray ../nbsap/refdata/aichi_goals.json
mongoimport -d nbsap -c indicators --drop --jsonArray ../nbsap/refdata/aichi_indicators.json
mongoimport -d nbsap -c targets --drop --jsonArray ../nbsap/refdata/aichi_targets.json
mongoimport -d nbsap -c actions --drop --jsonArray ../nbsap/refdata/be_actions.json
mongoimport -d nbsap -c objectives --drop --jsonArray ../nbsap/refdata/be_objectives.json
