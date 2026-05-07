#!/bin/bash

# UNOCHA Geo-Insight - Setup & Run Script
# This script helps you set up and run the application locally

set -e

echo "======================================"
echo "UNOCHA Geo-Insight Setup Script"
echo "======================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check Python version
echo -e "${BLUE}Checking Python version...${NC}"
python --version || {
    echo -e "${RED}Python not found. Please install Python 3.9+${NC}"
    exit 1
}

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${BLUE}Creating virtual environment...${NC}"
    python -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source venv/bin/activate

# Upgrade pip
echo -e "${BLUE}Upgrading pip...${NC}"
pip install --upgrade pip

# Install requirements
echo -e "${BLUE}Installing dependencies...${NC}"
pip install -r geo-insight/src/requirements.txt
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Check if CSV file exists
if [ ! -f "data/unocha_dataset.csv" ]; then
    echo -e "${YELLOW}⚠ Warning: data/unocha_dataset.csv not found${NC}"
    echo "   Please place your CSV file at: data/unocha_dataset.csv"
    echo ""
fi

# Setup .env file
if [ ! -f ".env" ]; then
    echo -e "${BLUE}Setting up .env file...${NC}"
    cp geo-insight/.env.example .env
    echo -e "${YELLOW}⚠ Please edit .env and add your OPENROUTER_API_KEY${NC}"
    echo "  Edit .env file now with your API key"
    echo ""
else
    echo -e "${GREEN}✓ .env file already exists${NC}"
fi

# Check if OPENROUTER_API_KEY is set
if ! grep -q "^OPENROUTER_API_KEY=" .env; then
    echo -e "${RED}❌ OPENROUTER_API_KEY not configured in .env${NC}"
    echo "   Please edit .env and add your key from https://openrouter.ai/"
    exit 1
fi

echo ""
echo -e "${GREEN}======================================"
echo "Setup Complete!"
echo "======================================"
echo ""
echo "To run the application:"
echo ""
echo "  1. Activate virtual environment:"
echo "     source venv/bin/activate"
echo ""
echo "  2. Run the app:"
echo "     python geo-insight/src/app.py"
echo ""
echo "  3. Open your browser:"
echo "     http://localhost:7860"
echo ""
echo -e "API Key status: ${GREEN}✓ Configured${NC}"
echo -e "CSV file status: $([ -f 'data/unocha_dataset.csv' ] && echo "${GREEN}✓ Found${NC}" || echo "${YELLOW}⚠ Not found${NC}")"
echo ""
