import os
from configparser import ConfigParser

import LearnMathGui


class LearnMathConfiguration(object):
    CONFIGURATION_FILE = "learn_math.ini"

    DEFAULT_EQUATION_NUMBER_KEY = "DEFAULT_EQUATION_NUMBER"
    HINTS_MODE_KEY = "HINTS_MODE"
    # HINTS_MODE_KEY can be one from  [GameConfiguration.GAME_HINTS_MODE_NO_HINTS,
    #                                  GameConfiguration.GAME_HINTS_MODE_UNLIMITED,
    #                                  GameConfiguration.GAME_HINTS_MODE_MAX_NUMBER,
    #                                  GameConfiguration.GAME_HINTS_MODE_MAX_AS_PERCENT]
    # so HINTS_MODE_KEY can be one from  ["HINT_NO_HINTS", "HINTS_UNLIMITED", "HINTS_MAX_NUMBER",
    #                                     "HINTS_MAX_AS_PERCENT"]
    HINTS_VALUE_KEY = "HINTS_VALUE"
    PLAYER_NAME_KEY = "PLAYER_NAME"
    SOUNDS_ON_KEY = "SOUNDS_ENABLED"


    @staticmethod
    def loadConfigurationFromFile():
        config = ConfigParser()
        config.read(os.getcwd()+'\\learn_math.ini')
        try:
            s_den = config.get('main', LearnMathConfiguration.DEFAULT_EQUATION_NUMBER_KEY)
            den = int(s_den)
            # print(den)

            s_hm = config.get('main', LearnMathConfiguration.HINTS_MODE_KEY)
            # print(s_hm)

            s_hv = config.get('main', LearnMathConfiguration.HINTS_VALUE_KEY)
            if s_hv is None or len(s_hv) <= 0:
                hv = None
            else:
                hv = int(s_hv)
            # print(s_hv)

            s_player = config.get('main', LearnMathConfiguration.PLAYER_NAME_KEY)
            # print(s_player)

            s_sounds = config.get('main', LearnMathConfiguration.SOUNDS_ON_KEY)
            s_sounds = True if s_sounds == "1" else False
            # print(s_sounds)

            game_configuration = LearnMathGui.GameConfiguration(den, None, None, s_hm, hv, s_sounds)
            game_configuration.player_name = s_player

            return game_configuration
        except Exception as exc:
            raise exc

    @staticmethod
    def saveConfigurationToFile(game_configuration):
        # print(os.getcwd())

        config = ConfigParser()
        config.add_section('main')
        config.set('main', LearnMathConfiguration.DEFAULT_EQUATION_NUMBER_KEY,
                   str(game_configuration.default_equations))
        config.set('main', LearnMathConfiguration.HINTS_MODE_KEY, game_configuration.game_hints_mode)
        config.set('main', LearnMathConfiguration.HINTS_VALUE_KEY, str(game_configuration.game_hints_value))
        config.set('main', LearnMathConfiguration.PLAYER_NAME_KEY, game_configuration.player_name)
        config.set('main', LearnMathConfiguration.SOUNDS_ON_KEY, "1" if game_configuration.default_sound_on else "0")

        with open(os.getcwd()+'\\learn_math.ini', 'w') as f:
            config.write(f)
