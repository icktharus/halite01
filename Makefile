ELECTRON=./chlorine/node_modules/.bin/electron
CHLORINE=${ELECTRON} ./chlorine

run_game:
	@rm *.log
	@rm *.hlt
	@./run_game.sh

run_chlorine:
	@${CHLORINE} &

chlorine\:%:
	@${CHLORINE} -o $* &

