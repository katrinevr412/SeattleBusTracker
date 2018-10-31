class OBAConstants:

    # for simplicity, we don't distinguish among central base, atlantic base and ryerson base.
    # same for east base and bellevue base.
    # 671~676 stand for rapid ride lines A~F.
    # TODO: add lines that use small vans like DARTs and Community Shuttles.
    KCM_CENTRAL_BASE_LINES = [
        673, 674, 675,  # C, D, E lines
        1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12,
        13, 14, 15, 17, 18, 19, 21, 24,
        26, 27, 28, 29, 33, 36, 37, 40, 43,
        44, 45, 47, 48, 49, 55, 56, 57, 60,
        62, 63, 64, 70, 71, 76, 106, 113, 114, 120, 121, 122,
        123, 124, 125, 128, 131, 132, 214, 303
    ]

    KCM_NORTH_BASE_LINES = [
        31, 32, 41, 65, 67, 73, 74, 75, 77, 78, 167,
        301, 304, 308, 309,
        312, 316, 330, 331, 342, 345, 346, 347, 348, 355, 
        372, 373
    ]

    KCM_EAST_BASE_LINES = [
        200, 201, 204, 208, 212, 216, 217, 218, 219,
        221, 224, 226,
        232, 234, 235, 236, 237, 238, 240, 241,
        243, 244, 245, 246, 248, 249, 252, 255,
        257, 268, 269, 271, 277, 311,
        672  # B line
    ]

    KCM_SOUTH_BASE_LINES = [
        22, 50, 101, 102, 105, 107, 111, 116, 118, 119,
        143, 148, 150, 153, 154, 156, 157, 158, 159, 164,
        166, 168, 169, 177, 178, 179, 180, 181, 182, 183,
        186, 187, 190, 192, 193, 197,
        671, 676  # A and F lines
    ]

    KCM_SPECIAL_LINES = [
        628, 629, 630, 631, 632, 634, 635, 636, 637,
        661, 773, 775, 823, 824, 886, 887, 888, 889,
        891, 892, 893, 894, 895, 901, 903, 906, 907,
        908, 910, 913, 914, 915, 916, 917, 930, 931,
        952, 980, 981, 982, 984, 986, 987, 988, 989,
        994, 995
    ]

    ALL_KCM_LINES = KCM_CENTRAL_BASE_LINES + KCM_EAST_BASE_LINES + KCM_SOUTH_BASE_LINES + KCM_NORTH_BASE_LINES + KCM_SPECIAL_LINES

    # Sound transit lines: K - King County Metro, C - Community Transit, P - Pierce Transit
    SOUND_TRANSIT_K_LINES = [
        522, 540, 541, 542, 545, 550, 554, 555, 556
    ]

    SOUND_TRANSIT_C_LINES = [
        510, 511, 512, 513, 532, 535
    ]

    SOUND_TRANSIT_P_LINES = [
        560, 566, 567, 574, 577, 578, 580,
        586, 590, 592, 594, 595, 596
    ]

    ALL_SOUND_TRANSIT_LINES = SOUND_TRANSIT_C_LINES + SOUND_TRANSIT_K_LINES + SOUND_TRANSIT_P_LINES

    COMMUNITY_TRANSIT_LINES = [
        101, 105, 106, 107, 109, 111, 112, 113, 115, 116,
        119, 120, 130, 196, 201, 202, 209, 220, 222, 227,
        230, 240, 247, 270, 271, 280, 402, 405, 410, 412,
        413, 415, 416, 417, 421, 422, 424, 425, 435, 701,
        810, 821, 855, 860, 871, 880
    ]

    PIERCE_TRANSIT_LINES = [
        1, 10, 100, 101, 102, 11, 13, 15, 16, 2, 202, 206,
        212, 214, 28, 3, 4, 400, 402, 409, 41, 42, 425,
        45, 48, 497, 500, 501, 52, 53, 54, 55, 57, 63
    ]

    KCM = '1'
    ST = '40'
    CT = '29'
    PT = '3'

    CT_LINE_INDICATOR = 'C'
    PT_LINE_INDICATOR = 'P'

    OBA_VEHICLE_ID_PREFIX = {
        KCM: 'King County Metro',
        ST: 'Sound Transit',
        CT: 'Community Transit',
        PT: 'Pierce Transit'
    }

    TRACKING_AGENCIES = [
        KCM, ST, CT, PT
    ]

    QUERY_INTERVAL = 0.11

    UNKNOWN = 'UNKNOWN'

    SHORT_NAME_EXCEPTIONS = {
        'A Line': '671',
        'B Line': '672',
        'C Line': '673',
        'D Line': '674',
        'E Line': '675',
        'F Line': '676',
        'Redmond Loop': '632',
        'Trailhead Direct Issaquah Alps': '634',
        'Trailhead Direct Mailbox Peak': '637',
        'Trailhead Direct Mt. Si': '636',
        'Swift': '701'
    }

    TRACKING_LINES_FOR_BASES = {
        # KCM
        # c, n, s and e mean Central, North, South and East base respectively.
        # x means special buses (DART, Community Shuttle, etc.)
        # 'kcm' is an alias for all bases in KCM
        'c': [str(line) for line in KCM_CENTRAL_BASE_LINES],
        'n': [str(line) for line in KCM_NORTH_BASE_LINES],
        's': [str(line) for line in KCM_SOUTH_BASE_LINES],
        'e': [str(line) for line in KCM_EAST_BASE_LINES],
        'x': [str(line) for line in KCM_SPECIAL_LINES],
        'kcm': [str(line) for line in ALL_KCM_LINES],

        # ST
        # stk: KCM-like buses, stc: CT-like buses, stp: PT-like buses
        # (x-like means the letter following the vehicle number on the vehicle)
        # 'st' is an alias for all bases in ST
        'stk': [str(line) for line in SOUND_TRANSIT_K_LINES],
        'stc': [str(line) for line in SOUND_TRANSIT_C_LINES],
        'stp': [str(line) for line in SOUND_TRANSIT_P_LINES],
        'st': [str(line) for line in ALL_SOUND_TRANSIT_LINES],

        # CT
        'ct': [CT_LINE_INDICATOR + str(line) for line in COMMUNITY_TRANSIT_LINES],

        # PT
        'pt': [PT_LINE_INDICATOR + str(line) for line in PIERCE_TRANSIT_LINES]
    }

    TRACKING_AGENCIES_FOR_BASES = {
        'c': [KCM],
        'n': [KCM],
        's': [KCM],
        'e': [KCM],
        'x': [KCM],
        'kcm': [KCM],
        'stk': [ST, KCM],
        'stc': [ST, CT],
        'stp': [ST],
        'st': [ST, KCM, CT],
        'ct': [CT, ST],
        'pt': [PT]
    }
