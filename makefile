lab_url:
	docker logs lab 2>&1 | grep 'http' | tail -1