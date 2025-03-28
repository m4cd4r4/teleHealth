#!/bin/bash
# Shell script to run the TeleHealth application locally without Docker

# ANSI color codes
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

echo -e "${CYAN}TeleHealth Local Development Runner${NC}"
echo -e "${CYAN}===================================${NC}"
echo ""

# Create and activate virtual environment
if [ ! -d "./venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to create virtual environment. Make sure Python is installed.${NC}"
        exit 1
    fi
fi

echo -e "${YELLOW}Activating virtual environment...${NC}"
source ./venv/bin/activate

# Install dependencies for each service
echo -e "${YELLOW}Installing dependencies for gateway...${NC}"
pip install -r gateway/requirements.txt

echo -e "${YELLOW}Installing dependencies for auth-service...${NC}"
pip install -r auth-service/requirements.txt

echo -e "${YELLOW}Installing dependencies for patient-service...${NC}"
pip install -r patient-service/requirements.txt

echo ""
echo -e "${GREEN}Dependencies installed successfully.${NC}"
echo ""

# Check if PostgreSQL is installed
pgInstalled=false
if command -v psql &> /dev/null; then
    pgVersion=$(psql --version)
    pgInstalled=true
    echo -e "${GREEN}PostgreSQL is installed: $pgVersion${NC}"
else
    echo -e "${YELLOW}PostgreSQL is not installed or not in PATH.${NC}"
fi

if [ "$pgInstalled" = false ]; then
    echo -e "${YELLOW}Warning: PostgreSQL is required for the auth and patient services.${NC}"
    echo -e "${YELLOW}Please install PostgreSQL from your package manager or https://www.postgresql.org/download/${NC}"
    echo ""
fi

# Check if Redis is installed
redisInstalled=false
if command -v redis-cli &> /dev/null; then
    redisVersion=$(redis-cli --version)
    redisInstalled=true
    echo -e "${GREEN}Redis is installed: $redisVersion${NC}"
else
    echo -e "${YELLOW}Redis is not installed or not in PATH.${NC}"
fi

if [ "$redisInstalled" = false ]; then
    echo -e "${YELLOW}Warning: Redis is required for rate limiting and caching in the gateway.${NC}"
    echo -e "${YELLOW}Please install Redis from your package manager or https://redis.io/download${NC}"
    echo ""
fi

# Instructions for running the services
echo -e "${CYAN}To run the TeleHealth services, open three separate terminal windows:${NC}"
echo ""

echo -e "${WHITE}Terminal 1 - Auth Service:${NC}"
echo -e "${WHITE}cd $(pwd)/auth-service${NC}"
echo -e "${WHITE}source ../venv/bin/activate${NC}"
echo -e "${WHITE}uvicorn src.main:app --reload --port 8001${NC}"
echo ""

echo -e "${WHITE}Terminal 2 - Patient Service:${NC}"
echo -e "${WHITE}cd $(pwd)/patient-service${NC}"
echo -e "${WHITE}source ../venv/bin/activate${NC}"
echo -e "${WHITE}uvicorn src.main:app --reload --port 8002${NC}"
echo ""

echo -e "${WHITE}Terminal 3 - API Gateway:${NC}"
echo -e "${WHITE}cd $(pwd)/gateway${NC}"
echo -e "${WHITE}source ../venv/bin/activate${NC}"
echo -e "${WHITE}uvicorn src.main:app --reload --port 8000${NC}"
echo ""

echo -e "${CYAN}After starting all services, you can access the application at:${NC}"
echo -e "${WHITE}- API Gateway: http://localhost:8000${NC}"
echo -e "${WHITE}- API Documentation: http://localhost:8000/docs${NC}"
echo ""

# Ask which service to run in this terminal
echo -e "${CYAN}Would you like to run one of the services in this terminal?${NC}"
echo -e "${WHITE}1. Auth Service (port 8001)${NC}"
echo -e "${WHITE}2. Patient Service (port 8002)${NC}"
echo -e "${WHITE}3. API Gateway (port 8000)${NC}"
echo -e "${WHITE}4. None (exit script)${NC}"
echo ""

read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        echo -e "${YELLOW}Starting Auth Service...${NC}"
        cd "$(pwd)/auth-service"
        uvicorn src.main:app --reload --port 8001
        ;;
    2)
        echo -e "${YELLOW}Starting Patient Service...${NC}"
        cd "$(pwd)/patient-service"
        uvicorn src.main:app --reload --port 8002
        ;;
    3)
        echo -e "${YELLOW}Starting API Gateway...${NC}"
        cd "$(pwd)/gateway"
        uvicorn src.main:app --reload --port 8000
        ;;
    4)
        echo -e "${YELLOW}Exiting script.${NC}"
        ;;
    *)
        echo -e "${RED}Invalid choice. Exiting script.${NC}"
        ;;
esac
