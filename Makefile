ELECTRON = ./chlorine/node_modules/.bin/electron
CHLORINE = ${ELECTRON} ./chlorine
PYTHON   = python3
TESTDIR  = test
TEST     = ${PYTHON} -m unittest discover

cleanup:
	@rm *.log *.hlt || true

run_game: cleanup
	@./run_game.sh

run_chlorine:
	@${CHLORINE} &

chlorine\:%:
	@${CHLORINE} -o $* &

test:
	@${TEST} --start ${TESTDIR}

.PHONY: test

