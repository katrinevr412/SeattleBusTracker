class Constants:

    # for simplicity, we don't distinguish among central base, atlantic base and ryerson base.
    # same for east base and bellevue base.
    # 671~676 stand for rapid ride lines A~F.
    CENTRAL_BASE_LINES = [
        673, 674, 675,  # C, D, E lines
        1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12,
        13, 14, 15, 17, 18, 19, 21, 22, 24,
        26, 27, 28, 29, 33, 36, 37, 40, 43,
        44, 45, 47, 48, 49, 55, 56, 57, 60,
        62, 63, 64, 70, 71, 73, 76, 106, 120, 121, 122,
        123, 124, 125, 128, 131, 132, 214
    ]

    NORTH_BASE_LINES = [
        31, 32, 41, 65, 67, 74, 75, 77, 78,
        212, 216, 217, 218, 219, 301, 303, 304, 308, 309,
        311, 312, 316, 330, 331, 342, 345, 346, 347, 348,
        355, 372, 373
    ]

    EAST_BASE_LINES = [
        114, 200, 201, 204, 208, 221, 224, 226,
        232, 234, 235, 236, 237, 238, 240, 241,
        243, 244, 245, 246, 248, 249, 252, 255,
        257, 268, 269, 271, 277,
        672,  # B line
        522, 540, 541, 542, 545, 550, 554, 555, 556  # Sound Transit records run mostly eastbound lines. And they borrow vehicles from east base.
    ]

    SOUTH_BASE_LINES = [
        50, 101, 102, 105, 107, 111, 113, 116, 118, 119,
        143, 148, 150, 153, 154, 156, 157, 158, 159, 164,
        166, 167, 168, 169, 177, 178, 179, 180, 181, 182, 183,
        186, 187, 190, 192, 193, 197,
        671, 676  # A and F lines
    ]

    # regular lines are lines that operate Mon~Sun and 24h.
    REGULAR_LINES = [
        671, 672, 673, 674, 675, 676,  # all rapid rides are regular lines
        1, 2, 3, 4, 5, 7, 8, 10, 11, 12,
        13, 14, 24, 26, 27, 28, 36, 40, 44,
        45, 48, 49, 62, 70, 71, 73, 106, 120, 124, 125, 128,
        131, 132,
        31, 32, 41, 65, 67, 75, 345, 346, 347, 348, 372,
        221, 224, 226, 234, 235, 238, 240, 241, 245, 248,
        249, 255, 271,
        50, 101, 105, 107, 148, 150, 156, 164, 166, 169,
        180, 181, 182, 183,
        522, 545, 550, 554
    ]

    DEFAULT_INBOUND_LINEID_SUFFIX = 2
    DEFAULT_OUTBOUND_LINEID_SUFFIX = 3
    MAXIMUM_LINE_QUERY = 2  # KCM api's limit is 4, but we send request for inbound and outbound at a time.

    ALL_LINES = CENTRAL_BASE_LINES + EAST_BASE_LINES + NORTH_BASE_LINES + SOUTH_BASE_LINES

    IN_OUT_BOUND_SUFFIX_MAPPING = {
         4: [
             8, 31, 32, 45, 50, 78, 156, 164, 168, 181, 186,
             208, 212, 214, 216, 217, 218, 219, 224, 226, 232,
             248, 249, 252, 255, 257, 268, 271, 277, 311, 330, 331,
             540, 541, 542, 545, 550, 554, 555, 556, 672, 676
         ]
    }
