#!/bin/bash
# ===== SmartCar AI-Dealer Deploy Script =====
# Script to deploy the application to production

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}=== SmartCar AI-Dealer Deploy Script ===${NC}"

# Check for production environment file
if [ ! -f .env.production ]; then
    echo -e "${RED}❌ .env.production file not found!${NC}"
    echo -e "${YELLOW}Please create .env.production with your production settings.${NC}"
    exit 1
fi

# Pull latest changes (if using git)
if [ -d ".git" ]; then
    echo -e "${YELLOW}Pulling latest changes...${NC}"
    git pull origin main || true
fi

# Build the image
echo -e "${YELLOW}Building Docker image...${NC}"
docker-compose -f docker-compose.prod.yml build

# Create backup before deploying
echo -e "${YELLOW}Creating backup...${NC}"
./scripts/backup.sh || true

# Stop old containers
echo -e "${YELLOW}Stopping old containers...${NC}"
docker-compose -f docker-compose.prod.yml down

# Start new containers
echo -e "${YELLOW}Starting new containers...${NC}"
docker-compose -f docker-compose.prod.yml up -d

# Wait for health check
echo -e "${YELLOW}Waiting for application to start...${NC}"
sleep 15

# Check health
if curl -s -f http://localhost:8501/_stcore/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Application is healthy!${NC}"
else
    echo -e "${RED}⚠️ Health check failed. Checking logs...${NC}"
    docker-compose -f docker-compose.prod.yml logs --tail=50 app
fi

echo -e "${GREEN}=== Deployment Complete ===${NC}"
echo -e "${GREEN}Application URL: http://localhost:8501${NC}"
