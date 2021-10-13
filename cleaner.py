





## MOVE IMAGE REJECTION AND PADDING TO SEPARATE FILE / DOCUMENT
## MOVE TRANSFORM DEFAULTS OUTSIDE OF CLASS AND TO WHERE YOU CALL IT



to_drop_black = [
    "JPMorgan Chase", "Sony", "BlackRock", "Volvo Group",
    "Panasonic", "Kering", "Ericsson", "Macquarie Group",
    "Norfolk Southern", "BASF", "Activision Blizzard", "Adidas",
    "Nissan Motor", "Advanced Micro Devices", "Renault", "BOE Technology Group",
    "Simon Property Group", "Assa Abloy", "Coal India", "T Rowe Price",
    "Marriott International", "L Brands", "Western Digital", "DaVita",
    "Autodesk", "Arrow Electronics", "Agilent Technologies", "Asustek Computer",
    "IDEXX Laboratories", "Zebra Technologies", "Bancolombia", "First Quantum Minerals",
    "Citrix Systems", "CrowdStrike", "DocuSign", "Palantir Technologies",
    "AECOM Technology", "CoStar Group", "JD Sports Fashion", "Marvell Technology Group",
    "Frost Bankers", "Nanto Bank", "Toll Brothers", "Unity Software"
]

to_drop_building = [
    "China State Construction Engineering", "China Railway Construction", "Westinghouse Air Brake Technologies",
    "Nomura Research Institute", "Hotai Motor", "Taiwan Cement", "Chang Hwa Bank",
    "China Railway Signal & Communication", "DGB Financial Group"
]

to_drop_all = to_drop_black
to_drop_all.append(to_drop_building)


        info_cleaned = [item for item in info if item['company_name'] not in to_drop_all]
