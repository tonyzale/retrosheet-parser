import collections
import json
import sys

Starter = collections.namedtuple('Starter', 'player batting_pos pos')
Play = collections.namedtuple('Play', 'inning player balls strikes events result')
Sub = collections.namedtuple('Sub', 'player team batting_pos pos')
Comment = collections.namedtuple('Comment', 'comment')
Data = collections.namedtuple('Data', 'type player data')

PITCH_CALL_STRIKE = 'STRIKE'
PITCH_CALL_BALL = 'BALL'
PITCH_CALL_UNKNOWN = 'UNKNOWN'
PITCH_CALL_NOT_PITCH = 'NOT PITCH'

Event = collections.namedtuple('Event', 'code desc pitch_call')

class Events:
    CALLED_STRIKE = Event('C', 'called strike', PITCH_CALL_STRIKE)
    SWINING_STRIKE = Event('S', 'swinging strike', PITCH_CALL_STRIKE)
    BALL = Event('B', 'ball', PITCH_CALL_BALL)
    FOUL = Event('F', 'foul', PITCH_CALL_STRIKE)
    PICKOFF_FIRST = Event('1', 'pickoff first', PITCH_CALL_NOT_PITCH)
    PICKOFF_SECOND = Event('2', 'pickoff second', PITCH_CALL_NOT_PITCH)
    PICKOFF_THIRD = Event('3', 'pickoff third', PITCH_CALL_NOT_PITCH)
    CATCHER_PICKOFF_FIRST = Event('1+', 'catcher pickoff first', PITCH_CALL_NOT_PITCH)
    CATCHER_PICKOFF_SECOND = Event('2+', 'catcher pickoff second', PITCH_CALL_NOT_PITCH)
    CATCHER_PICKOFF_THIRD = Event('3+', 'catcher pickoff third', PITCH_CALL_NOT_PITCH)
    FOUL_BUNT = Event('L', 'foul bunt', PITCH_CALL_STRIKE)
    MISSED_BUNT = Event('M', 'missed bunt', PITCH_CALL_STRIKE)
    SWINGING_STRIKE_PITCHOUT = Event('Q', 'swinging strike on pitchout', PITCH_CALL_STRIKE)
    FOUL_PITCHOUT = Event('R', 'foul on pitchout', PITCH_CALL_STRIKE)
    INTENTIONAL_BALL = Event('I', 'intentional ball', PITCH_CALL_BALL)
    PITCHOUT = Event('P', 'pitchout', PITCH_CALL_BALL)
    HBP = Event('H', 'hit by pitch', PITCH_CALL_BALL)
    STRIKE = Event('K', 'strike of unknown type', PITCH_CALL_STRIKE)
    UNKNOWN_PITCH = Event('U', 'unknown pitch', PITCH_CALL_UNKNOWN)
    SEPARATOR = Event('.', 'non-pitch event', PITCH_CALL_NOT_PITCH)
    RESULT = Event('X', 'result', PITCH_CALL_UNKNOWN)

EVENTS = {}
# Get the non-private members of Events and use to populate EVENTS dict
for el in dir(Events):
    if el[0] != '_':
        event = Events.__dict__[el]
        EVENTS[event.code] = event

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
            current_game.setdefault('starters', {}).setdefault('visitors' if (split[3] == '0') else 'home', []).append(
                Starter(player=split[1], batting_pos=split[4], pos=split[5]))
        elif split[0] == 'play':
            current_game.setdefault('plays', []).append(
                Play(inning=split[1] + ('t' if split[2] == '0' else 'b'), player=split[3], balls=int(split[4][0]), strikes=int(split[4][1]), events=split[5], result=split[6]))
        elif split[0] == 'sub':
            current_game.setdefault('plays', []).append(Sub(player=split[1],team=split[3],batting_pos=split[4],pos=split[5]))
        elif split[0] == 'com':
            current_game.setdefault('plays', []).append(Comment(split[1]))
        elif split[0] == 'data':
            current_game.setdefault('data', []).append(Data(*split[1:]))
        else:
            print 'unknown row type: %s' % split[0]
    if len(current_game):
        all_games.append(current_game)
    return all_games


def main(argv = None):
    if argv is None:
        argv = sys.argv
    # print json.dumps(GetGameDicts(open(argv[1], 'r')))
    print GetGameDicts(open(argv[1], 'r'))[1]

if __name__ == '__main__':
    sys.exit(main())

