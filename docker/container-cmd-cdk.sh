export LANGINFRA_DATABASE_URL="mysql+pymysql://${username}:${password}@${host}:3306/${dbname}"
# echo $LANGINFRA_DATABASE_URL
uvicorn --factory langinfra.main:create_app --host 0.0.0.0 --port 7860 --reload --log-level debug --loop asyncio

# python -m langinfra run --host 0.0.0.0 --port 7860