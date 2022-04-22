run-db:
	docker run --name local -p 5432:5432 -e POSTGRES_PASSWOR=123 -e POSTGRES_DB=fastapi -v ${PWD}/db_Data:/var/lib/postgresql/data -d postgres
	