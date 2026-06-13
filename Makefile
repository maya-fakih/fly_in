SRC = main.py
MAP = maps/challenger/01_the_impossible_dream.txt

run: all
	python3 main.py $(MAP)