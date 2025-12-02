$root=(Get-Location).path
cd $root/front-end/not-jeopardy

# install package dependencies for frontend
npm ci

# build production code for frontend
npm run build

cd $root

python -m venv .venv

.venv/Scripts/activate

# install package dependencies for backend
pip install -r requirements.txt