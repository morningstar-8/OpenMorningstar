# 本地开发
dev() {
	# update_dev_package # NOTE: 更新docker开发环境
	source /Users/henry529/Projects/OpenMorningstar/env/bin/activate
	# python -m pip install --upgrade pip
	pip freeze >requirements.txt
	pip freeze >deploy/django/requirements.txt
	pipdeptree -fl >pipdeptree.txt
	python manage.py makemigrations
	python manage.py migrate
	python manage.py rebuild_index --noinput
	python manage.py collectstatic --noinput
	python manage.py runserver 0.0.0.0:8000
}

# 数据生成
fake() {
	source /Users/henry529/Projects/OpenMorningstar/env/bin/activate
	python scripts/fake/fake.py
}

# 单元测试
coverge() {
	source /Users/henry529/Projects/OpenMorningstar/env/bin/activate
	coverage erase --rcfile=scripts/coverge/.coveragerc
	coverage run --rcfile=scripts/coverge/.coveragerc manage.py test Morningstar/ apps/ --failfast --keepdb
	coverage report --rcfile=scripts/coverge/.coveragerc
	coverage html --rcfile=scripts/coverge/.coveragerc
	live-server scripts/coverge/coverage_html_report
}

# 代码提交
autoci() {
	## UpdateAll Method
	read -p "输入commit内容: " commit
	ci_time=$(date "+%Y.%m.%d %H:%M")
	# 更新主体
	git add -A
	if test ${#commit} -gt 0; then
		commit=': '$commit
	fi
	git commit -m "💩${ci_time}${commit}"
	git push github main
	# 更新静态文件
	cd static/ && git add -A && git ci "update: ${ci_time}" && git push github main && cd ../
	echo "更新完成"
	fortune
}

# 远程同步
update() {
	source /Users/henry529/Projects/OpenMorningstar/env/bin/activate
	fab -H jeep_jipu@server.morningstar529.com -r scripts/fabric -p update
}

# 数据备份
backup() {
	source /Users/henry529/Projects/OpenMorningstar/env/bin/activate
	fab -H jeep_jipu@server.morningstar529.com -r scripts/fabric -p backup
}

# 数据还原
restore() {
	source /Users/henry529/Projects/OpenMorningstar/env/bin/activate
	fab -H jeep_jipu@server.morningstar529.com -r scripts/fabric -p restore
}

# 整体更新
upgrade() {
	source /Users/henry529/Projects/OpenMorningstar/env/bin/activate
	fab -H jeep_jipu@server.morningstar529.com -r scripts/fabric -p upgrade
}

# 检视信息
check() {
	source /Users/henry529/Projects/OpenMorningstar/env/bin/activate
	fab -H jeep_jipu@server.morningstar529.com -r scripts/fabric --prompt-for-login-password -p check
}

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

backupDockerVolume() {
	source /Users/henry529/Projects/OpenMorningstar/env/bin/activate
	fab -H jeep_jipu@server.morningstar529.com -r scripts/fabric -p backupDockerVolume
}

restoreDockerVolume() {
	source /Users/henry529/Projects/OpenMorningstar/env/bin/activate
	fab -H jeep_jipu@server.morningstar529.com -r scripts/fabric -p restoreDockerVolume
}

updatePackage() {
	source /Users/henry529/Projects/OpenMorningstar/env/bin/activate
	echo "更新生产环境下的容器..."
	fab -H jeep_jipu@server.morningstar529.com -r scripts/fabric -p updatePackage
	echo "更新开发环境下的容器..."
	read -s -n1 -p '按任意键继续...'
	docker compose -f deploy/example_dev.yml up --build -d
	docker push henry529/dev
	docker tag henry529/dev ghcr.io/henryji529/morningstar-dev
	docker push ghcr.io/henryji529/morningstar-dev
	docker tag henry529/dev dockerhub.morningstar529.com/morningstar-dev
	docker push dockerhub.morningstar529.com/morningstar-dev
}

updateDocs() {
	cd docs/
	vercel --prod
	cd ../
}

publicCoverage() {
	cd scripts/coverge/coverage_html_report/
	vercel --prod
	cd ../../../
}

#==================================================================

cat <<_haibara_
$(figlet Morningstar)
_haibara_

echo "运行命令:
============================================================
a. backupDockerVolume();
b. restoreDockerVolume();
c. updatePackage();
d. updateDocs();
e. publicCoverage();
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
0. check();
1. dev();
2. fake();
3. coverge();
4. autoci();
5. update();
6. backup();
7. restore();
8. upgrade();
"
read -p "输入序号(a-e|0-8): " order

start_time=$(date +%s)

case $order in
a) backupDockerVolume ;;
b) restoreDockerVolume ;;
c) updatePackage ;;
d) updateDocs ;;
e) publicCoverage ;;
# ==========================
0) check ;;
1) dev ;;
2) fake ;;
3) coverge ;;
4) autoci ;;
5) update ;;
6) backup ;;
7) restore ;;
8) upgrade ;;
*) echo "输入错误" ;;
esac
end_time=$(date +%s)
during=$((end_time - start_time))
echo "运行时间: $during 秒"
