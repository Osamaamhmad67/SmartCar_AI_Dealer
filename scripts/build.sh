#!/bin/bash
# ===== SmartCar AI-Dealer Build Script =====
# Script to build Docker image

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}=== SmartCar AI-Dealer Build Script ===${NC}"

# Get version from argument or use 'latest'
VERSION=${1:-latest}

echo -e "${YELLOW}Building version: ${VERSION}${NC}"

# Build the Docker image
echo -e "${YELLOW}Building Docker image...${NC}"
docker build -t smartcar-ai-dealer:${VERSION} .

# Tag as latest if not already
if [ "$VERSION" != "latest" ]; then
    docker tag smartcar-ai-dealer:${VERSION} smartcar-ai-dealer:latest
fi

echo -e "${GREEN}✅ Build completed successfully!${NC}"
echo -e "${GREEN}Image: smartcar-ai-dealer:${VERSION}${NC}"

# Show image info
docker images smartcar-ai-dealer
