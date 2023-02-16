def get_list_of_available_game_from_db(game_model):
        data = game_model.objects.filter(opponent__isnull = True, game_end_status = False).order_by("date_of_the_game")
        list_of_game = []
        for obj in data:
            list_of_game.append((str(obj), obj.id, str(obj.owner)))
        return list_of_game