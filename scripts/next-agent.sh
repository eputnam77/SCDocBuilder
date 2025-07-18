#!/bin/bash
# Placeholder script to determine next Codex agent
# For now, always forward to scaffolder
NEXT_AGENT="scaffolder"
echo "NEXT_AGENT=$NEXT_AGENT" >> $GITHUB_ENV
