from emojis import Emojis

welcome_msg = '''
Hi! I am Anagramika, the humble disciple of Riddler. I challenge you to solve all my anagrams!! If you are game, please start the game by /anstart {}
'''.format(Emojis["smiling_face_with_open_mouth"])

anagram_welcome_msg = '''
Okay ! Let's test your anagram skills {}
'''.format(Emojis["winking_face"])

rules_group_msg = '''
Here are the rules {}:

1. Anybody can start the game by /anstart, stop the game by typing /anstop. I know people, I am trusting you guys on your sportsman spirit {}! Be a good sport {}

2. Each correct answer fetches 10 points to the individual who answered it correctly.

3. In many cases, there could be more meaningful words formed from the anagram. But I am adamant and uncompromising {} I want exactly what I asked !!

4. There are no negative marks for a wrong answer {}

5. There is no timeout for any question. However, if the frustration hits the ceiling, you can enter a /pass to pass a particular word {}

6. You can know your score anytime during /score command. For the full scoreboard, use /board command!

7. That's all folks!! Enjoy!! Here you go..{}!
'''.format(Emojis["smiling_face_with_open_mouth"],
           Emojis["winking_face"],
           Emojis["face_with_stuck-out_tongue_and_winking_eye"],
           Emojis["pouting_face"],
           Emojis["relieved_face"],
           Emojis["unamused_face"],
           Emojis["face_with_no_good_gesture"]
           )

rules_priv_msg = '''
Here are the rules :

1. Start by /anstart and end by /anstop {}

2. Each correct answer fetches you 10 points

3. No negative marking {}

4. No timeouts, however you can pass the question by /pass

5. You can know your score anytime during /score command.

6. That's all!!! Enjoy!! Here you go..{}!
'''.format(
        Emojis["smiling_face_with_open_mouth"],
        Emojis["relieved_face"],
        Emojis["face_with_no_good_gesture"]
    )

already_in_msg = '''
I am already giving you anagrams! Don't get me started again!! :P
'''
not_on_game_msg = '''
Please do /start. You only told me to stop :|..
'''

good_bye_msg = '''
Good bye {}!! Hope to see you soon {} ! Here are the scores :
'''.format(
    Emojis["happy_person_raising_one_hand"],
    Emojis["grinning_face_with_smiling_eyes"]
    )

pairs = [
    [
        r"my name is (.*)",
        ["Hello %1 {}, How are you today ?".format(Emojis["grinning_face_with_smiling_eyes"]),]
    ],
    [
        r"what is your name(.*)?",
        ["My name is Anagramika {}","Don't you already know {} ?".format(Emojis["smiling_face_with_smiling_eyes"], Emojis["unamused_face"]),]
    ],
    [
        r"how are you(.*)?",
        ["I'm doing good\nHow about You ?",]
    ],
    [
        r"i'm fine(.*)?",
        ["{}".format(Emojis["smiling_face_with_smiling_eyes"], Emojis["grinning_face_with_smiling_eyes"]),]
    ],
    [
        r"sorry(.*)",
        ["Its alright","Its OK, never mind",]
    ],
    [
        r"i'm(.*)doing good",
        ["Nice to hear that","Alright :)",]
    ],
    [
        r"hi|hey|hello",
        ["Hello", "Hey there",]
    ],
    [
        r"(.*) age?",
        ["I'm a computer program dude\nSeriously you are asking me this{}?".format(Emojis["face_with_ok_gesture"]),]
        
    ],
    [
        r"how old are you(.*)?",
        ["I'm a computer program dude\nSeriously you are asking me this{}?".format(Emojis["face_with_ok_gesture"]),]
        
    ],
    [
        r"what (.*) want ?",
        ["Make me an offer I can't refuse",]
        
    ],
    [
        r"(.*) created ?",
        ["Maddy created me","Top secret {}".format(Emojis["winking_face"]),]
    ],
    [
        r"(.*) (location|city) ?",
        ["Letteranta, the land of letters",]
    ],
    [
        r"how is weather in (.*)?",
        ["Weather in %1 is awesome like always","Too hot man here in %1","Too cold man here in %1","Never even heard about %1"]
    ],
    [
        r"i work in (.*)?",
        ["%1 is an Amazing company, I have heard about it. But they are in huge loss these days.",]
    ],
[
        r"(.*)raining in (.*)",
        ["No rain since last week here in %2","Damn its raining too much here in %2"]
    ],
    [
        r"how (.*) health(.*)",
        ["I'm a computer program, so I'm always healthy {}".format(Emojis["face_with_stuck-out_tongue_and_winking_eye"]),]
    ],
    [
        r"(.*)who (.*) sportsperson(.*)?",
        ["Sachin Tendulkar","Daniel Negreanu","Adam Gilchrist"]
    ],
    [
        r"who (.*) (moviestar|actor|filmstar)?",
        ["What's a movie ?"]
    ],
    [
        r"(.*)sex(.*)",
        ["Aah, just stop it ! Don't ask me such questions {}".format(Emojis["see-no-evil_monkey"])]
    ]
]