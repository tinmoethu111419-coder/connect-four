"""四目並べ（Connect Four）・2人対戦ASCII版。標準ライブラリのみ。

OとXが交互に列を指定し、下から駒が積み上がる。
縦・横・斜めのいずれかに同じ駒を4つ並べると勝ち。

【改造の入口 ★★～★★★★★】
★★：盤面サイズ変更、記号・表示変更、勝利演出。
★★★：CPUのランダム着手を追加。勝ち筋探索を追加。
★★★★：CPUが相手の3連を防ぐ、次の1手で勝つ手を選ぶ。
★★★★★：先読み探索（minimax）、評価関数の実装。

学習対象となる関数: drop_piece(), check_win(), legal_columns()。
上級者はGameを継承してCPU対戦を作ることも可能です。
"""
from __future__ import annotations

COLS, ROWS, GOAL = 7, 6, 4
DIRECTIONS = ((1, 0), (0, 1), (1, 1), (1, -1))


class ConnectFour:
    def __init__(self):
        self.reset()

    def reset(self):
        self.board = [['.' for _ in range(COLS)] for _ in range(ROWS)]
        self.turn = 'O'
        self.winner = None
        self.moves = 0

    def legal_columns(self):
        return [x for x in range(COLS) if self.board[0][x] == '.']

    def drop_piece(self, col):
        """0始まり列番号に駒を入れる。置いた座標を返し、置けなければNone。"""
        if self.winner is not None or col not in self.legal_columns():
            return None
        for row in range(ROWS - 1, -1, -1):
            if self.board[row][col] == '.':
                self.board[row][col] = self.turn
                placed = (col, row)
                self.moves += 1
                if self.check_win(col, row):
                    self.winner = self.turn
                elif not self.legal_columns():
                    self.winner = 'DRAW'
                else:
                    self.turn = 'X' if self.turn == 'O' else 'O'
                return placed
        return None

    def check_win(self, x, y):
        """直前に置いた座標から、縦横斜めの連続数を数える。"""
        piece = self.board[y][x]
        for dx, dy in DIRECTIONS:
            count = 1
            for sign in (-1, 1):
                nx, ny = x + dx * sign, y + dy * sign
                while 0 <= nx < COLS and 0 <= ny < ROWS and self.board[ny][nx] == piece:
                    count += 1
                    nx += dx * sign
                    ny += dy * sign
            if count >= GOAL:
                return True
        return False

    def render(self):
        lines = ['=== CONNECT FOUR / 四目並べ ===', ' ' + ' '.join(str(i + 1) for i in range(COLS))]
        lines += ['|' + ' '.join(row) + '|' for row in self.board]
        lines += ['+' + '-' * (COLS * 2 - 1) + '+']
        if self.winner == 'DRAW':
            lines.append('引き分け！ R:再戦 / Q:終了')
        elif self.winner:
            lines.append(f'{self.winner} の勝利！ R:再戦 / Q:終了')
        else:
            lines.append(f'{self.turn} の番です。列番号 1～{COLS} / R:再開 / Q:終了')
        return '\n'.join(lines)


def main():
    game = ConnectFour()
    while True:
        print('\n' + game.render())
        command = input('> ').strip().lower()
        if command == 'q':
            break
        if command == 'r':
            game.reset()
            continue
        if game.winner is not None:
            print('Rで再戦するか、Qで終了してください。')
            continue
        try:
            col = int(command) - 1
        except ValueError:
            print('列番号を入力してください。')
            continue
        if game.drop_piece(col) is None:
            print('そこには置けません。別の列を選んでください。')
    print('終了しました。')


if __name__ == '__main__':
    main()
