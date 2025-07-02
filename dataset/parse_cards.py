import json
from collections import defaultdict

from fetch_cards import get_bulk_cards

card_properties = ['loyalty','color_identity','keywords','power','type_line','toughness','oracle_text','mana_cost', 'produced_mana','cmc','rarity']
color_properties = ['color_identity','produced_mana']
scalar_properties = ['loyalty','power','toughness','cmc']
variable_length_strings = ['type_line','mana_cost']
variable_length_properties = variable_length_strings + ["keywords"]

def parse_cards(fp: str | None = None) -> tuple[list, dict[str,int]]:
    """
    Fetches and parses card, data, returning and optionally serializing the parsed data.
    :param fp: filepath to save parsed data to, if None, it will not be saved.
    :return: a tuple of the (parsed data, max property lengths)
    """
    parsed_data: list = list()
    data: list = get_bulk_cards()
    max_property_lengths: dict[str,int] = dict()
    for card_property in color_properties:
        max_property_lengths[card_property] = 5
    for card_property in scalar_properties:
        max_property_lengths[card_property] = 1
    for card_property in variable_length_properties:
        max_property_lengths[card_property] = 1
    for card in data:
        if "card_faces" in card:
            continue
        else:
            card_data: dict = defaultdict(lambda: 0)
            for attribute in card_properties:
                if attribute in card:
                    card_data[attribute] = card[attribute]
                    if attribute in variable_length_properties:
                        if attribute in variable_length_strings:
                            unbracketed_list = str(card_data[attribute]).split('}')
                        else:
                            unbracketed_list = card_data[attribute]
                        if max_property_lengths[attribute] and  len(unbracketed_list) > max_property_lengths[attribute]:
                            max_property_lengths[attribute] = len(unbracketed_list)
            parsed_data.append(card_data)
    if fp is not None:
        with(open(fp,'w') as file):
            json.dump({"data": parsed_data, "max_lengths": max_property_lengths},file)
    return parsed_data, max_property_lengths

print(parse_cards(fp="parsedCards.json")[1])