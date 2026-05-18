#!/bin/bash

# Second Brain Bootstrap Script
# This script sets up the folder structure for the Second Brain + Wiki.

set -e

TARGET_DIR="${1:-.}"

echo "Creating vault structure in $TARGET_DIR..."

# Create core directories
mkdir -p "$TARGET_DIR/00 Inbox"
mkdir -p "$TARGET_DIR/01 Updates"
mkdir -p "$TARGET_DIR/02 Daily/$(date +%Y)/$(date +%m)"
mkdir -p "$TARGET_DIR/03 Meetings/Transcriptions"
mkdir -p "$TARGET_DIR/04 People"
mkdir -p "$TARGET_DIR/05 Projects"
mkdir -p "$TARGET_DIR/06 Wiki/pages"
mkdir -p "$TARGET_DIR/07 Summaries"
mkdir -p "$TARGET_DIR/_Assets"
mkdir -p "$TARGET_DIR/_Bases"
mkdir -p "$TARGET_DIR/_Templates"
mkdir -p "$TARGET_DIR/_Random"
mkdir -p "$TARGET_DIR/Archive"

# Create placeholder wiki files
cat << "EOF" > "$TARGET_DIR/06 Wiki/index.md"
---
unread: true
---

## Sources

## Entities & Concepts
EOF

cat << "EOF" > "$TARGET_DIR/06 Wiki/log.md"
---
unread: true
---

## [$(date +%Y-%m-%d)] Init
- Vault initialized.
EOF

cat << "EOF" > "$TARGET_DIR/06 Wiki/overview.md"
---
title: Overview
tags: [overview, synthesis]
sources: []
unread: true
---

## Overview

> Evolving synthesis of everything in the wiki.
EOF

# Copy templates if they exist in the repository
if [ -d "templates" ]; then
    echo "Copying templates..."
    cp -r templates/* "$TARGET_DIR/_Templates/"
fi

# Copy updates if they exist in the repository
if [ -d "01 Updates" ]; then
    echo "Copying initial 01 Updates files..."
    cp -r "01 Updates"/* "$TARGET_DIR/01 Updates/"
fi

# Copy AI Configs
echo "Copying AI instructions and skills..."
cp GEMINI.md "$TARGET_DIR/" 2>/dev/null || true
cp CLAUDE.md "$TARGET_DIR/" 2>/dev/null || true
cp AGENTS.md "$TARGET_DIR/" 2>/dev/null || true

if [ -d ".gemini" ]; then
    cp -r .gemini "$TARGET_DIR/"
fi
if [ -d ".claude" ]; then
    cp -r .claude "$TARGET_DIR/"
fi

echo "✅ Vault structure created successfully!"
echo "Next steps:"
echo "1. Open $TARGET_DIR in Obsidian."
echo "2. Check out the README.md for the capabilities and philosophy."
