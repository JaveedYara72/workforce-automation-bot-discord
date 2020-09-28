import discord
from termcolor import colored
import asyncio
import random
from enum import IntEnum, Enum
from words import word_list
import numpy as np
import sys
from tabulate import tabulate
import time

# c4d
# board = []


###############################################################################################################
# 	CONNECT4 DOTS GAME
###############################################################################################################

async def c4d(client, ctx):
	board = []

	def pred(m):
		return(m.author == ctx.author and m.channel == ctx.channel)

	async def take_input():
		try:
			msg1 = await client.wait_for('message',check=pred,timeout=8640.0)
		except asyncio.TimeoutError:
			await ctx.send("Timeout. Please request a koder for reregistration.")
		else:
			return msg1


	def create_board():
		for i in range(6):
			a=[]
			for j in range(7):
				a.append("⬜️")
			board.append(a)

		create_board()


	async def display_board():
		for i in range(6):
			str=""
			for j in range(7):
				str = str+'|'+board[i][j]+'|'
			str = str +'\n'+'---------------------------'
			await ctx.send(str)

		await display_board()


	last_index = [5,5,5,5,5,5,5]
	filled_boxes = 0

	def check_draw():
		if filled_boxes == 42:
		    return True


		def horizontalcheck():
			for i in range(6):
				for j in range(4):
					if(board[i][j]==board[i][j+1]==board[i][j+2]==board[i][j+3] and board[i][j]!="⬜️"):
						return True
					else:
						continue

	def verticalcheck():
		for j in range(7):
			for i in range(3):
				if(board[i][j]==board[i+1][j]==board[i+2][j]==board[i+3][j] and board[i][j]!="⬜️"):
					return True
				else:
					continue

	def diagonalcheck():
		for j in range(7):
			for i in range(6):
				try:
					if(board[i][j]==board[i+1][j+1]==board[i+2][j+2]==board[i+3][j+3] and board[i][j]!="⬜️"):
						return True

					elif(board[i][j]==board[i-1][j+1]==board[i-2][j+2]==board[i-3][j+3] and board[i][j]!="⬜️"):
						return True
					else:
						continue
				except IndexError:
					pass
				continue


	p1 = "Player 1"
	p1_symbol = "⭕️"

	p2 = "Player 2"
	p2_symbol = "❌"

	game_on=True
	current_player = 1
	player = p1
	current_symbol = p1_symbol

	while game_on:

		await ctx.send('For this round, Player %s will go!' %(player))
		await ctx.send('Select any coloumn (1-7):')

		col_number = await take_input()
		col_no = int(col_number.content)
		col_no = col_no-1

		board[last_index[col_no]][col_no] = current_symbol
		last_index[col_no] = last_index[col_no]-1
		filled_boxes = filled_boxes+1
		await display_board()

		if check_draw():
		    await ctx.send("It's a draw")
		    game_on = False

		if (horizontalcheck() or verticalcheck() or diagonalcheck()):
		    game_on = False
		    await ctx.send('%s won the game'%(player))

		current_player = current_player*-1

		if(current_player == 1):
		    player = p1
		    current_symbol = p1_symbol
		else:
		    player = p2
		    current_symbol = p2_symbol


###############################################################################################################
# 	DEC OF CARD GAME
###############################################################################################################

async def doc(client, ctx):
    p1_win_count = 0
    p2_win_count = 0

    full_deck=[]
    partial_deck=[]
    player1_cards=[]
    player2_cards=[]
    await ctx.send("Welcome to Deck of Cards game...")
    await ctx.send("In each round player will draw card and player with highest card wins the round!!")
    await ctx.send("But the player with most number of wins ....Wins the Game!!!")
    await ctx.send("To get started invite one of the members!!")
    def pred(m):
        return m.author == ctx.author and m.channel == ctx.channel


    def check(reaction, user):
        return (str(reaction.emoji) == '☑' or str(reaction.emoji) == '❎') and user == ctx.message.author


    async def take_input():
        try:
            message = await client.wait_for('message', check=pred, timeout=8640.0)
        except asyncio.TimeoutError:
            await ctx.send("Timeout. Please request a koder for reregistration.")
        else:
            return message


    async def take_reaction():
        try:
            result = await client.wait_for('reaction_add', check=check, timeout=8640.0)
        except asyncio.TimeoutError:
            await ctx.send("Timeout. Please request a koder for reregistration.")
        else:
            reaction, user = result
            if (str(reaction.emoji) == '☑'):
                return True
            if (str(reaction.emoji) == '❎'):
                return False


    embed = discord.Embed(title="Challenged",description="Following" + str(ctx.author) + "challenged")# + pass_context)
    embed.set_author(name="Welcome Deck of cards",icon_url="https://cdn0.iconfinder.com/data/icons/card-games/48/Paul-29-512.png")
    embed.set_footer(text="Click on reactions for accepting and rejecting")
    textEmbed = await ctx.send(embed=embed)
    await textEmbed.add_reaction(emoji="☑")
    await textEmbed.add_reaction(emoji="❎")
    input = await take_reaction()
    await textEmbed.delete()


    class Card(IntEnum):
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5
        SIX = 6
        SEVEN = 7
        EIGHT = 8
        NINE = 9
        TEN = 10
        JACK =11
        QUEEN = 12
        KING = 13
        ACE = 14

    class Suit(Enum):
        SPADES = 'spades'
        CLUBS = 'clubs'
        HEARTS = 'hearts'
        DIAMONDS = 'diamonds'

    class PlayingCard:
        def __init__(self,card_value,card_suit):
            self.card = card_value
            self.suit = card_suit

    def create_deck():
        for i in Suit:
            for j in Card:
                full_deck.append(PlayingCard(Card(j), Suit(i)))
        return full_deck


    def draw_card(deck):
        rand_card = random.randint(0,len(deck)-1)
        return deck.pop(rand_card)


    def deal():
        while(len(partial_deck)>0):
            player1_cards.append(draw_card(partial_deck))
            player2_cards.append(draw_card(partial_deck))


    if (input):
        create_deck()
        partial_deck = list(full_deck)
        deal()

        for i in range(0,len(player1_cards)):
            if(player1_cards[i].card > player2_cards[i].card):
                await ctx.send('p1 wins with {}'.format(player1_cards[i].card))
                await ctx.send('p2 looses with {}'.format(player2_cards[i].card))
                p1_win_count+=1 
            if(player1_cards[i].card < player2_cards[i].card):
                await ctx.send('p1 wins with {}'.format(player2_cards[i].card))
                await ctx.send('p2 looses with {}'.format(player1_cards[i].card))
                p2_win_count+=2

            else:
                await ctx.send("It's a draw")

        await ctx.send("Time see the Final result!!!")

        if(p1_win_count > p2_win_count):
            await ctx.send('p1 wins with a total count of: {}'.format(p1_win_count))
            await ctx.send('p2 looses with a total count of: {}'.format(p2_win_count))
        elif(p1_win_count < p2_win_count):
            await ctx.send('p2 wins with a total count of: {}'.format(p2_win_count))
            await ctx.send('p1 looses with a total count of: {}'.format(p1_win_count))
        else:
            await ctx.send("It's a draw!!")


###############################################################################################################
# 	ESCAPE ROOM GAME
###############################################################################################################

player = 100
enemy = 100
message1="You wake up in a dark room, You don't know where you are or how you get here"
message2= "You vaguely see two doors in font of you"


async def er(client, ctx):
	
	global player
	global enemy
	async def enemyAttack():
	    global player
	    enemyAttack = random.randint(4,15)
	    await ctx.send("Enemy Attacks!!")
	    await ctx.send("Attack = {} HP".format(enemyAttack))
	    player = player-enemyAttack
	    await ctx.send("Player Health: {}".format(player))

	async def conservAttack():
	    global enemy
	    attack = random.randint(7,9)
	    await ctx.send("Player Attacks!!")
	    await ctx.send("Attack = {} HP".format(attack))
	    enemy=enemy-attack
	    await ctx.send("Enemy Health: {}".format(enemy))

	async def hardAttack():
	    global enemy
	    attack=random.randint(1,17)
	    await ctx.send("Player Attacks!!")
	    await ctx.send("Attack = {} HP".format(attack))
	    enemy=enemy-attack
	    await ctx.send("Enemy Health: {}".format(enemy))

	async def checkPlayerHealth():
	    if player<1:
	        await ctx.send("You died!!!")
	        exit()


	await ctx.send(message1)
	await ctx.send(message2)
	await ctx.send('''Do you want to go through one of the door??
	            1. Left Door
	            2. Right Door
	            3. Just sit here a minute''')

	def pred(m):
	    return(m.author == ctx.author and m.channel == ctx.channel)

	async def take_input():
	    try:
	        msg1 = await client.wait_for('message',check=pred,timeout=8640.0)
	    except asyncio.TimeoutError:
	        await ctx.send("Timeout. Please request a koder for reregistration.")
	    else:
	        return msg1


	msg = await take_input()
	msg = msg.content

	if msg=='1':
	    await ctx.send("Good choice,but be prepared for a fight")

	elif msg =='2':
	    await ctx.send("You like taking the hard way,don't you?")
	    enemy=enemy*2

	elif msg =='3':
	    await ctx.send("You are wasting time! You're losing life")
	    player = player-7
	    await ctx.send("Player health:{}".format(player))

	else:
	    await ctx.send("You entered wrong option...Try again")

	await ctx.send("You hear the sounds of a monster approaching in the darkness...What you want to do??")
	while True:
	    await checkPlayerHealth()
	    if enemy<1:
	        await ctx.send("You defeated the monster!!!")
	        break
	    await ctx.send("Fight or Flee????")
	    choice_taken=await take_input()
	    choice=choice_taken.content
	    if choice in ['flee','Flee','FLEE']:
	        break
	    elif choice in ['fight','Fight','FIGHT']:
	        await ctx.send("Choose '1' for Hard attack")
	        await ctx.send("Choose '2' for Conservative attack")
	        choice_taken=await take_input()
	        choice=choice_taken.content
	        if choice=='1':
	            await hardAttack()
	        elif choice=='2':
	            await conservAttack()
	        else:
	            await ctx.send("That's not an option...Try again")
	    else:
	        await ctx.send("That's not an option...Try again")
	    await enemyAttack()


###############################################################################################################
# 	HANGMAN GAME
###############################################################################################################

async def hm(client, ctx):

    def pred(m):
        return(m.author == ctx.author and m.channel == ctx.channel)

    async def take_input():
        try:
            msg1 = await client.wait_for('message',check=pred,timeout=8640.0)
        except asyncio.TimeoutError:
            await ctx.send("Timeout. Please request a koder for reregistration.")
        else:
            return msg1

    def get_word():
        word = random.choice(word_list)
        return word.upper()


    def display_hangman(tries):
        stages = [
                    """
                       --------
                       |      |
                       |      O
                       |     \\|/
                       |      |
                       |     / \\
                       -
                    """,

                    """
                       --------
                       |      |
                       |      O
                       |     \\|/
                       |      |
                       |     /
                       -
                    """,

                    """
                       --------
                       |      |
                       |      O
                       |     \\|/
                       |      |
                       |
                       -
                    """,

                    """
                       --------
                       |      |
                       |      O
                       |     \\|
                       |      |
                       |
                       -
                    """,

                    """
                       --------
                       |      |
                       |      O
                       |      |
                       |      |
                       |
                       -
                    """,

                    """
                       --------
                       |      |
                       |      O
                       |
                       |
                       |
                       -
                    """,

                    """
                       --------
                       |      |
                       |
                       |
                       |
                       |
                       -
                    """
        ]
        return stages[tries]


    word = get_word()
    word_completion = "_" * len(word)
    guessed = False
    guessed_letters = []
    guessed_words = []
    tries = 6
    await ctx.send("Let's play Hangman!")
    await ctx.send(display_hangman(tries))
    await ctx.send(word_completion)
    while not guessed and tries > 0:
        guess_word = await take_input()
        guess = guess_word.content.upper()

        if len(guess) == 1 and guess.isalpha():
            if guess in guessed_letters:
                await ctx.send("You already guessed the letter:{}".format(guess))
            elif guess not in word:
                await ctx.send( "{} is not in the word.".format(guess))
                tries -= 1
                guessed_letters.append(guess)
            else:
                await ctx.send("Good job,{} is in the word!".format(guess))
                guessed_letters.append(guess)
                word_as_list = list(word_completion)
                indices = [i for i, letter in enumerate(word) if letter == guess]
                for index in indices:
                    word_as_list[index] = guess
                word_completion = "".join(word_as_list)
                if "_" not in word_completion:
                    guessed = True
        elif len(guess) == len(word) and guess.isalpha():
            if guess in guessed_words:
                await ctx.send("You already guessed the word:{}".format(guess))
            elif guess != word:
                await ctx.send("{} is not the word.".format(guess))
                tries -= 1
                guessed_words.append(guess)
            else:
                guessed = True
                word_completion = word
        else:
            await ctx.send("Not a valid guess.")
        await ctx.send(display_hangman(tries))
        await ctx.send(word_completion)
    if guessed:
        await ctx.send("Congrats, you guessed the word! You win!")
    else:
        await ctx.send("Sorry, you ran out of tries. The word was " + word + ". Maybe next time!")


###############################################################################################################
# 	HOUSIE GAME
###############################################################################################################

async def housie(client, ctx):
    await ctx.send("Welcome to the housie game:")
    await ctx.send("This is a ticket generator...")


    def pred(m):
        return m.author == ctx.author and m.channel == ctx.channel



    async def take_input():
        try:
            message = await client.wait_for('message', check=pred, timeout=8640.0)
        except asyncio.TimeoutError:
            await ctx.send("Timeout. Please request a koder for reregistration.")
        else:
            return message



    def getTickets():

        ticket_array = np.zeros((3, 9), dtype=int)
        total_numbers = [num for num in range(1, 90)]
        total_indices = [(i, j) for i in range(3) for j in range(9)]
        random_indices = []


        first_row = random.sample(total_indices[:9], 5)
        second_row = random.sample(total_indices[9:18], 5)
        third_row = random.sample(total_indices[-9:], 5)

        for i in first_row:
            random_indices.append(i)

        for i in second_row:
            random_indices.append(i)

        for i in third_row:
            random_indices.append(i)


        for num in random_indices:
            if num[1] == 0:
                number = random.choice(total_numbers[:10])
                ticket_array[num] = number
                total_numbers[total_numbers.index(number)] = 0
            elif num[1] == 1:
                number = random.choice(total_numbers[10:20])
                ticket_array[num] = number
                total_numbers[total_numbers.index(number)] = 0
            elif num[1] == 2:
                number = random.choice(total_numbers[20:30])
                ticket_array[num] = number
                total_numbers[total_numbers.index(number)] = 0
            elif num[1] == 3:
                number = random.choice(total_numbers[30:40])
                ticket_array[num] = number
                total_numbers[total_numbers.index(number)] = 0
            elif num[1] == 4:
                number = random.choice(total_numbers[40:50])
                ticket_array[num] = number
                total_numbers[total_numbers.index(number)] = 0
            elif num[1] == 5:
                number = random.choice(total_numbers[50:60])
                ticket_array[num] = number
                total_numbers[total_numbers.index(number)] = 0
            elif num[1] == 6:
                number = random.choice(total_numbers[60:70])
                ticket_array[num] = number
                total_numbers[total_numbers.index(number)] = 0
            elif num[1] == 7:
                number = random.choice(total_numbers[70:80])
                ticket_array[num] = number
                total_numbers[total_numbers.index(number)] = 0
            elif num[1] == 8:
                number = random.choice(total_numbers[80:89])
                ticket_array[num] = number
                total_numbers[total_numbers.index(number)] = 0


        for col in range(9):
            if(ticket_array[0][col] != 0 and ticket_array[1][col] != 0 and ticket_array[2][col] != 0):
                for row in range(2):
                    if ticket_array[row][col] > ticket_array[row+1][col]:
                        temp = ticket_array[row][col]
                        ticket_array[row][col] = ticket_array[row+1][col]
                        ticket_array[row+1][col] = temp

            elif(ticket_array[0][col] != 0 and ticket_array[1][col] != 0 and ticket_array[2][col] == 0):
                if ticket_array[0][col] > ticket_array[1][col]:
                    temp = ticket_array[0][col]
                    ticket_array[0][col] = ticket_array[1][col]
                    ticket_array[1][col] = temp

            elif(ticket_array[0][col] != 0 and ticket_array[2][col] != 0 and ticket_array[1][col] == 0):
                if ticket_array[0][col] > ticket_array[2][col]:
                    temp = ticket_array[0][col]
                    ticket_array[0][col] = ticket_array[2][col]
                    ticket_array[2][col] = temp

            elif(ticket_array[0][col] == 0 and ticket_array[1][col] != 0 and ticket_array[2][col] != 0):
                if ticket_array[1][col] > ticket_array[2][col]:
                    temp = ticket_array[1][col]
                    ticket_array[1][col] = ticket_array[2][col]
                    ticket_array[2][col] = temp

        return ticket_array


    await ctx.send("Enter no of ticket you want to generate:")
    numberOfTickets = await take_input()
    tickets = []
    for i in range(int(numberOfTickets.content)):
        ticket = getTickets()
        tickets.append(ticket)
    for ticket in tickets:
        await ctx.send(tabulate(ticket, tablefmt="fancy_grid", numalign="center"))


###############################################################################################################
# 	ROCK PAPER SCISSORS GAME
###############################################################################################################

async def rps(client, ctx):
    await ctx.send("Welcome>>>>")
    await ctx.send("This is a Rock-Paper-Scissors game")
    await ctx.send("Invite a member to get started")

    def pred(m):
        return m.author == ctx.author and m.channel == ctx.channel


    def check(reaction, user):
        # return (str(reaction.emoji) == '☑' or str(reaction.emoji) == '❎') and user == user.author
        return (str(reaction.emoji) == '☑' or str(reaction.emoji) == '❎') and user == ctx.message.author


    async def take_input():
        try:
            message = await client.wait_for('message', check=pred, timeout=8640.0)
        except asyncio.TimeoutError:
            await ctx.send("Timeout. Please request a koder for reregistration.")
        else:
            return message


    async def take_reaction():
        try:
            result = await client.wait_for('reaction_add', check=check, timeout=8640.0)
        except asyncio.TimeoutError:
            await ctx.send("Timeout. Please request a koder for reregistration.")
        else:
            reaction, user = result
            if (str(reaction.emoji) == '☑'):
                return True
            if (str(reaction.emoji) == '❎'):
                return False


    embed = discord.Embed(title="Challenged",description="Following" + str(ctx.author) + "challenged")# + pass_context)
    embed.set_author(name="Welcome to Rock-Paper-Scissors",icon_url="https://www.pinclipart.com/picdir/middle/15-152622_water-droplets-cartoon-robber-running-easy-to-rock.png")
    embed.set_footer(text="Click on reactions for accepting and rejecting")
    textEmbed = await ctx.send(embed=embed)
    await textEmbed.add_reaction(emoji="☑")
    await textEmbed.add_reaction(emoji="❎")
    input = await take_reaction()
    await textEmbed.delete()

    if(input):
        await ctx.send("Enter rock/paper/scissors:")
        player_1 = await take_input()
        player_1 = player_1.content
        
        player_2 = await take_input()
        player_2 = player_2.content

        a_list = ["rock", "paper", "scissors"]

        while player_1 not in a_list or player_2 not in a_list:
            await ctx.send("Invalid input. Please give a valid input.")
            player_1 = await take_input()
            player_1 = player_1.content
            player_2 = await take_input()
            player_2 = player_2.content

        while player_1 == player_2:
            await ctx.send("Nobody wins. Try again")
            player_1 = await take_input()
            player_1 = player_1.content
            player_2 = await take_input()
            player_2 = player_2.content

        if player_1 == "rock" and player_2 == "paper":
            await ctx.send("Player 2 wins!")

        elif player_1 == "paper" and player_2 == "rock":
            await ctx.send("Player 1 wins!")

        elif player_1 == "rock" and player_2 == "scissors":
            await ctx.send("Player 1 wins!")

        elif player_1 == "scissors" and player_2 == "rock":
            await ctx.send("Player 2 wins")

        elif player_1 == "paper" and player_2 == "scissors":
            await ctx.send("Player 2 wins!")

        elif player_1 == "scissors" and player_2 == "paper":
            await ctx.send("PLayer 1 wins!")

    else:
        await ctx.send("Player declined your request!!")


###############################################################################################################
# 	SNAKE GAME
###############################################################################################################

# SLEEP_BETWEEN_ACTIONS = 1
# MAX_VAL = 100
# DICE_FACE = 6
# player = ['0','1','2']


async def snake(client, ctx):
	SLEEP_BETWEEN_ACTIONS = 1
	MAX_VAL = 100
	DICE_FACE = 6
	player = ['0','1','2']

	await ctx.send("Welcome>>>>")
	await ctx.send("This is a Snake and Ladder game!!!!")

	msg = """

	Rules:
	  1. Initally both the players are at starting position i.e. 0.
	     Take it in turns to roll the dice.
	     Move forward the number of spaces shown on the dice.
	  2. If you lands at the bottom of a ladder, you can move up to the top of the ladder.
	  3. If you lands on the head of a snake, you must slide down to the bottom of the snake.
	  4. The first player to get to the FINAL position is the winner.
	  5. Hit enter to roll the dice.

	"""
	await ctx.send(msg)
	await ctx.send("Invite a member to get started")


	def pred(m):
	    return m.author == ctx.author and m.channel == ctx.channel


	def check(reaction, user):
	    # return (str(reaction.emoji) == '☑' or str(reaction.emoji) == '❎') and user == user.author
	    return (str(reaction.emoji) == '☑' or str(reaction.emoji) == '❎') and user == ctx.message.author


	async def take_input():
	    try:
	        message = await client.wait_for('message', check=pred, timeout=8640.0)
	    except asyncio.TimeoutError:
	        await ctx.send("Timeout. Please request a koder for reregistration.")
	    else:
	        return message


	async def take_reaction():
	    try:
	        result = await client.wait_for('reaction_add', check=check, timeout=8640.0)
	    except asyncio.TimeoutError:
	        await ctx.send("Timeout. Please request a koder for reregistration.")
	    else:
	        reaction, user = result
	        if (str(reaction.emoji) == '☑'):
	            return True
	        if (str(reaction.emoji) == '❎'):
	            return False


	embed = discord.Embed(title="Challenged",description="Following" + str(ctx.author) + "challenged")# + pass_context)
	embed.set_author(name="Welcome to Snake and Ladders",icon_url="https://image.flaticon.com/icons/png/512/103/103261.png")
	embed.set_footer(text="Click on reactions for accepting and rejecting")
	textEmbed = await ctx.send(embed=embed)
	await textEmbed.add_reaction(emoji="☑")
	await textEmbed.add_reaction(emoji="❎")
	input = await take_reaction()
	await textEmbed.delete()

	snakes = {
	    8: 4,
	    18: 1,
	    26: 10,
	    39: 5,
	    51: 6,
	    54: 36,
	    56: 1,
	    60: 23,
	    75: 28,
	    83: 45,
	    85: 59,
	    90: 48,
	    92: 25,
	    97: 87,
	    99: 63
	}


	ladders = {
	    3: 20,
	    6: 14,
	    11: 28,
	    15: 34,
	    17: 74,
	    22: 37,
	    38: 59,
	    49: 67,
	    57: 76,
	    61: 78,
	    73: 86,
	    81: 98,
	    88: 91
	}

	player_turn_text = [
	    "Your turn.",
	    "Go.",
	    "Please proceed.",
	    "Lets win this.",
	    "Are you ready?",
	    "",
	]

	snake_bite = [
	    "boohoo",
	    "bummer",
	    "snake bite",
	    "oh no",
	    "dang"
	]

	ladder_jump = [
	    "woohoo",
	    "woww",
	    "nailed it",
	    "oh my God...",
	    "yaayyy"
	]




	async def get_dice_value():
	    time.sleep(SLEEP_BETWEEN_ACTIONS)
	    dice_value = random.randint(1, DICE_FACE)
	    await ctx.send("Its a " + str(dice_value))
	    return dice_value

	async def got_snake_bite(old_value, current_value, player_name):
	    await ctx.send(random.choice(snake_bite).upper() + " ~~~~~~~~>")
	    await ctx.send(player_name + " got a snake bite. Down from " + str(old_value) + " to " + str(current_value))


	async def got_ladder_jump(old_value, current_value, player_name):
	    await ctx.send(random.choice(ladder_jump).upper() + " ########")
	    await ctx.send(player_name + " climbed the ladder from " + str(old_value) + " to " + str(current_value))


	async def snake_ladder(player_name, current_value, dice_value):
	    time.sleep(SLEEP_BETWEEN_ACTIONS)
	    old_value = current_value
	    current_value = current_value + dice_value

	    if current_value > MAX_VAL:
	        await ctx.send("You need " + str(MAX_VAL - old_value) + " to win this game. Keep trying.")
	        return old_value

	    await ctx.send(player_name + " moved from " + str(old_value) + " to " + str(current_value))
	    if current_value in snakes:
	        final_value = snakes.get(current_value)
	        await got_snake_bite(current_value, final_value, player_name)

	    elif current_value in ladders:
	        final_value = ladders.get(current_value)
	        await got_ladder_jump(current_value, final_value, player_name)

	    else:
	        final_value = current_value

	    return final_value


	async def check_win(player_name, position):
	    time.sleep(SLEEP_BETWEEN_ACTIONS)
	    if MAX_VAL == position:
	        await ctx.send("Thats it.\n\n" + player_name + " won the game.")
	        await ctx.send("Congratulations " + player_name)
	        await ctx.send("Thank you for playing the game.")


	player1_current_position = 0
	player2_current_position = 0
	player1_name = "Player 1"
	player2_name = "Player 2"

	while True:
	    time.sleep(SLEEP_BETWEEN_ACTIONS)
	    await ctx.send("Hit 'R' to roll the dice:")
	    input_1 = await take_input()
	    await ctx.send("\nRolling dice...")
	    dice_value = await get_dice_value()
	    time.sleep(SLEEP_BETWEEN_ACTIONS)
	    await ctx.send(player1_name + " moving....")
	    player1_current_position = await snake_ladder(player1_name, player1_current_position, dice_value)

	    await check_win(player1_name, player1_current_position)


	    await ctx.send("Hit 'R' to roll the dice:")
	    input_2 = await take_input()
	    await ctx.send("\nRolling dice...")
	    dice_value = await get_dice_value()
	    time.sleep(SLEEP_BETWEEN_ACTIONS)
	    await ctx.send(player2_name + " moving....")
	    player2_current_position = await snake_ladder(player2_name, player2_current_position, dice_value)

	    await check_win(player2_name, player2_current_position)


###############################################################################################################
#   BATTLESHIP GAME
###############################################################################################################


async def bs(client, ctx):

    board = []
    def pred(m):
        return(m.author == ctx.author and m.channel == ctx.channel)

    async def take_input():
        try:
            msg1 = await client.wait_for('message',check=pred,timeout=8640.0)
        except asyncio.TimeoutError:
            await ctx.send("Timeout. Please request a koder for reregistration.")
        else:
            return msg1


    for x in range(0,5):
        board.append(["o"] * 5)

    async def print_board(board):
        for row in board:
            await ctx.send(" ".join(row))

    await ctx.send("Let's play Battleship!")
    await ctx.send("This is a 2 player game")

    await ctx.send("Enter first player name: ")
    player_1 = await take_input()
    player_1 = str(player_1.content)
    await ctx.send("Enter second player name: ")
    player_2 = await take_input()
    player_2 = str(player_2.content)
    players = [0,player_1, player_2]

    def random_player(players):
        return random.choice(players)

    def random_row(board):
        return random.randint(0,len(board)-1)

    def random_col(board):
        return random.randint(0,len(board[0])-1)


    ship_row_1 = random_row(board)
    ship_col_1 = random_col(board)

    ship_row_2 = random_row(board)
    ship_col_2 = random_col(board)

    await print_board(board)

    await ctx.send( "Player 1 starts the game.")




    hit_count = 0
    curr_player = 1
    for turn in range(7):
        await ctx.send("{} Turn!!".format(players[curr_player]))
        await ctx.send("Guess Row: (allowed values: 0-4) ")
        guess_row = await take_input()
        guess_row = int(guess_row.content)-1
        await ctx.send("Guess Col: (allowed values: 0-4) ")
        guess_col = await take_input()
        guess_col = int(guess_col.content)-1

        if (guess_row == ship_row_1 and guess_col == ship_col_1) or (guess_row == ship_row_2 and guess_col == ship_col_2):
            hit_count = hit_count + 1
            board[guess_row][guess_col] = "*"
            await ctx.send("Congratulations! ")
            if hit_count == 1:
                   await ctx.send("You sunk first battleship!")
                   await print_board(board)
            elif hit_count == 2:
                   await ctx.send("You sunk second battleship! You win!")
                   await print_board(board)
                   break
        else:
            if (guess_row < 0 or guess_row > 4)  or (guess_col < 0 or guess_col > 4):
                await ctx.send("Oops, that's not even in the ocean.")
            elif(board[guess_row][guess_col] == "X"):
                await ctx.send("You guessed that one already.")
                await print_board(board)
            else:
                await ctx.send("You missed my battleship!")
                board[guess_row][guess_col] = "X"
                await print_board(board)
            turn = turn+1
            await ctx.send("{} turn".format(turn))
        curr_player = curr_player * -1
    await print_board(board)
    await ctx.send("Ship 1 is hidden:")
    await ctx.send(ship_row_1)
    await ctx.send(ship_col_1)

    await ctx.send("Ship 2 is hidden:")
    await ctx.send(ship_row_2)
    await ctx.send(ship_col_2)
