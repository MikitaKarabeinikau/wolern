#!/bin/bash

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}Running tests...${NC}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT" || exit 1

echo -e "${YELLOW}Project root: $PROJECT_ROOT${NC}"

# Set PYTHONPATH to include backend directory
export PYTHONPATH="$PROJECT_ROOT/backend:$PYTHONPATH"
export DATABASE_URL="postgresql+psycopg2://woler_test_user:password@localhost:5432/test_db"

echo -e "${YELLOW}PYTHONPATH: $PYTHONPATH${NC}"
echo ""

# Ensure package is installed in editable mode
if ! pip show wolern > /dev/null 2>&1; then
    echo -e "${YELLOW}Installing package in editable mode...${NC}"
    pip install -e . > /dev/null 2>&1
fi

echo -e "${GREEN}Running unit tests...${NC}"
pytest backend/tests/unit/ -v --cov=src --cov-report=term-missing --tb=short

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✓✓✓ All tests passed! ✓✓✓${NC}"
    exit 0
else
    echo ""
    echo -e "${RED}✗✗✗ Tests failed! ✗✗✗${NC}"
    exit 1
fi
