import imgui

# Misc Stuff
import json

# Filestuffs
import os
import pathlib
from MiscFuncs import File

# Card Stuff
from Cardstuffs import *

Cards = ["Ace", "King", "Queen", "Jack", "10", "9", "8", "7", "6", "5", "4", "3", "2"]

def GenSuit():
    """
        Create card list for each suit
    """
    return [{"Value": val, "Edition": "Default", "Seal": "None", "Sticker": "None", "Enhancements": "None"} for val in Cards]

GenSuit()

def CreateDeck(Name,
               Description,
               Discards=3,
               Hands=4,
               Cash=4,
               JokerSlots=5,
               ConsumableSlots=2
               ):
    """
        Returns a full deck json file\n

        This function does not create any source for the deck\n

        Name and Description are required for it to work\n
        all the other inputs are not required they all have a default value as follows\n
        Discards 3\n
        Hands 4\n
        Cash 4\n
        JokerSlots 5\n
        ConsumableSlots 2\n
    """

    # Define the full deck structure
    DeckData = {
        "Deck": {
            "Name": Name,
            "Description": Description,
            "Variables": {
                "Discards": Discards,
                "Hands": Hands,
                "Cash": Cash,
                "JokerSlots": JokerSlots,
                "ConsumableSlots": ConsumableSlots
            },
            "Cards": {
                "Hearts": GenSuit(),
                "Diamonds": GenSuit(),
                "Clubs": GenSuit(),
                "Spades": GenSuit()
            }
        }
    }

    return DeckData

DeckName = "Deck Name Here"

def DeckCreationGui():
    global DeckName

    DeckPath = pathlib.Path("Decks")
    ExistingDecks = [item.name for item in DeckPath.iterdir() if item.is_dir()]
    if not os.path.exists(DeckPath):
        os.makedirs("Decks")

    imgui.new_line()

    imgui.separator()
    imgui.same_line()
    imgui.text("Deck Creation Stuffs")

    DeckNameChanged, DeckName = imgui.input_text('Deck Name', DeckName)
    if imgui.button("Create Deck"):
        print("Existing decks:", ExistingDecks)
        for Deck in ExistingDecks:
            if DeckName == Deck:
                print("You already have a deck with this name.")
                return -1
        
        os.makedirs(f"Decks/{DeckName}/Source") # Source contains custom stuff like stickers editions seals and enhancements
        File.Create(f"Decks/{DeckName}Deck.json") # Create deck file

    return 1

def DeckEditorGui():
    if not hasattr(DeckEditorGui, "Current"):
        DeckEditorGui.Current = 0
        DeckEditorGui.Previous = -1  # force reinit on first load

    if not hasattr(DeckEditorGui, "name_buffer"):
        DeckEditorGui.name_buffer = ""
        DeckEditorGui.desc_buffer = ""
        DeckEditorGui.combo_states = {}

    imgui.separator()
    imgui.same_line()
    imgui.text("Deck Editor Stuffs")

    ExistingDecks = [item.name for item in pathlib.Path("Decks").iterdir() if item.is_dir()]
    if not ExistingDecks:
        imgui.text("No decks found.")
        return

    # Clamp to avoid index error
    DeckEditorGui.Current = min(DeckEditorGui.Current, len(ExistingDecks) - 1)
    DeckPath = ExistingDecks[DeckEditorGui.Current]

    # Load deck data
    DeckData = json.loads(File.Read(f"Decks/{DeckPath}/Deck.json"))
    Deck = DeckData["Deck"]
    Variables = Deck["Variables"]
    Cards = Deck["Cards"]

    # For detecting if anything in deckdata has changed
    OriginalDeckData = json.loads(File.Read(f"Decks/{DeckPath}/Deck.json"))

    COMBO_OPTIONS = {
        "Edition": Editions,
        "Seal": Seals,
        "Sticker": Stickers,
        "Enhancements": Enhancements
    }

    # Reset buffers if deck changed
    if DeckEditorGui.Current != DeckEditorGui.Previous:
        DeckEditorGui.name_buffer = Deck["Name"] + " " * (256 - len(Deck["Name"]))
        DeckEditorGui.desc_buffer = Deck["Description"] + " " * (512 - len(Deck["Description"]))
        DeckEditorGui.combo_states = {}
        DeckEditorGui.Previous = DeckEditorGui.Current

    if imgui.tree_node("Deck Editor", imgui.TREE_NODE_DEFAULT_OPEN):
        imgui.text("NOTE THIS CURRENTLY AUTOSAVES IMMEDIATELY")
        imgui.text("MAKE A COPY OF THE DECK IF YOUR NOT SURE IF YOU WANT TO OVERWRITE IT")

        imgui.separator()

        # Dropdown to select deck
        changed, DeckEditorGui.Current = imgui.combo("Selected Deck", DeckEditorGui.Current, ExistingDecks)

        imgui.separator()
        imgui.text("Name And Description")

        changed, DeckEditorGui.name_buffer = imgui.input_text("Deck Name", DeckEditorGui.name_buffer, 256)
        changed, DeckEditorGui.desc_buffer = imgui.input_text_multiline(
            "Description", DeckEditorGui.desc_buffer, 512, 400, 60
        )

        imgui.separator()
        imgui.text("Deck Variables")

        AnyVarsChanged = False
        for key in Variables:
            changed, value = imgui.input_int(key, Variables[key])
            if changed:
                Variables[key] = value
                AnyVarsChanged = True

        imgui.separator()
        imgui.text("Cards")
        imgui.begin_child("CardsEditor", width=950, height=500, border=True)

        for suit in Cards:
            if imgui.tree_node(suit):
                for idx, card in enumerate(Cards[suit]):
                    if imgui.tree_node(f"{suit} - {card['Value']}##{idx}"):
                        for field in ["Edition", "Seal", "Sticker", "Enhancements"]:
                            options = COMBO_OPTIONS[field]
                            key = f"{suit}_{idx}_{field}"

                            if key not in DeckEditorGui.combo_states:
                                try:
                                    DeckEditorGui.combo_states[key] = options.index(card[field])
                                except ValueError:
                                    DeckEditorGui.combo_states[key] = 0

                            selected_index = DeckEditorGui.combo_states[key]
                            clicked, new_index = imgui.combo(f"{field}##{key}", selected_index, options)

                            if clicked:
                                DeckEditorGui.combo_states[key] = new_index
                                card[field] = options[new_index]
                        imgui.tree_pop()
                imgui.tree_pop()

        imgui.end_child()

        imgui.separator()

        if DeckData != OriginalDeckData or AnyVarsChanged:
            Deck["Name"] = DeckEditorGui.name_buffer.strip()
            Deck["Description"] = DeckEditorGui.desc_buffer.strip()
            File.Overwrite(f"Decks/{DeckPath}/Deck.json", json.dumps(DeckData, indent=4))
            print(f"Saved: Decks/{DeckPath}/Deck.json")

        ### Im gonna implement propper non autosaving later for now this works
        ### if imgui.button("Save"):
        ###     Deck["Name"] = DeckEditorGui.name_buffer.strip()
        ###     Deck["Description"] = DeckEditorGui.desc_buffer.strip()
        ###     File.Overwrite(f"Decks/{DeckPath}/Deck.json", json.dumps(DeckData, indent=4))
        ###     print(f"Saved: Decks/{DeckPath}/Deck.json")

        imgui.tree_pop()

def CreateJoker():
    return 1
