#!/bin/bash

# Contact Data Cleaner - Server Deployment Script
# For DigitalOcean, AWS, Google Cloud, or any VPS with Docker

set -e

echo "🚀 Contact Data Cleaner - Server Deployment"
echo "============================================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed!"
    echo ""
    echo "Installing Docker..."
    
    # Install Docker
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    rm get-docker.sh
    
    echo "✅ Docker installed!"
    echo "⚠️  Please log out and log back in for Docker permissions to take effect."
    echo "Then run this script again."
    exit 0
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "Installing Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    echo "✅ Docker Compose installed!"
fi

echo "📦 Building Docker image..."
docker-compose build

echo ""
echo "🚀 Starting application..."
docker-compose up -d

echo ""
echo "⏳ Waiting for application to start (30 seconds)..."
sleep 30

# Get server IP
SERVER_IP=$(curl -s ifconfig.me || hostname -I | awk '{print $1}')

echo ""
echo "============================================"
echo "✅ Deployment Complete!"
echo "============================================"
echo ""
echo "🌐 Your application is now running at:"
echo ""
echo "   http://$SERVER_IP:8501"
echo ""
echo "📱 Access from anywhere:"
echo "   1. Open a browser"
echo "   2. Go to: http://$SERVER_IP:8501"
echo "   3. Upload files up to 20GB!"
echo ""
echo "🔍 Check status:"
echo "   docker-compose ps"
echo ""
echo "📊 View logs:"
echo "   docker-compose logs -f"
echo ""
echo "🛑 Stop server:"
echo "   docker-compose down"
echo ""
echo "🔄 Update application:"
echo "   git pull"
echo "   docker-compose up -d --build"
echo ""
echo "============================================"

