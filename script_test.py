"""Ce script a été créé pour tester les modèles trouvés dans /models."""
from models.tournament import Tournament


def main():
    new_tournament = Tournament(
        name="Tournoi de test3",
        place="Testtown",
        date_start="2020-12-10",
        date_end="2020-12-16",
        description="Ceci est un test du tournoi, le test 3",
        rounds_number=4
    )

    list_of_players = ["p_1", "p_2", "p_3", "p_4", "p_17", "p_18", "p_19", "p_20"]
    for player_id in list_of_players:
        new_tournament.add_participant(player_id)

    new_tournament.initialize_first_round()

    for round_num in range(1, new_tournament.rounds_number + 1):
        round_key = f"Round_{round_num}"
        current_round = new_tournament.rounds.get(round_key)
        if not current_round:
            print(f"Le {round_key} n'existe pas.")
            continue

        print(f"\n--- {round_key} ---")
        for match in current_round.matches:
            print(f"Match : {repr(match)}")
            while True:
                winner = input("Gagnant ? (entrer l'ID du joueur, 'draw' pour match nul): ")
                if winner.lower() == 'draw':
                    match.draw()
                    break
                elif winner in match.score.keys():
                    match.id_win(winner)
                    break
                else:
                    print("Entrée invalide. Veuillez réessayer.")

        new_tournament.complete_round(round_key)

        if new_tournament.complete:
            print("Tournoi terminé")
            break
        else:
            new_tournament.start_next_round()

        print('############')
        print("Participants:")
        for pid, (player_obj, score) in new_tournament.participants.items():
            print(f"{pid}: {player_obj}, Score: {score}")
        print("\nClassement:")
        ranking = new_tournament.get_ranking()
        for rank, players in ranking.items():
            print(f"Rang {rank}: {', '.join(players)}")
        print("\nRounds:")
        for round_name, round_obj in new_tournament.rounds.items():
            status = 'Terminé' if round_obj and round_obj.is_finished else 'En cours ou non démarré'
            print(f"{round_name}: {status}")
        print('############')
        new_tournament.save_to_database()

    if new_tournament.complete:
        print("Le tournoi est maintenant complet.")
    else:
        print("Le tournoi n'est pas encore complet.")


if __name__ == '__main__':
    main()
