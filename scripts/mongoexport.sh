#!/bin/bash

mongoexport -v -d nbsap -c goals  --out ../nbsap/bkp/aichi_goals.json
mongoexport -v -d nbsap -c indicators  --out ../nbsap/bkp/aichi_indicators.json
mongoexport -v -d nbsap -c targets  --out ../nbsap/bkp/aichi_targets.json
mongoexport -v -d nbsap -c actions  --out ../nbsap/bkp/be_actions.json
mongoexport -v -d nbsap -c objectives  --out ../nbsap/bkp/be_objectives.json
