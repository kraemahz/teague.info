#!/bin/bash
git pull
npm run build
aws s3 sync dist s3://dist.subseq.io/teague.info
