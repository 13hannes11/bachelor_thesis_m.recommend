from enum import Enum
class HEIMISCH(Enum):
    NIEDRIG = "62bcc15f-5f39-4239-963a-455498c34f79"
    MITTEL = "066372f5-9b21-46a3-a62a-76be0afd8f4e"
    HOCH = "2e94ef17-7ea1-42e0-b070-bba3a8debfd8"

class KLIMA(Enum):
    NIEDRIG = "1a02a295-5afd-427a-bf1e-2b8065687380"
    MITTEL = "6f3a5204-1276-40f9-84dc-c8e139e5402d"
    HOCH = "5bd172ba-0076-456e-9ee2-0b81780a5da0"

class VERWERTBAR(Enum):
    NIEDRIG = "79cb7c2f-6b90-4991-8c9c-9a28f1b31cc8"
    MITTEL = "b17eceb1-1cd5-4c11-b398-c6834e4e2ed1"
    HOCH = "3fb4ae3d-c892-4025-815f-6b6074ac3d3c"

class AUFWAND(Enum):
    NIEDRIG = "a755ba0d-fb8d-475a-a0f9-5ca267fd479f"
    MITTEL = "653b4832-6647-426d-a18e-ee444ba67979"
    HOCH = "dcb34d08-06f2-4426-a3a9-039cec1e6f6d"

class MENGE(Enum):
    NIEDRIG = "9e70ea9a-1311-48db-9238-cbc98da1ed2b"
    MITTEL = "5de4ee9e-14a5-4b50-aa36-6efc39cdc24c"
    HOCH = "09594573-6fc5-4c62-9d5c-84b4ccf817a1"

class PREIS(Enum):
    NIEDRIG = "8d2f5efe-db35-4b4d-9591-cf797335e3ba"
    MITTEL = "c7b0f02c-9afe-4ef6-9af0-b7c193b08e93"
    HOCH = "c6bd1fd3-8f0f-4d7d-aa8a-86ec00cb7853"

class ERFAHRUNG(Enum):
    NIEDRIG = "d59c52cf-0eb1-4ad9-9228-c5100c2b6237"
    MITTEL = "311389a2-c4b7-4a13-bf5a-04a1befad0e9"
    HOCH = "f08b7cd1-c470-4d6e-951d-a69a02b04849"

not_with = [
    (HEIMISCH.MITTEL, KLIMA.HOCH),
    (HEIMISCH.MITTEL, VERWERTBAR.HOCH),
    (HEIMISCH.HOCH, KLIMA.HOCH),
    (HEIMISCH.HOCH, VERWERTBAR.MITTEL),
    (HEIMISCH.HOCH, VERWERTBAR.HOCH),
    (HEIMISCH.HOCH, MENGE.HOCH),
    (HEIMISCH.HOCH, PREIS.NIEDRIG),

    (KLIMA.MITTEL, VERWERTBAR.HOCH),
    (KLIMA.HOCH, VERWERTBAR.MITTEL),
    (KLIMA.HOCH, VERWERTBAR.HOCH),
    (KLIMA.HOCH, MENGE.HOCH),
    (KLIMA.HOCH, PREIS.MITTEL),
    (KLIMA.HOCH, PREIS.NIEDRIG),

    (VERWERTBAR.NIEDRIG, MENGE.HOCH),
    (VERWERTBAR.NIEDRIG, PREIS.MITTEL),
    (VERWERTBAR.NIEDRIG, PREIS.NIEDRIG),
    (VERWERTBAR.HOCH, ERFAHRUNG.HOCH),

    (AUFWAND.NIEDRIG, MENGE.HOCH), 
    (AUFWAND.NIEDRIG, PREIS.MITTEL),
    (AUFWAND.NIEDRIG, PREIS.NIEDRIG),
    (AUFWAND.MITTEL, ERFAHRUNG.MITTEL),
    (AUFWAND.MITTEL, ERFAHRUNG.HOCH), 
    (AUFWAND.HOCH, ERFAHRUNG.MITTEL),
    (AUFWAND.HOCH, ERFAHRUNG.HOCH),

    (MENGE.NIEDRIG, PREIS.NIEDRIG),
    (MENGE.NIEDRIG, PREIS.MITTEL),
    (MENGE.MITTEL, PREIS.NIEDRIG),
    (MENGE.MITTEL, PREIS.MITTEL),
    (MENGE.HOCH, ERFAHRUNG.MITTEL),
    (MENGE.HOCH, ERFAHRUNG.HOCH),

]
counter = 0
string = ""

for heimisch in [HEIMISCH.NIEDRIG, HEIMISCH.MITTEL, HEIMISCH.HOCH]:
    for klima in [KLIMA.NIEDRIG, KLIMA.MITTEL, KLIMA.HOCH]:
        for verwertbar in [VERWERTBAR.NIEDRIG, VERWERTBAR.MITTEL, VERWERTBAR.HOCH]:
            for aufwand in [AUFWAND.NIEDRIG, AUFWAND.MITTEL, AUFWAND.HOCH]:
                for menge in [MENGE.NIEDRIG, MENGE.MITTEL, MENGE.HOCH]:
                    for preis in [PREIS.NIEDRIG, PREIS.MITTEL, PREIS.HOCH]:
                        for erfahrung in [ERFAHRUNG.NIEDRIG, ERFAHRUNG.MITTEL, ERFAHRUNG.HOCH]:
                            plus = True
                            if (heimisch, klima) in not_with:
                                plus = False
                            if (heimisch, verwertbar) in not_with:
                                plus = False
                            if (heimisch, aufwand) in not_with:
                                plus = False
                            if (heimisch, menge) in not_with:
                                plus = False
                            if (heimisch, preis) in not_with:
                                plus = False
                            if (heimisch, erfahrung) in not_with:
                                plus = False
                            
                            if (klima, verwertbar) in not_with:
                                plus = False
                            if (klima, aufwand) in not_with:
                                plus = False
                            if (klima, menge) in not_with:
                                plus = False
                            if (klima, preis) in not_with:
                                plus = False
                            if (klima, erfahrung) in not_with:
                                plus = False
                            
                            if (verwertbar, aufwand) in not_with:
                                plus = False
                            if (verwertbar, menge) in not_with:
                                plus = False
                            if (verwertbar, preis) in not_with:
                                plus = False
                            if (verwertbar, erfahrung) in not_with:
                                plus = False
                            
                            if (aufwand, menge) in not_with:
                                plus = False
                            if (aufwand, preis) in not_with:
                                plus = False
                            if (aufwand, erfahrung) in not_with:
                                plus = False                            
                            
                            if (menge, preis) in not_with:
                                plus = False
                            if (menge, erfahrung) in not_with:
                                plus = False
                            
                            if (preis, erfahrung) in not_with:
                                plus = False
                            if plus:
                                counter += 1
                                print("{}, {}, {}, {}, {}, {}, {}".format(heimisch, klima, verwertbar, aufwand, menge, preis, erfahrung))
                                string += '"' + str(counter) + '":' + "{ 'configuration': [" + heimisch.value + "," + klima.value + "," + verwertbar.value + "," + aufwand.value + "," + menge.value + "," + preis.value + "," + erfahrung.value + "], 'variables': []},"

print(counter)
#print(string)                                               
