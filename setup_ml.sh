#!/bin/bash

# Setup script for ML training infrastructure

set -e

echo "================================================"
echo "🚀 Setting up ML Training Infrastructure"
echo "================================================"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Git LFS is installed
echo -e "\n${BLUE}Checking Git LFS...${NC}"
if ! command -v git-lfs &> /dev/null; then
    echo -e "${YELLOW}Git LFS not found. Installing...${NC}"
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        brew install git-lfs
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        sudo apt-get update
        sudo apt-get install -y git-lfs
    else
        echo -e "${YELLOW}Please install Git LFS manually: https://git-lfs.github.com/${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✅ Git LFS already installed${NC}"
fi

# Initialize Git LFS
echo -e "\n${BLUE}Initializing Git LFS...${NC}"
git lfs install
echo -e "${GREEN}✅ Git LFS initialized${NC}"

# Track model files
echo -e "\n${BLUE}Setting up Git LFS tracking...${NC}"
git lfs track "*.h5"
git lfs track "*.keras"
git lfs track "*.pb"
git lfs track "*.pkl"
echo -e "${GREEN}✅ Model files tracked${NC}"

# Create virtual environment for ML
echo -e "\n${BLUE}Creating Python virtual environment...${NC}"
cd ml
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo -e "\n${BLUE}Installing ML dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt
echo -e "${GREEN}✅ Dependencies installed${NC}"

# Create data directories
echo -e "\n${BLUE}Creating data directories...${NC}"
mkdir -p data/train/Positive data/train/Negative
mkdir -p data/val/Positive data/val/Negative
mkdir -p data/test/Positive data/test/Negative
mkdir -p checkpoints
mkdir -p logs
echo -e "${GREEN}✅ Directories created${NC}"

# Deactivate virtual environment
deactivate
cd ..

# Add Git LFS files
echo -e "\n${BLUE}Committing Git LFS configuration...${NC}"
git add .gitattributes
git commit -m "Setup Git LFS for model tracking" || echo "Already committed"

echo -e "\n${GREEN}================================================${NC}"
echo -e "${GREEN}✅ Setup completed successfully!${NC}"
echo -e "${GREEN}================================================${NC}"

echo -e "\n${YELLOW}Next steps:${NC}"
echo "1. Copy your training data to ml/data/"
echo "2. cd ml && source venv/bin/activate"
echo "3. python train.py"
echo "4. python evaluate.py ../inference-service/models/model.h5 data/test"
echo "5. git add inference-service/models/model.h5"
echo "6. git commit -m 'Update model'"
echo "7. git push origin main"

echo -e "\n${BLUE}For GitHub Actions:${NC}"
echo "- Add DOCKER_USERNAME and DOCKER_PASSWORD secrets to your GitHub repo"
echo "- Settings > Secrets and variables > Actions > New repository secret"
