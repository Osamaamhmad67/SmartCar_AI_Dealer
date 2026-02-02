#!/bin/bash
# ===== SmartCar AI-Dealer Restore Script =====
# Script to restore from backup

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}=== SmartCar AI-Dealer Restore Script ===${NC}"

BACKUP_DIR="./backups"

# Check if backup name provided
if [ -z "$1" ]; then
    echo -e "${YELLOW}Available backups:${NC}"
    ls -lh ${BACKUP_DIR}/*.db 2>/dev/null || echo "No database backups found"
    echo ""
    echo -e "${YELLOW}Usage: ./restore.sh <backup_name>${NC}"
    echo -e "Example: ./restore.sh smartcar_backup_20240115_120000"
    exit 1
fi

BACKUP_NAME=$1

# Check if backup exists
if [ ! -f "${BACKUP_DIR}/${BACKUP_NAME}.db" ]; then
    echo -e "${RED}❌ Backup not found: ${BACKUP_DIR}/${BACKUP_NAME}.db${NC}"
    exit 1
fi

echo -e "${YELLOW}Restoring from: ${BACKUP_NAME}${NC}"

# Create a backup of current state
echo -e "${YELLOW}Creating backup of current state...${NC}"
./scripts/backup.sh

# Stop the application
echo -e "${YELLOW}Stopping application...${NC}"
docker-compose down 2>/dev/null || true

# Restore database
echo -e "${YELLOW}Restoring database...${NC}"
cp ${BACKUP_DIR}/${BACKUP_NAME}.db smartcar.db
echo -e "${GREEN}✅ Database restored${NC}"

# Restore invoices if exists
if [ -f "${BACKUP_DIR}/${BACKUP_NAME}_invoices.tar.gz" ]; then
    echo -e "${YELLOW}Restoring invoices...${NC}"
    tar -xzf ${BACKUP_DIR}/${BACKUP_NAME}_invoices.tar.gz
    echo -e "${GREEN}✅ Invoices restored${NC}"
fi

# Restore uploads if exists
if [ -f "${BACKUP_DIR}/${BACKUP_NAME}_uploads.tar.gz" ]; then
    echo -e "${YELLOW}Restoring uploads...${NC}"
    tar -xzf ${BACKUP_DIR}/${BACKUP_NAME}_uploads.tar.gz
    echo -e "${GREEN}✅ Uploads restored${NC}"
fi

# Start the application
echo -e "${YELLOW}Starting application...${NC}"
docker-compose up -d 2>/dev/null || true

echo -e "${GREEN}=== Restore Complete ===${NC}"
