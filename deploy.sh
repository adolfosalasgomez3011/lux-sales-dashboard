#!/bin/bash
# Quick Deploy Script for Lux Sales Dashboard

echo "🚀 Deploying Lux Sales Dashboard..."
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing Git repository..."
    git init
    echo "✅ Git initialized"
else
    echo "✅ Git already initialized"
fi

# Add all files
echo "📝 Adding files to Git..."
git add .

# Commit
echo "💾 Creating commit..."
git commit -m "Deploy: $(date '+%Y-%m-%d %H:%M:%S')"

# Check if remote exists
if git remote | grep -q "origin"; then
    echo "🌐 Pushing to GitHub..."
    git push
    echo "✅ Pushed to GitHub!"
    echo ""
    echo "🎉 Streamlit Cloud will auto-deploy in ~1 minute"
else
    echo ""
    echo "⚠️  No GitHub remote configured yet."
    echo ""
    echo "📋 Next steps:"
    echo "1. Create repo on GitHub: https://github.com/new"
    echo "2. Run these commands:"
    echo ""
    echo "   git remote add origin https://github.com/YOUR-USERNAME/lux-sales-dashboard.git"
    echo "   git push -u origin main"
    echo ""
fi
