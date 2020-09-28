import discord
from discord.ext import commands
import youtube_dl
from discord.utils import get
from discord import FFmpegPCMAudio


playlist = ["https://www.youtube.com/watch?v=gEV_Po7PeIY", "https://www.youtube.com/watch?v=8Q5d0P6x61k",
			"https://www.youtube.com/watch?v=beqprrnaKFc", "https://www.youtube.com/watch?v=h18s7zlYOyg"]

count = 0

async def join(client, ctx):
	channel = ctx.message.author.voice.channel
	await channel.connect()


async def play(client, ctx, url):

	def check_queue():
		length = len(playlist)
		global count

		if length != 0:
			print("playing next song...")
			ydl_opts = {
				'format': 'bestaudio/best',
				'quiet': True,
				'postprocessors': [{
					'key': 'FFmpegExtractAudio',
					'preferredcodec': 'mp3',
					'preferredquality': '192',
			}],}
			FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

			with youtube_dl.YoutubeDL(ydl_opts) as ydl:
				url = playlist[count]
				info = ydl.extract_info(url, download=False)
				URL = info['formats'][0]['url']

			voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after=lambda e: check_queue())
			count += 1



	voice = get(client.voice_clients, guild=ctx.guild)
	ydl_opts = {
		'format': 'bestaudio/best',
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],}
	FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
	    info = ydl.extract_info(url, download=False)
	    URL = info['formats'][0]['url']
	voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after=lambda e: check_queue())


async def pause(client, ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("music paused")
        voice.pause()
        await ctx.send('music paused')
    else:
        print('music not playing :')
        await ctx.send('music not playing :')


async def resume(client, ctx):

    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_paused():
        print('music resumed')
        voice.resume()
        await ctx.send('music resumed')
    else:
        print('music is not paused')
        await ctx.send('music is not paused')


async def next(client, ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Playing next song")
        voice.stop()

        await ctx.send("Next song")
    else:
        print("No music playing failed to play next song")
        await ctx.send("no music playing failed")


async def previous(client, ctx):
	global count
	count -= 2

	voice = get(client.voice_clients, guild=ctx.guild)	

	if voice and voice.is_playing():
		print("Playing previous song")
		voice.stop()

		await ctx.send("Previous song")
	else:
		print("No music playing failed to play previous song")
		await ctx.send("no music playing failed")



async def add(client, ctx, url):
	playlist.append(url)



async def leave(client, ctx):
    server = ctx.message.guild
    voice_client = ctx.guild.voice_client
    await voice_client.disconnect()

