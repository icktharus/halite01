ELECTRON = ./chlorine/node_modules/.bin/electron
CHLORINE = ${ELECTRON} ./chlorine
PYTHON   = python3
TESTDIR  = test
TEST     = ${PYTHON} -m unittest discover
ZIP      = zip

build:
	@$(MAKE) run_game
	@$(MAKE) chlorine:*.hlt

run_game: clean
	@./run_game.sh

run_chlorine:
	@${CHLORINE} &

chlorine\:%:
	@echo "Displaying game..."
	@${CHLORINE} -o $* &

clean:
	@rm *.log *.hlt || true
	@rm submission.zip || true
	@find . -name "*.pyc" | xargs rm

test:
	@${TEST} --start ${TESTDIR}

.PHONY: build run_game run_chlorine clean test

submission.zip:
	@${ZIP} -r submission.zip MyBot.py hlt
