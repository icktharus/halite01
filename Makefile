ELECTRON = ./chlorine/node_modules/.bin/electron
CHLORINE = ${ELECTRON} ./chlorine
PYTHON   = python3
TESTDIR  = test
TEST     = ${PYTHON} -m unittest discover

build:
	@$(MAKE) run_game
	@$(MAKE) chlorine:*.hlt

run_game: clean
	@./run_game.sh

run_chlorine:
	@${CHLORINE} &

chlorine\:%:
	@${CHLORINE} -o $* &

clean:
	@rm *.log *.hlt || true

test:
	@${TEST} --start ${TESTDIR}

.PHONY: build run_game run_chlorine clean test
