#!/bin/bash
curl http://localhost:8080/update/test \
-X POST \
-H 'Content-type: application/json' \
-d '{
   "path":"document1.txt",
   "metadata": {
               "parameter1": "value1",
               "paramneter2": "value2"
               }
   }'
