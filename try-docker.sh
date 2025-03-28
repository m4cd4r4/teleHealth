#!/bin/bash
# Shell script to help with Docker troubleshooting

# ANSI color codes
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

echo -e "${CYAN}TeleHealth Docker Troubleshooting Helper${NC}"
echo -e "${CYAN}=======================================${NC}"
echo ""

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo -e "${RED}Docker does not appear to be running.${NC}"
    echo -e "${RED}Please start Docker and try again.${NC}"
    exit 1
else
    echo -e "${GREEN}Docker is running.${NC}"
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

# Try to run the modified docker-compose file
echo ""
echo -e "${YELLOW}Attempting to start services with modified docker-compose file...${NC}"
echo -e "${YELLOW}(This may take a few minutes for the first run)${NC}"
echo ""

if docker-compose -f docker-compose.modified.yml up -d; then
    echo ""
    echo -e "${GREEN}Services started successfully!${NC}"
    echo ""
    echo -e "${CYAN}You can access the services at:${NC}"
    echo -e "${WHITE}- API Gateway: http://localhost:8000${NC}"
    echo -e "${WHITE}- API Documentation: http://localhost:8000/docs${NC}"
    echo ""
    echo -e "${CYAN}To view logs:${NC}"
    echo -e "${WHITE}docker-compose -f docker-compose.modified.yml logs -f${NC}"
    echo ""
    echo -e "${CYAN}To stop the services:${NC}"
    echo -e "${WHITE}docker-compose -f docker-compose.modified.yml down${NC}"
else
    echo -e "${RED}Failed to start services.${NC}"
    echo -e "${RED}Please check the error messages above.${NC}"
    echo ""
    echo -e "${YELLOW}For more troubleshooting help, see DOCKER_TROUBLESHOOTING.md${NC}"
fi

echo ""
echo -e "${CYAN}If Docker continues to cause issues, you can use the local development approach:${NC}"
echo -e "${WHITE}1. Run ./reload-vscode.sh to set up your environment${NC}"
echo -e "${WHITE}2. Follow the instructions in DEVELOPMENT.md for local setup${NC}"
