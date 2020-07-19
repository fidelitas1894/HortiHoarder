if [ ! -d "venv" ]; then
  virtualenv -p python3 venv
fi

. venv/bin/activate

pip install -r requirements.txt

python3 HortiHoarder.py
