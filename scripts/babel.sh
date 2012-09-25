#!/bin/bash

pybabel extract -F ../babel.cfg -o ../nbsap/translations/messages.pot ../nbsap
pybabel update -i ../nbsap/translations/messages.pot -d ../nbsap/translations
pybabel compile -d ../nbsap/translations
