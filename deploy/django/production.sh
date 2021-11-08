cd /app
# 需创建超级管理员
python3 manage.py makemigrations --settings=Morningstar.settings.production
python3 manage.py migrate --settings=Morningstar.settings.production
python3 manage.py rebuild_index --settings=Morningstar.settings.production --noinput
python3 manage.py collectstatic --settings=Morningstar.settings.production --noinput
