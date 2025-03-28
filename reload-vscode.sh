#!/bin/bash
# Shell script to help reload VSCode and select the Python interpreter

# ANSI color codes
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

echo -e "${CYAN}TeleHealth Development Environment Setup Helper${NC}"
echo -e "${CYAN}================================================${NC}"
echo ""

# Check if VSCode is installed
if ! command -v code &> /dev/null; then
    echo -e "${RED}Visual Studio Code is not found in your PATH.${NC}"
    echo -e "${RED}Please make sure VSCode is installed and 'code' command is available.${NC}"
    exit 1
fi

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

echo ""
echo -e "${GREEN}Next steps:${NC}"
echo -e "${WHITE}1. In VSCode, press Cmd+Shift+P to open the command palette${NC}"
echo -e "${WHITE}2. Type 'Developer: Reload Window' and press Enter${NC}"
echo -e "${WHITE}3. After VSCode reloads, press Cmd+Shift+P again${NC}"
echo -e "${WHITE}4. Type 'Python: Select Interpreter' and press Enter${NC}"
echo -e "${WHITE}5. Select the interpreter from your virtual environment (it should include 'venv' in the path)${NC}"
echo ""
echo -e "${CYAN}This will apply the VSCode settings and configure the Python environment.${NC}"

# Open VSCode in the current directory if it's not already open
echo -e "${YELLOW}Opening VSCode in the current directory...${NC}"
code .

echo ""
echo -e "${CYAN}For more information, see the DEVELOPMENT.md file.${NC}"
