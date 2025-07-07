#!/usr/bin/bash
pip install flask flask_cors sqlalchemy mysqlclient python-dateutil flask-wft Flask-SQLAlchemy==3.0.5 Flask-Migrate==4.0.5
export TZ="Asia/Istanbul"
export INADIS_MYSQL_USER=stofgenius
export INADIS_MYSQL_HOST=stofgenius.mysql.pythonanywhere-services.com
export INADIS_MYSQL_DB="stofgenius$stories"
export INADIS_ENV="dev"
export INADIS_TYPE_STORAGE=db

# Linux
export DATABASE_URL=mysql+pymysql://stofgenius:readthedocs@stofgenius.mysql.pythonanywhere-services.com/stofgenius\$stories

# Environment setup script for Linux migration
# Run with: source setup_env_linux.sh

echo "Setting up environment variables for migration..."

# Database configuration
export DB_HOST="stofgenius.mysql.pythonanywhere-services.com"
export DB_PORT="3306"
export DB_NAME="stofgenius$stories"
export DB_USER="stofgenius"
export DB_PASSWORD="your_secure_password"

# Flask configuration
export FLASK_APP="migrate_app.py"
export FLASK_ENV="development"
export FLASK_DEBUG="1"

# Application configuration
export APP_SECRET_KEY="your-super-secret-key-change-this"
export APP_CONFIG="development"

# API configuration
export API_VERSION="v1"
export API_HOST="0.0.0.0"
export API_PORT="5000"

# CORS settings
export CORS_ORIGINS="*"

# Storage configuration
export STORAGE_TYPE="db"  # or "file" for file storage
export STORAGE_PATH="./data"

# Logging
export LOG_LEVEL="INFO"
export LOG_FILE="./logs/app.log"

# Linux


# Create necessary directories
mkdir -p ./logs
mkdir -p ./data

echo "Environment variables set successfully!"
echo "Current environment:"
echo "  FLASK_APP: $FLASK_APP"
echo "  FLASK_ENV: $FLASK_ENV"
echo "  DB_HOST: $DB_HOST"
echo "  DB_NAME: $DB_NAME"
echo "  API_VERSION: $API_VERSION"
echo ""
echo "To run the application:"
echo "  flask run --host=$API_HOST --port=$API_PORT"