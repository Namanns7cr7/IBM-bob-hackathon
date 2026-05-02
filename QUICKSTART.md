# DebugSensei - Quick Start Guide

Get DebugSensei running in 5 minutes! 🚀

## Prerequisites

- Python 3.10+ installed
- Node.js 18+ installed
- A code editor (VS Code recommended)

## Step 1: Clone/Download

If you have the project, navigate to the `debugsensei` directory:

```bash
cd debugsensei
```

## Step 2: Start Backend (Terminal 1)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the server
python -m uvicorn main:app --reload
```

✅ Backend running at: `http://localhost:8000`

## Step 3: Start Frontend (Terminal 2)

Open a new terminal:

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

✅ Frontend running at: `http://localhost:3000`

## Step 4: Test It Out

1. Open your browser to `http://localhost:3000`
2. You should see the DebugSensei interface
3. Try the demo flow:
   - Upload a ZIP file of any codebase
   - Select your skill level
   - Click "Analyze Codebase"
   - Explore the results!

## Quick Test Without Upload

To test the API directly:

```bash
# Check health
curl http://localhost:8000/health

# List available docs
curl http://localhost:8000/docs
```

## Common Issues

### Backend Issues

**Issue**: `ModuleNotFoundError: No module named 'fastapi'`
**Solution**: Make sure virtual environment is activated and dependencies are installed:
```bash
pip install -r requirements.txt
```

**Issue**: `Address already in use`
**Solution**: Change the port:
```bash
uvicorn main:app --reload --port 8001
```

### Frontend Issues

**Issue**: `npm: command not found`
**Solution**: Install Node.js from https://nodejs.org/

**Issue**: Port 3000 already in use
**Solution**: Vite will automatically suggest another port, or specify one:
```bash
npm run dev -- --port 3001
```

## Next Steps

1. **Read the README**: Full documentation in `README.md`
2. **Try the Demo**: Follow `DEMO.md` for a guided tour
3. **Understand Bob Usage**: Read `BOB_USAGE.md` for architecture details
4. **See the Impact**: Check `IMPACT.md` for metrics and benefits

## Creating a Test Repository

Want to test with a sample project? Create a simple one:

```bash
# Create a test directory
mkdir test-repo
cd test-repo

# Create a simple Python file
echo "def hello():
    print('Hello World')" > main.py

# Create a requirements file
echo "fastapi==0.104.1" > requirements.txt

# Zip it
zip -r test-repo.zip .
```

Now upload `test-repo.zip` to DebugSensei!

## Development Mode

Both servers run in development mode with hot reload:
- **Backend**: Changes to `.py` files auto-reload
- **Frontend**: Changes to `.jsx` files auto-reload

## Production Build

### Backend
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Frontend
```bash
npm run build
npm run preview
```

## Need Help?

- Check the full README.md
- Review the code comments
- Open an issue on GitHub
- Contact the maintainers

---

**Happy Debugging! 🥋**