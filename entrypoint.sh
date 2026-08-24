#!/bin/sh

if [ -z "$(ls -A /code/media 2>/dev/null)" ]; then
    echo "Media disk is empty. Copying seed media..."
    cp -r /code/media_seed/. /code/media/
else
    echo "Media disk already contains files. Skipping seed copy."
fi

exec "$@"