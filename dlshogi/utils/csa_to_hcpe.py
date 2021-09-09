from cshogi import *
from cshogi import CSA
import numpy as np
import os
import glob
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('csa_dir')
parser.add_argument('hcpe')
parser.add_argument('--out_draw', action='store_true')
parser.add_argument('--out_maxmove', action='store_true')
parser.add_argument('--out_noeval', action='store_true')
parser.add_argument('--out_mate', action='store_true')
parser.add_argument('--eval', type=int)
parser.add_argument('--filter_moves', type=int, default=50)
parser.add_argument('--filter_rating', type=int, default=3500)
args = parser.parse_args()

filter_moves = args.filter_moves
filter_rating = args.filter_rating
endgames = ['%TORYO', '%KACHI']
if args.out_draw:
    endgames.append('%SENNICHITE')
if args.out_maxmove:
    endgames.append('%JISHOGI')

csa_file_list = glob.glob(os.path.join(args.csa_dir, '**', '*.csa'), recursive=True)

hcpes = np.zeros(513, HuffmanCodedPosAndEval)

f = open(args.hcpe, 'wb')

board = Board()
kif_num = 0
position_num = 0
for filepath in csa_file_list:
    for kif in CSA.Parser.parse_file(filepath):
        if kif.endgame not in endgames or len(kif.moves) < filter_moves:
            continue
        if filter_rating > 0 and min(kif.ratings) < filter_rating:
            continue

        board.set_sfen(kif.sfen)
        p = 0
        try:
            for i, (move, score, comment) in enumerate(zip(kif.moves, kif.scores, kif.comments)):
                assert board.is_legal(move)
                if not args.out_noeval and comment == '':
                    board.push(move)
                    continue
                hcpe = hcpes[p]
                board.to_hcp(hcpe['hcp'])
                assert abs(score) <= 200000
                eval = min(32767, max(score, -32767))
                if args.eval and abs(eval) > args.eval:
                    break
                hcpe['eval'] = eval if board.turn == BLACK else -eval
                hcpe['bestMove16'] = move16(move)
                hcpe['gameResult'] = kif.win
                p += 1
                if not args.out_mate and abs(score) == 100000:
                    break
                board.push(move)
        except:
            print(f'skip {filepath}:{i}:{move_to_usi(move)}:{score}')
            continue

        if p == 0:
            continue

        hcpes[:p].tofile(f)

        kif_num += 1
        position_num += p

print('kif_num', kif_num)
print('position_num', position_num)
