#!/bin/sh
curl "https://wammu.eu/download/gammu/" 2>/dev/null |grep "stable release" |sed -e 's,.*stable release ,,;s,<.*,,;'

