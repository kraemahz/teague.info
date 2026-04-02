#!/bin/bash
git pull
pnpm run build-production
aws s3 sync dist s3://dist.subseq.io/teague.info
