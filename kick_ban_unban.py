import discord

# MANUAL IMPORT
import settings as setting

async def kick(ctx, member, reason):
	await member.kick(reason=reason)
	await ctx.send(f'{member.mention} has been kicked.')


async def ban(ctx, member, reason):
	await member.ban(reason=reason)
	await ctx.send(f'Banned {member.mention}')


async def unban(ctx, member):
	banned_users = await ctx.guild.bans()
	member_name, member_discriminator = member.split('#')

	for ban_entry in banned_users:
		user = ban_entry.user

		if (user.name, user.discriminator) == (member_name, member_discriminator):
			await ctx.guild.unban(user)
			await ctx.send(f'Unbanned {user.mention}')
			return


async def mute(ctx, member):
	muted_role = ctx.guild.get_role(setting.MUTED_ROLE)

	await member.add_roles(muted_role)
	await ctx.send("{} has been muted.".format(member.mention))


async def unmute(ctx, member):
	muted_role = ctx.guild.get_role(setting.MUTED_ROLE)

	await member.remove_roles(muted_role)
	await ctx.send("{} has been unmuted.".format(member.mention))
