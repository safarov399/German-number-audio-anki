import random

from gtts import gTTS
import genanki
import os

language = "de"

fast_deck_name = "German Numbers Fast"
slow_deck_name = "German Numbers Slow"

fast_deck_id = 1234567891  # random large number
fast_model_id = 1091735105  # random large number

slow_deck_id = 1234567892
slow_model_id = 1091735106


fast_my_deck = genanki.Deck(fast_deck_id, fast_deck_name)
slow_my_deck = genanki.Deck(slow_deck_id, slow_deck_name)


my_model = genanki.Model(
    fast_model_id,
    'Audio Front / Text Back',
    fields=[
        {'name': 'Audio'},
        {'name': 'Text'},
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '{{Audio}}',  # front side: only audio
            'afmt': '{{FrontSide}}<hr>{{Text}}',  # back side: audio + number text below
        },
    ])

slow_audio_folder = "num_slow/"  # folder with your mp3 files
fast_audio_folder = "num_fast/"

os.makedirs(slow_audio_folder, exist_ok=True)
os.makedirs(fast_audio_folder, exist_ok=True)

# FAST
for i in range(0, 1000):
    speech = gTTS(text=str(i),lang="de", slow=False)
    speech.save(fast_audio_folder + str(i) + ".mp3")

# SLOW
for i in range(0, 1000):
    speech = gTTS(text=str(i),lang="de", slow=True)
    speech.save(slow_audio_folder + str(i) + ".mp3")

ultimate_number_list = []
for i in range(1, 1000):
    ultimate_number_list.append(i)

random.shuffle(ultimate_number_list)

# FAST
for word in ultimate_number_list:
    audio_file = f"{word}.mp3"
    audio_path = os.path.join(fast_audio_folder, audio_file)

    if os.path.exists(audio_path):
        note = genanki.Note(
            model=my_model,
            fields=[f"[sound:{audio_file}]", str(word)]
        )
        fast_my_deck.add_note(note)
    else:
        print(f"Warning: audio file missing for {word}")

# Package deck with all audio files
my_package = genanki.Package(fast_my_deck)
my_package.media_files = [os.path.join(fast_audio_folder, f"{w}.mp3") for w in ultimate_number_list if os.path.exists(os.path.join(fast_audio_folder, f"{w}.mp3"))]

# Save the Anki deck package
my_package.write_to_file('german_number_fast_num.apkg')



# SLOW
for word in ultimate_number_list:
    audio_file = f"{word}.mp3"
    audio_path = os.path.join(slow_audio_folder, audio_file)

    if os.path.exists(audio_path):
        note = genanki.Note(
            model=my_model,
            fields=[f"[sound:{audio_file}]", str(word)]
        )
        slow_my_deck.add_note(note)
    else:
        print(f"Warning: audio file missing for {word}")

# Package deck with all audio files
my_package = genanki.Package(slow_my_deck)
my_package.media_files = [os.path.join(slow_audio_folder, f"{w}.mp3") for w in ultimate_number_list if os.path.exists(os.path.join(slow_audio_folder, f"{w}.mp3"))]

# Save the Anki deck package
my_package.write_to_file('german_number_slow_num.apkg')
