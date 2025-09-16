#!/bin/bash
curl http://localhost:8080/retrieve/test \
-X POST \
-H 'Content-type: application/json' \
-d '{"text":"какая погода в лондоне?"}'
