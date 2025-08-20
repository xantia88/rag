#!/bin/bash
psql -U admin -d kbase -c "CREATE EXTENSION IF NOT EXISTS vector;"
