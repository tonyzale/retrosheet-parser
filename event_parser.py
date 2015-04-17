import sys


def GetGameDicts(f):
    all_games = []
    current_game = {}
    for line in f:
        line = line.replace('\r\n', '')
        split = line.split(',')
        if split[0] == 'id':
            if len(current_game):
                all_games.append(current_game)
                current_game = {}
            current_game['id'] = split[1]
        elif split[0] == 'version':
            current_game['version'] = split[1]
        elif split[0] == 'info':
            current_game.setdefault('info', {})[split[1]] = split[2]
        elif split[0] == 'start':
            current_game.setdefault('starters', {}).setdefault('visitors' if split[3] == 0 else 'home', []).append((split[1],split[4],split[5]))
        elif split[0] == 'play':
            current_game.setdefault('plays', []).append(split[1:])
        elif split[0] == 'sub' or split[0] == 'com':
            current_game.setdefault('plays', []).append(split)
        elif split[0] == 'data':
            current_game.setdefault('data', []).append(split[1:])
        else:
            print 'unknown row type: %s' % split[0]
    if len(current_game):
        all_games.append(current_game)
    return all_games


def main(argv = None):
    if argv is None:
        argv = sys.argv
    print argv
    print GetGameDicts(open(argv[1], 'r'))[0]

if __name__ == '__main__':
    sys.exit(main())

