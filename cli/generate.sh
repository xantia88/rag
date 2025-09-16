#!/bin/bash
curl http://localhost:8080/generate/test \
-X POST \
-H 'Content-type: application/json' \
-d '{"text":"какая погода в лондоне?"}'
