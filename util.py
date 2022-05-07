from riotwatcher import LolWatcher, ApiError
import pandas as pd
from config import API_KEY, REGION, LIST_FIELDS
import copy


def get_data_from_account(account_name):
    try:
        lol_watcher = LolWatcher(API_KEY)

        summoner = lol_watcher.summoner.by_name(REGION, account_name)
        summoner_league = lol_watcher.league.by_summoner(REGION, summoner['id'])
        # my_ranked_stats = lol_watcher.league.by_summoner(REGION, summoner['id'])

        summoner_matches = lol_watcher.match.matchlist_by_puuid(REGION, summoner['puuid'], queue=420, count=1)
        print(len(summoner_matches))
        df = get_player_data_from_matches(lol_watcher, summoner_matches, summoner['puuid'], summoner_league)
        return df
    except Exception as error:
        print(f"Error al tratar los partidos de la cuenta {account_name}: {str(error)}")
        return pd.DataFrame()


def get_challenge_fields(match_result, participant):
    for key_challenge in participant[key].keys():
        if key_challenge not in LIST_FIELDS:
            continue
        match_result[key_challenge] = participant[key][key_challenge]


def get_participant_fields(match_result, participant):
    global key
    for key in participant.keys():
        if key == 'challenges':
            get_challenge_fields(match_result, participant)
        elif key in LIST_FIELDS:
            match_result[key] = participant[key]



def get_player_data_fields_from_match(match_result, match_detail):
    participants = []
    for participant in match_detail['info']['participants']:
        new_participant = copy.deepcopy(match_result)
        get_participant_fields(new_participant, participant)
        participants.append(new_participant)
    return participants


def get_player_data_from_matches(lol_watcher, player_matches, summoner, summoner_league):
    match_result_list = []
    for match in player_matches:
        try :
            match_detail = lol_watcher.match.by_id(REGION, match)
            match_result = {}
            match_result['puuid_current_summoner'] = summoner
            match_result['queue'] = summoner_league[0]['queueType']
            match_result['tier'] = summoner_league[0]['tier']
            match_result['rank'] = summoner_league[0]['rank']
            participants = get_player_data_fields_from_match(match_result, match_detail)

            match_result_list += participants
        except Exception as error:
            print(f"fallo al obtener la partida {match}. Error: {str(error)}")
    df = pd.DataFrame(match_result_list)
    return df

