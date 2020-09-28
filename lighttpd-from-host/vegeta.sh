#!/bin/bash

CPUS=4
DURATION=10s
RATE=0
WORKERS=20

vegeta \
    -cpus ${CPUS} \
    attack \
    -duration ${DURATION} \
    -keepalive \
    -max-body 0 \
    -max-workers ${WORKERS} \
    -rate ${RATE} \
    -targets apps/nginx/targets \
    -workers ${WORKERS} \
    | vegeta report
    # | vegeta report -output results.txt
