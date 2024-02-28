import asyncio
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Coroutine, Any, List, Tuple, Optional, Union


class DeckRequestStatus(Enum):
    ALL_DECKS_FOUND = 0
    DECK_NOT_FOUND = 1
    RANGE_INVALID = 2


@dataclass
class Card:
    question: str
    answer: str
    meaning: str
    instruction: str


@dataclass
class CardGetter:
    get: Callable[[int],  Coroutine[Any, Any, Card]]
    length: int
    memory_array: list[Card]


@dataclass
class Deck:
    name: str
    questionCreationStrategy: str
    cards: CardGetter = field(default_factory=CardGetter)


async def create_card_getter_from_in_memory_array(array: list[dict]) -> CardGetter:
    async def get(i: int) -> Card:
        return Card(**array[i])

    return CardGetter(
        get=get,
        length=len(array),
        memory_array=[Card(**card_data) for card_data in array]
    )


async def prepare_cards(data: json) -> List[dict]:
    assert "cards" in data, "Key 'cards' not found in data"

    return [
        {
            "question": card['question'],
            "answer": card['answer'],
            "meaning": card['meaning'],
            "instruction": data["instructions"]
        }
        for card in data["cards"]
    ]


async def prepare_deck(path: str = '', name: str = '') -> Union[
    tuple[DeckRequestStatus, str], tuple[DeckRequestStatus, Optional[Deck]]]:
    if name == "n2":
        path = 'resources/quiz_data/n2.json'
    else:
        return create_deck_notfound_status(name)
    # i should here change for the search of quiz data, but for now i leave it as it is
    with open(path, 'r', encoding="utf-8") as json_file:
        data = json.load(json_file)

    assert "name" in data, "Key 'name' not found in data"
    assert "questionCreationStrategy" in data, "Key 'questionCreationStrategy' not found in data"

    cards: list[dict] = await prepare_cards(data)

    card_getter = await create_card_getter_from_in_memory_array(cards)

    deck = Deck(
        name=data["name"],
        questionCreationStrategy=data["questionCreationStrategy"],
        cards=card_getter
    )
    return create_deck_found_status(deck)


def create_deck_found_status(deck: Deck) -> Tuple[DeckRequestStatus, Optional[Deck]]:
    return DeckRequestStatus.ALL_DECKS_FOUND, deck


def create_deck_notfound_status(missingName: str) -> Tuple[DeckRequestStatus, str]:
    return DeckRequestStatus.DECK_NOT_FOUND, missingName


async def main() -> None:
    quiz_data = 'resources/quiz_data/n2.json'
    _, deck = await prepare_deck(quiz_data)
    card: Card = await deck.cards.get(100)
    print(card.instruction)
    print(card.question)
    print(card.answer)
    print(card.meaning)
    print(deck.cards.length)
    print(deck.name)
    print(deck.questionCreationStrategy)

if __name__ == '__main__':
    asyncio.run(main())

# TODO
"""
create index set of this array
shuffle it if needed
then just pop or what form set thats it
"""