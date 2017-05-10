import fetch_charity_data
import titlecase


def test_titlecase():
    names = [
        "The St. Endellion Festivals Trust",
        "Friends of North Heath CP School",
        "A M Challis Trust Ltd",
        "Majlis Al-Falah Trust (UK)",
        "Kilby Woodland Trust Ltd",
        "Biocentre UK",
        "Bury St.Edmunds Methodist Circuit",
        "Ridgeway School PTA",
        "St Matthews High Brooms PFA",
        "Friends of the Gwyn Hall, Neath",
        "1st Shifnal Scout Group",
        "SV2G (St Vincent & the Grenadines, 2nd Generation",
        "103rd Reading (Oxford Road) Scout Group",
        "The 4th London Collection",
        "Dr Smith's Charity",
        "The PDC Trust",
        "35th Norwich Sea Scouts",
        "Adept - Yorkshire ADHD and Learning Ability Support Group",
        "Tuesday O'Hara Fund",
        "Ysgol Cwm-Y-Glo School P.T.A.",
        "Clwb Llawen Y Llys",
        "Activities 4 Children (Sheffield)Limited",
        "Prince Albert II of Monaco Foundation (GB)",
        "The Drs Hady Bayoumi & Rashida Mangera Charitable Trust",
        "KT's Fund",
        "St Michaels CE (VC) Combined School Fund",
        "You're the Outdoors 4 Today Onwards and Fairfield Voice CIC",
        "1st Lytham St Annes (St Cuthbert's) Scout Group"
    ]
    
    for n in names:
        assert n == titlecase.titlecase( n.upper(), fetch_charity_data.title_exceptions )




