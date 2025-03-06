"""
Moodul lauamängu statistika jälgimiseks ja analüüsimiseks.
Pakub funktsionaalsust mängude salvestamiseks, mängijate soorituse jälgimiseks
ja erinevate statistikate pärimiseks mängude ja mängijate kohta.
"""

import collections


class Player:
    """
    Esindab mängijat, kes osaleb erinevates mängudes.
    Jälgib mängitud mänge, võite ja kaotusi iga mängija kohta.
    """
    
    def __init__(self, name):
        """
        Lähtesta mängija nime ja tühja statistikaga.
        
        Args:
            name (str): Mängija nimi
        """
        self.name = name
        self.games_played = collections.defaultdict(int)
        self.wins = 0
        self.losses = 0
    
    def add_game(self, game_name, won=False, lost=False):
        """
        Salvesta mängija poolt mängitud mäng.
        
        Args:
            game_name (str): Mängitud mängu nimi
            won (bool): Kas mängija võitis mängu
            lost (bool): Kas mängija kaotas mängu
        """
        self.games_played[game_name] += 1
        if won:
            self.wins += 1
        if lost:
            self.losses += 1
    
    def favourite_game(self):
        """
        Määra mängija kõige sagedamini mängitud mäng.
        
        Returns:
            str või None: Kõige rohkem mängitud mängu nimi või None kui mänge pole mängitud
        """
        return max(self.games_played, key=self.games_played.get, default=None)


class Game:
    """
    Esindab konkreetset mängu koos selle statistikaga.
    Jälgib mängukordi, võite, kaotusi ja rekordeid.
    """
    
    def __init__(self, name):
        """
        Lähtesta mäng nime ja tühja statistikaga.
        
        Args:
            name (str): Mängu nimi
        """
        self.name = name
        self.play_count = 0
        self.player_counts = collections.defaultdict(int)
        self.wins = collections.defaultdict(int)
        self.losses = collections.defaultdict(int)
        self.high_scores = {}
        # Jälgi mängijate osalemiste arvu
        self.player_plays = collections.defaultdict(int)
    
    def add_play(self, players, result_type, results):
        """
        Salvesta üks mängukord.
        
        Args:
            players (list): Osalenud mängijate nimede loend
            result_type (str): Tulemuse tüüp ("points", "places" või "winner")
            results (list): Mängu tulemused, formaat sõltub result_type'st
        """
        self.play_count += 1
        self.player_counts[len(players)] += 1
        
        # Jälgi iga mängija osalemist
        for player in players:
            self.player_plays[player] += 1
        
        if result_type == "points":
            scores = list(map(int, results))
            max_score = max(scores)
            min_score = min(scores)
            
            winners = [players[i] for i, score in enumerate(scores) if score == max_score]
            losers = [players[i] for i, score in enumerate(scores) if score == min_score]
            
            for winner in winners:
                self.wins[winner] += 1
            for loser in losers:
                self.losses[loser] += 1
            
            for player, score in zip(players, scores):
                if player not in self.high_scores or self.high_scores[player] < score:
                    self.high_scores[player] = score
        
        elif result_type == "places":
            winner = results[0]
            loser = results[-1]
            self.wins[winner] += 1
            self.losses[loser] += 1
        
        elif result_type == "winner":
            winner = results[0]
            self.wins[winner] += 1
    
    def most_wins(self):
        """
        Leia mängija, kellel on selles mängus kõige rohkem võite.
        
        Returns:
            str või None: Kõige rohkem võitnud mängija nimi või None kui võite pole registreeritud
        """
        return max(self.wins, key=self.wins.get, default=None)
    
    def most_frequent_winner(self):
        """
        Leia mängija, kellel on selles mängus kõrgeim võidumäär.
        Võidumäär arvutatakse võitude jagamisel mängija mängitud mängude arvuga.
        
        Returns:
            str või None: Kõrgeima võidumääraga mängija nimi või None kui võite pole registreeritud
        """
        if not self.wins:
            return None
        
        # Arvuta võidusagedus kui võidud jagatud mängija mängitud mängudega
        win_frequency = {}
        for player, wins in self.wins.items():
            if player in self.player_plays and self.player_plays[player] > 0:
                win_frequency[player] = wins / self.player_plays[player]
        
        if not win_frequency:
            return None
        
        return max(win_frequency, key=win_frequency.get)
    
    def most_losses(self):
        """
        Leia mängija, kellel on selles mängus kõige rohkem kaotusi.
        
        Returns:
            str või None: Kõige rohkem kaotanud mängija nimi või None kui kaotusi pole registreeritud
        """
        return max(self.losses, key=self.losses.get, default=None)
    
    def most_frequent_loser(self):
        """
        Leia mängija, kellel on selles mängus kõrgeim kaotuse määr.
        Kaotuse määr arvutatakse kaotuste jagamisel mängija mängitud mängude arvuga.
        
        Returns:
            str või None: Kõrgeima kaotuse määraga mängija nimi või None kui kaotusi pole registreeritud
        """
        if not self.losses:
            return None
        
        # Arvuta kaotussagedus kui kaotused jagatud mängija mängitud mängudega
        loss_frequency = {}
        for player, losses in self.losses.items():
            if player in self.player_plays and self.player_plays[player] > 0:
                loss_frequency[player] = losses / self.player_plays[player]
        
        if not loss_frequency:
            return None
        
        return max(loss_frequency, key=loss_frequency.get)
    
    def record_holder(self):
        """
        Leia mängija, kellel on selles mängus kõrgeim punktisumma.
        
        Returns:
            str või None: Kõrgeima punktisummaga mängija nimi või None kui punkte pole registreeritud
        """
        return max(self.high_scores, key=self.high_scores.get, default=None)


class Statistics:
    """
    Keskne klass mängustatistika haldamiseks andmefailist.
    Pakub meetodeid mitmesuguste statistikate pärimiseks mängude ja mängijate kohta.
    """
    
    def __init__(self, filename):
        """
        Lähtesta statistika, lugedes andmeid failist.
        
        Args:
            filename (str): Mänguandmeid sisaldava faili asukoht
        """
        self.players = {}
        self.games = {}
        self.total_games = 0
        self.result_type_counts = collections.defaultdict(int)
        
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                self.total_games += 1
                game_name, players_str, result_type, results_str = line.strip().split(";")
                players = players_str.split(",")
                results = results_str.split(",")
                self.result_type_counts[result_type] += 1
                
                if game_name not in self.games:
                    self.games[game_name] = Game(game_name)
                self.games[game_name].add_play(players, result_type, results)
                
                for player in players:
                    if player not in self.players:
                        self.players[player] = Player(player)
                    won = (result_type == "points" and player in [players[i] for i, score in enumerate(map(int, results)) if score == max(map(int, results))]) or \
                          (result_type == "places" and player == results[0]) or \
                          (result_type == "winner" and player == results[0])
                    lost = (result_type in {"points", "places"} and player == results[-1])
                    self.players[player].add_game(game_name, won, lost)
    
    def _get_player_info(self, player_name, info_type):
        """
        Abimeetod mängijapõhise teabe saamiseks.
        
        Args:
            player_name (str): Mängija nimi
            info_type (str): Soovitud teabe tüüp
            
        Returns:
            Mitmesugused: Soovitud mängija teave või None, kui ei leitud
        """
        player = self.players.get(player_name)
        if not player:
            return None
            
        if info_type == "amount":
            return sum(player.games_played.values())
        if info_type == "favourite":
            return player.favourite_game()
        if info_type == "won":
            return player.wins
        return player
    
    def _get_game_info(self, game_name, info_type):
        """
        Abimeetod mängupõhise teabe saamiseks.
        
        Args:
            game_name (str): Mängu nimi
            info_type (str): Soovitud teabe tüüp
            
        Returns:
            Mitmesugused: Soovitud mängu teave või None, kui ei leitud
        """
        game = self.games.get(game_name)
        if not game:
            return None
            
        if info_type == "amount":
            return game.play_count
        if info_type == "player-amount":
            return max(game.player_counts, key=game.player_counts.get, default=0)
        if info_type == "most-wins":
            return game.most_wins()
        if info_type == "most-frequent-winner":
            return game.most_frequent_winner()
        if info_type == "most-losses":
            return game.most_losses()
        if info_type == "most-frequent-loser":
            return game.most_frequent_loser()
        if info_type == "record-holder":
            return game.record_holder()
        return game
    
    def get(self, path):
        """
        Hangi statistika vastavalt määratud teele.
        
        Args:
            path (str): Tee, mis määrab hangitava statistika
            
        Returns:
            Mitmesugused: Soovitud statistika või None, kui ei leitud
        """
        parts = path.strip("/").split("/")
        
        # Käsitle põhijuhtumeid
        if not parts or not parts[0]:
            return None
            
        # Hangi mängijate nimekiri
        if parts[0] == "players":
            return list(self.players.keys())
            
        # Hangi mängude nimekiri
        if parts[0] == "games":
            return list(self.games.keys())
            
        # Hangi mängude koguarv või tulemustüüpide loendus
        if parts[0] == "total":
            if len(parts) == 1:
                return self.total_games
            return self.result_type_counts.get(parts[1], 0)
            
        # Hangi mängija teave
        if parts[0] == "player" and len(parts) > 1:
            if len(parts) <= 2:
                return self.players.get(parts[1])
            return self._get_player_info(parts[1], parts[2])
            
        # Hangi mängu teave
        if parts[0] == "game" and len(parts) > 1:
            if len(parts) <= 2:
                return self.games.get(parts[1])
            return self._get_game_info(parts[1], parts[2])
            
        return None
