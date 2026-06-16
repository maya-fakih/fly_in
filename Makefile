SRC = ./src/main.py ./src/parser.py ./src/parsing_errors.py ./src/sim_errors.py ./src/zone_types.py
MAP = maps/challenger/01_the_impossible_dream.txt

lint:
	python3 -m flake8
	python3 -m mypy .
run: all
	python3 main.py $(MAP)