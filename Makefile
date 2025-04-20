fullrevision:	
	alembic downgrade -1;  \
	sleep 3; \
	rm ./migrations/versions/*; \
	alembic revision --autogenerate -m "initial migration"; \
	sleep 3; \
	alembic upgrade head; \
