ELECTRON=./chlorine/node_modules/.bin/electron
CHLORINE=${ELECTRON} ./chlorine

cleanup:
	@rm *.log
	@rm *.hlt

run_game: cleanup
	@./run_game.sh

run_chlorine:
	@${CHLORINE} &

chlorine\:%:
	@${CHLORINE} -o $* &

