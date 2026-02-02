#!/bin/bash
# ===== SmartCar AI-Dealer Backup Script =====
# Script to create database and data backups

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}=== SmartCar AI-Dealer Backup Script ===${NC}"

# Configuration
BACKUP_DIR="./backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="smartcar_backup_${TIMESTAMP}"

# Create backup directory
mkdir -p ${BACKUP_DIR}

echo -e "${YELLOW}Creating backup: ${BACKUP_NAME}${NC}"

# Backup database
if [ -f "smartcar.db" ]; then
    echo -e "${YELLOW}Backing up database...${NC}"
    cp smartcar.db ${BACKUP_DIR}/${BACKUP_NAME}.db
    echo -e "${GREEN}✅ Database backed up${NC}"
fi

# Backup invoices
if [ -d "invoices" ] && [ "$(ls -A invoices 2>/dev/null)" ]; then
    echo -e "${YELLOW}Backing up invoices...${NC}"
    tar -czf ${BACKUP_DIR}/${BACKUP_NAME}_invoices.tar.gz invoices/
    echo -e "${GREEN}✅ Invoices backed up${NC}"
fi

# Backup uploads
if [ -d "uploads" ] && [ "$(ls -A uploads 2>/dev/null)" ]; then
    echo -e "${YELLOW}Backing up uploads...${NC}"
    tar -czf ${BACKUP_DIR}/${BACKUP_NAME}_uploads.tar.gz uploads/
    echo -e "${GREEN}✅ Uploads backed up${NC}"
fi

# Cleanup old backups (keep last 10)
echo -e "${YELLOW}Cleaning old backups...${NC}"
cd ${BACKUP_DIR}
ls -t *.db 2>/dev/null | tail -n +11 | xargs -r rm --
ls -t *_invoices.tar.gz 2>/dev/null | tail -n +11 | xargs -r rm --
ls -t *_uploads.tar.gz 2>/dev/null | tail -n +11 | xargs -r rm --
cd ..

echo -e "${GREEN}=== Backup Complete ===${NC}"
echo -e "${GREEN}Backup location: ${BACKUP_DIR}/${BACKUP_NAME}*${NC}"

# List backups
echo -e "${YELLOW}Available backups:${NC}"
ls -lh ${BACKUP_DIR}/ | tail -10
