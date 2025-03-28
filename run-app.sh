#!/bin/bash
# Shell script to run the TeleHealth application

# ANSI color codes
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

echo -e "${CYAN}TeleHealth Application Runner${NC}"
echo -e "${CYAN}===========================${NC}"
echo ""

# Check if Docker is running
dockerRunning=false
if command -v docker &> /dev/null; then
    if docker info &> /dev/null; then
        dockerRunning=true
        echo -e "${GREEN}Docker is running.${NC}"
    else
        echo -e "${YELLOW}Docker is not running.${NC}"
    fi
else
    echo -e "${YELLOW}Docker is not installed or not in PATH.${NC}"
fi

# Check if .env files exist, create from examples if they don't
services=("gateway" "auth-service" "patient-service")
for service in "${services[@]}"; do
    env_file="./$service/.env"
    env_example_file="./$service/.env.example"
    
    if [ ! -f "$env_file" ]; then
        if [ -f "$env_example_file" ]; then
            echo -e "${YELLOW}Creating $env_file from example file...${NC}"
            cp "$env_example_file" "$env_file"
            echo -e "${GREEN}Created $env_file${NC}"
        else
            echo -e "${YELLOW}Warning: $env_example_file not found, cannot create $env_file${NC}"
        fi
    else
        echo -e "${GREEN}$env_file already exists.${NC}"
    fi
done

# Ask user which method they want to use
echo ""
echo -e "${CYAN}How would you like to run the application?${NC}"
echo -e "${WHITE}1. Using Docker (recommended)${NC}"
echo -e "${WHITE}2. Local development (requires PostgreSQL and Redis)${NC}"
echo ""

read -p "Enter your choice (1 or 2): " choice

if [ "$choice" = "1" ]; then
    # Docker approach
    if [ "$dockerRunning" = false ]; then
        echo -e "${RED}Docker is not running. Please start Docker and try again.${NC}"
        exit 1
    fi
    
    echo ""
    echo -e "${YELLOW}Starting the application using Docker...${NC}"
    echo -e "${YELLOW}(This may take a few minutes for the first run)${NC}"
    echo ""
    
    if docker-compose -f docker-compose.modified.yml up -d; then
        echo ""
        echo -e "${GREEN}Services started successfully!${NC}"
        echo ""
        echo -e "${CYAN}You can access the application at:${NC}"
        echo -e "${WHITE}- API Gateway: http://localhost:8000${NC}"
        echo -e "${WHITE}- API Documentation: http://localhost:8000/docs${NC}"
        echo ""
        echo -e "${CYAN}To view logs:${NC}"
        echo -e "${WHITE}docker-compose -f docker-compose.modified.yml logs -f${NC}"
        echo ""
        echo -e "${CYAN}To stop the application:${NC}"
        echo -e "${WHITE}docker-compose -f docker-compose.modified.yml down${NC}"
    else
        echo -e "${RED}Failed to start services.${NC}"
        echo -e "${RED}Please check the error messages above.${NC}"
        echo ""
        echo -e "${YELLOW}For more troubleshooting help, see DOCKER_TROUBLESHOOTING.md${NC}"
    fi
elif [ "$choice" = "2" ]; then
    # Local development approach
    echo ""
    echo -e "${YELLOW}Starting the application using local development...${NC}"
    echo ""
    
    # Check if virtual environment exists
    if [ ! -d "./venv" ]; then
        echo -e "${YELLOW}Virtual environment not found.${NC}"
        echo -e "${YELLOW}Creating a new virtual environment...${NC}"
        
        python3 -m venv venv
        if [ $? -ne 0 ]; then
            echo -e "${RED}Failed to create virtual environment. Make sure Python is installed.${NC}"
            exit 1
        fi
        
        echo -e "${GREEN}Virtual environment created successfully.${NC}"
    fi
    
    # Activate virtual environment
    echo -e "${YELLOW}Activating virtual environment...${NC}"
    source ./venv/bin/activate
    
    # Install dependencies
    echo -e "${YELLOW}Installing dependencies...${NC}"
    pip install -r gateway/requirements.txt
    pip install -r auth-service/requirements.txt
    pip install -r patient-service/requirements.txt
    
    echo ""
    echo -e "${GREEN}Dependencies installed.${NC}"
    echo ""
    echo -e "${CYAN}To run the application, you need to open three separate terminal windows:${NC}"
    echo ""
    echo -e "${WHITE}Terminal 1 - Auth Service:${NC}"
    echo -e "${WHITE}cd $(pwd)/auth-service${NC}"
    echo -e "${WHITE}uvicorn src.main:app --reload --port 8001${NC}"
    echo ""
    echo -e "${WHITE}Terminal 2 - Patient Service:${NC}"
    echo -e "${WHITE}cd $(pwd)/patient-service${NC}"
    echo -e "${WHITE}uvicorn src.main:app --reload --port 8002${NC}"
    echo ""
    echo -e "${WHITE}Terminal 3 - API Gateway:${NC}"
    echo -e "${WHITE}cd $(pwd)/gateway${NC}"
    echo -e "${WHITE}uvicorn src.main:app --reload --port 8000${NC}"
    echo ""
    echo -e "${CYAN}After starting all services, you can access the application at:${NC}"
    echo -e "${WHITE}- API Gateway: http://localhost:8000${NC}"
    echo -e "${WHITE}- API Documentation: http://localhost:8000/docs${NC}"
else
    echo -e "${RED}Invalid choice. Please run the script again and enter 1 or 2.${NC}"
fi

echo ""
echo -e "${CYAN}For more information, see the HOW_TO_RUN.md file.${NC}"
