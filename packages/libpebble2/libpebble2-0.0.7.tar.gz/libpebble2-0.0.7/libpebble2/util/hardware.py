__author__ = 'katharine'


class PebbleHardware(object):
    UNKNOWN = 0
    TINTIN_EV1 = 1
    TINTIN_EV2 = 2
    TINTIN_EV2_3 = 3
    TINTIN_EV2_4 = 4
    TINTIN_V1_5 = 5
    BIANCA = 6
    SNOWY_EVT2 = 7
    SNOWY_DVT = 8

    TINTIN_BB = 0xFF
    TINTIN_BB2 = 0xFE
    SNOWY_BB = 0xFD
    SNOWY_BB2 = 0xFC

    PLATFORMS = {
        UNKNOWN: 'unknown',
        TINTIN_EV1: 'aplite',
        TINTIN_EV2: 'aplite',
        TINTIN_EV2_3: 'aplite',
        TINTIN_EV2_4: 'aplite',
        TINTIN_V1_5: 'aplite',
        BIANCA: 'aplite',
        SNOWY_EVT2: 'basalt',
        SNOWY_DVT: 'basalt',
        TINTIN_BB: 'aplite',
        TINTIN_BB2: 'aplite',
        SNOWY_BB: 'basalt',
        SNOWY_BB2: 'basalt',
    }

    @classmethod
    def hardware_platform(cls, hardware):
        return cls.PLATFORMS.get(hardware, 'unknown')
