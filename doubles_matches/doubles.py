import random
import csv
import argparse

def make_matches(player_num, games_per_player):
    players = player_num
    # 複数のゲームで同じ4プレイヤーの組み合わせとなることを許すか？
    allow_same_player_combination = True
    # 複数のゲームで同じペアとなることを許すか？
    allow_same_pair = False
    # 3ゲーム以上連続となるプレイヤーを許すか？
    allow_three_times_in_a_row = False
    # 前のゲームから連続となるプレイヤーを何名まで許すか？
    allowed_same_players_in_next_game = 2
    # 試行回数
    TRIALS = 100

    # 全プレイヤーの参加ゲーム数が同じとなるように実施ゲーム数を求める
    games = int(players * games_per_player / 4)

    # 試行を繰り返して条件を満たす対戦表（ゲーム一覧）を求める

    # 条件を満たす対戦表が見つかったか？
    is_success = False
    for i in range(TRIALS):
        # 今回の試行で登録済みの対戦表
        game_list = []

        # 条件検証用変数

        # ゲーム数が残っているプレイヤー一覧
        player_list = list(range(players))
        # 各プレイヤーの参加ゲーム数
        player_count = dict(zip(player_list, [0] * players))
        # allow_same_player_combination検証用の登録済みゲーム集合
        game_set = set()
        # allow_same_pair検証用の登録済みペア集合
        pair_set = set()

        # ゲーム数が残っているプレイヤーからランダムに4つ選択して、
        # 条件を満たす場合に対戦表に登録する。

        for i in range(TRIALS):
            game = random.sample(player_list, 4)

            # allow_same_player_combination（プレイヤーの組み合わせ重複）検証
            if (not allow_same_player_combination and tuple(game) in game_set):
                continue
            # allow_same_pair（ペアの組み合わせ重複）検証
            pair_1 = frozenset(game[0:2])
            pair_2 = frozenset(game[2:4])
            if (not allow_same_pair and  (pair_1 in pair_set or pair_2 in pair_set)):
                continue
            # allow_three_times_in_a_row（3ゲーム連続プレイ）検証
            if(not allow_three_times_in_a_row and len(game_list) > 1):
                x = set(game_list[-2]) & set(game_list[-1]) & set(game)
                if (len(x) > 0): continue
            # allowed_same_players_in_next_game（前ゲームとの重複プレイヤー数）検証
            if(len(game_list) > 0):
                same_players_in_next_game = set(game_list[-1]) & set(game)
                if (len(same_players_in_next_game) > allowed_same_players_in_next_game):
                    continue

            # 対戦表に発見した条件を満たすゲームを追加する。
            game_list.append(game)
            # 実施ゲーム数分の対戦表ができた場合は完了となる。
            if (len(game_list) == games):
                is_success = True
                break

            # 条件検証用変数を更新する。
            for player in game:
                player_count[player] += 1
            for player in player_list[:]:
                if (player_count[player] == games_per_player):
                    player_list.remove(player) 
            game_set.add(tuple(game))
            pair_set.add(pair_1)
            pair_set.add(pair_2)

            # 残プレイヤー数が3以下となった場合は次のゲームを作れないため試行を中断する。
            if (len(player_list) <= 3): 
                break
 
        if (is_success): break

    # 結果出力

    if (is_success):
        print('%dプレイヤー %dゲーム（1プレイヤーあたり%dゲーム）の対戦表：'
                % (players, len(game_list), games_per_player))

        return game_list
    else:
        print("条件を満たす対戦表を作成できませんでした。")
        return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--names_csv_path',
                        help="名前が書かれたcsvファイルのパス",
                        type=str, default='./names.csv')
    parser.add_argument('--games_per_player','-g',
                        help="一人当たりのゲーム数",
                        type=int, default=4)
    parser.add_argument('--players','-p',
                        help="参加人数",
                        type=int, default=10)
    parser.add_argument('--output_path',
                        help="出力となるcsvファイルのパス",
                        type=str, default='./matches.csv')
    
    args = parser.parse_args()

    with open(args.names_csv_path) as f:
        reader = csv.reader(f)
        l = [row for row in reader]
        names = l[0]
        if len(names) != args.players:
            print("参加人数とcsvファイルに書かれた人数が一致しません")
            exit()
    
    games = make_matches(args.players, args.games_per_player)
    if games:
        matches = []
        for i, game in enumerate(games):
            print(f'第{i+1}試合 {names[game[0]]} & {names[game[1]]} vs {names[game[2]]} & {names[game[3]]}')
            matches.append([f'第{i+1}試合',f'{names[game[0]]}',f'{names[game[1]]}','vs',f'{names[game[2]]}',f'{names[game[3]]}'])
        with open(args.output_path, 'w') as f:
            writer = csv.writer(f)
            writer.writerows(matches)
    else:
        exit()