import discord
from discord.ext import commands
from discord import app_commands
import os
# from dotenv import load_dotenv <-- ELIMINADO
from datetime import timedelta
from collections import defaultdict
import asyncio

# Las librerías de música (yt_dlp, spotipy) han sido eliminadas.

# load_dotenv() <-- ELIMINADO

# --- CONFIGURACIÓN DE CANALES ---
WELCOME_CHANNEL_ID = 1433467091574329417
STREAM_ANNOUNCE_CHANNEL_ID = 1433986349618172098

# --- CONFIGURACIÓN DEL BOT E INTENTS ---
intents = discord.Intents.default()
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix='!', intents=intents)

warnings_db = defaultdict(list)


@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')
    print(f'ID del bot: {bot.user.id}')
    print('------')
    try:
        # Sincroniza los comandos slash de moderación restantes
        synced = await bot.tree.sync()
        print(f'Sincronizados {len(synced)} comandos slash')
    except Exception as e:
        print(f'Error al sincronizar comandos: {e}')


# --- EVENTO DE BIENVENIDA ---
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        embed = discord.Embed(
            title="¡Bienvenido!",
            description=
            f"¡Bienvenido {member.mention}! ¡Qué alegría tenerte en nuestra comunidad!",
            color=0x8B5CF6)
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="Miembro número",
                        value=f"#{len(member.guild.members)}",
                        inline=True)
        embed.set_image(
            url=
            "https://media.discordapp.net/attachments/1433471238239420457/1433471274763550800/Gemini_Generated_Image_jx061tjx061tjx06.png?ex=69062128&is=6904cfa8&hm=e317b8c98a7b7d3f01f5c4b848eec4ae15c467c015fb165f22d5293d9f37a947&=&format=webp&quality=lossless&width=1318&height=517"
        )
        embed.set_footer(text=f"ID: {member.id}")

        await channel.send(embed=embed)
        print(f'Nuevo miembro: {member.name} (ID: {member.id})')


# --- EVENTO DE ANUNCIO DE STREAM ---
@bot.event
async def on_voice_state_update(member, before, after):
    # Verifica si el usuario acaba de empezar a hacer stream (self_stream pasa de False a True)
    if before.self_stream == False and after.self_stream == True:
        channel = bot.get_channel(STREAM_ANNOUNCE_CHANNEL_ID)
        if channel:
            embed = discord.Embed(
                description=
                "<:kickappicon:1433975381416742963>  **STREAM ON** <:kickappicon:1433975381416742963>\n\n***LINK DEL DIRECTO EN KICK: *** [LINK KICK](https://kick.com/naicocos)\n\n<@&1433987445841723524>",
                color=0x00FF00)
            embed.set_image(
                url=
                "https://media.discordapp.net/attachments/1433471238239420457/1433986686827626576/REGLAS_5.png?ex=6906afac&is=69055e2c&hm=c78e9d7b9d515042d1c50a328a246a0c2a7263cdbe0998523aa7171450cb366c&=&format=webp&quality=lossless"
            )

            await channel.send(embed=embed)
            print(f'Stream iniciado por: {member.name}')


# --- COMANDOS DE MODERACIÓN (SLASH COMMANDS) ---


@bot.tree.command(name="kick",
                  description="Expulsar a un usuario del servidor")
@app_commands.describe(miembro="El miembro que deseas expulsar",
                       razon="Razón de la expulsión")
@app_commands.checks.has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction,
               miembro: discord.Member,
               razon: str = "No especificada"):
    if miembro.top_role >= interaction.user.top_role:
        await interaction.response.send_message(
            "❌ No puedes expulsar a este usuario (rol superior o igual).",
            ephemeral=True)
        return

    try:
        await miembro.kick(reason=razon)
        embed = discord.Embed(
            title="👢 Usuario Expulsado",
            description=
            f"**Usuario:** {miembro.mention}\n**Razón:** {razon}\n**Moderador:** {interaction.user.mention}",
            color=discord.Color.orange())
        await interaction.response.send_message(embed=embed)
        print(
            f'Expulsado: {miembro.name} por {interaction.user.name} - Razón: {razon}'
        )
    except Exception as e:
        await interaction.response.send_message(
            f"❌ Error al expulsar: {str(e)}", ephemeral=True)


@bot.tree.command(name="ban", description="Banear a un usuario del servidor")
@app_commands.describe(miembro="El miembro que deseas banear",
                       razon="Razón del baneo")
@app_commands.checks.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction,
              miembro: discord.Member,
              razon: str = "No especificada"):
    if miembro.top_role >= interaction.user.top_role:
        await interaction.response.send_message(
            "❌ No puedes banear a este usuario (rol superior o igual).",
            ephemeral=True)
        return

    try:
        await miembro.ban(reason=razon)
        embed = discord.Embed(
            title="🔨 Usuario Baneado",
            description=
            f"**Usuario:** {miembro.mention}\n**Razón:** {razon}\n**Moderador:** {interaction.user.mention}",
            color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
        print(
            f'Baneado: {miembro.name} por {interaction.user.name} - Razón: {razon}'
        )
    except Exception as e:
        await interaction.response.send_message(f"❌ Error al banear: {str(e)}",
                                                ephemeral=True)


@bot.tree.command(name="timeout",
                  description="Silenciar temporalmente a un usuario")
@app_commands.describe(miembro="El miembro que deseas silenciar",
                       minutos="Duración del silencio en minutos",
                       razon="Razón del silencio")
@app_commands.checks.has_permissions(moderate_members=True)
async def timeout(interaction: discord.Interaction,
                  miembro: discord.Member,
                  minutos: int,
                  razon: str = "No especificada"):
    if miembro.top_role >= interaction.user.top_role:
        await interaction.response.send_message(
            "❌ No puedes silenciar a este usuario (rol superior o igual).",
            ephemeral=True)
        return

    if minutos < 1 or minutos > 40320:
        await interaction.response.send_message(
            "❌ La duración debe estar entre 1 minuto y 28 días (40320 minutos).",
            ephemeral=True)
        return

    try:
        duration = timedelta(minutes=minutos)
        await miembro.timeout(duration, reason=razon)
        embed = discord.Embed(
            title="🔇 Usuario Silenciado",
            description=
            f"**Usuario:** {miembro.mention}\n**Duración:** {minutos} minutos\n**Razón:** {razon}\n**Moderador:** {interaction.user.mention}",
            color=discord.Color.blue())
        await interaction.response.send_message(embed=embed)
        print(
            f'Silenciado: {miembro.name} por {minutos} minutos - Razón: {razon}'
        )
    except Exception as e:
        await interaction.response.send_message(
            f"❌ Error al silenciar: {str(e)}", ephemeral=True)


@bot.tree.command(name="purge",
                  description="Eliminar una cantidad de mensajes del canal")
@app_commands.describe(cantidad="Número de mensajes a eliminar (1-100)")
@app_commands.checks.has_permissions(manage_messages=True)
async def purge(interaction: discord.Interaction, cantidad: int):
    if cantidad < 1 or cantidad > 100:
        await interaction.response.send_message(
            "❌ La cantidad debe estar entre 1 y 100.", ephemeral=True)
        return

    try:
        await interaction.response.defer(ephemeral=True)
        deleted = await interaction.channel.purge(limit=cantidad)
        await interaction.followup.send(
            f"✅ Se eliminaron {len(deleted)} mensaje(s).", ephemeral=True)
        print(
            f'Purge: {len(deleted)} mensajes eliminados por {interaction.user.name}'
        )
    except Exception as e:
        await interaction.followup.send(
            f"❌ Error al eliminar mensajes: {str(e)}", ephemeral=True)


@bot.tree.command(name="warn", description="Advertir a un usuario")
@app_commands.describe(miembro="El miembro que deseas advertir",
                       razon="Razón de la advertencia")
@app_commands.checks.has_permissions(moderate_members=True)
async def warn(interaction: discord.Interaction, miembro: discord.Member,
               razon: str):
    warning_data = {
        'razon': razon,
        'moderador': interaction.user.name,
        'moderador_id': interaction.user.id
    }
    warnings_db[miembro.id].append(warning_data)

    total_warnings = len(warnings_db[miembro.id])

    embed = discord.Embed(
        title="⚠️ Usuario Advertido",
        description=
        f"**Usuario:** {miembro.mention}\n**Razón:** {razon}\n**Moderador:** {interaction.user.mention}\n**Total de advertencias:** {total_warnings}",
        color=discord.Color.yellow())

    await interaction.response.send_message(embed=embed)
    print(
        f'Advertencia: {miembro.name} - Razón: {razon} - Total: {total_warnings}'
    )

    try:
        dm_embed = discord.Embed(
            title="⚠️ Has recibido una advertencia",
            description=
            f"**Servidor:** {interaction.guild.name}\n**Razón:** {razon}\n**Advertencias totales:** {total_warnings}",
            color=discord.Color.yellow())
        await miembro.send(embed=dm_embed)
    except:
        pass


@bot.tree.command(name="warnings",
                  description="Ver las advertencias de un usuario")
@app_commands.describe(
    miembro="El miembro del que deseas ver las advertencias")
@app_commands.checks.has_permissions(moderate_members=True)
async def warnings(interaction: discord.Interaction, miembro: discord.Member):
    user_warnings = warnings_db.get(miembro.id, [])

    if not user_warnings:
        await interaction.response.send_message(
            f"✅ {miembro.mention} no tiene advertencias.", ephemeral=True)
        return

    embed = discord.Embed(
        title=f"⚠️ Advertencias de {miembro.name}",
        description=f"Total: {len(user_warnings)} advertencia(s)",
        color=discord.Color.yellow())
    embed.set_thumbnail(url=miembro.display_avatar.url)

    for i, warning in enumerate(user_warnings, 1):
        embed.add_field(
            name=f"Advertencia #{i}",
            value=
            f"**Razón:** {warning['razon']}\n**Moderador:** {warning['moderador']}",
            inline=False)

    await interaction.response.send_message(embed=embed, ephemeral=True)


# --- COMANDO DE PRUEBA DE STREAM ---
@bot.tree.command(name="teststream", description="Probar el anuncio de stream")
@app_commands.checks.has_permissions(administrator=True)
async def teststream(interaction: discord.Interaction):
    channel = bot.get_channel(STREAM_ANNOUNCE_CHANNEL_ID)
    if channel:
        embed = discord.Embed(
            description=
            "<:kickappicon:1433975381416742963>  **STREAM ON** <:kickappicon:1433975381416742963>\n\n***LINK DEL DIRECTO EN KICK: *** [LINK KICK](https://kick.com/naicocos)\n\n<@&1433987445841723524>",
            color=0x00FF00)
        embed.set_image(
            url=
            "https://media.discordapp.net/attachments/1433471238239420457/1433986686827626576/REGLAS_5.png?ex=6906afac&is=69055e2c&hm=c78e9d7b9d515042d1c50a328a246a0c2a7263cdbe0998523aa7171450cb366c&=&format=webp&quality=lossless"
        )

        await channel.send(embed=embed)
        await interaction.response.send_message(
            "✅ Anuncio de prueba enviado al canal de streams!", ephemeral=True)
        print(f'Prueba de stream ejecutada por: {interaction.user.name}')
    else:
        await interaction.response.send_message(
            "❌ No se encontró el canal de anuncios de stream.", ephemeral=True)


# --- MANEJO DE ERRORES ---
@kick.error
@ban.error
@timeout.error
@purge.error
@warn.error
@warnings.error
@teststream.error
async def permission_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message(
            "❌ No tienes permisos para usar este comando.", ephemeral=True)


# --- EJECUCIÓN DEL BOT ---
if __name__ == '__main__':
    # Obtiene el token directamente de la variable de entorno de Render
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        # Esto solo se imprime si la variable no existe en Render o localmente
        print(
            "❌ Error: No se encontró DISCORD_TOKEN en las variables de entorno."
        )
        print("Asegúrate de haberla configurado en el panel 'Environment' de Render.")
    else:
        # Inicia el bot usando el token seguro de Render
        bot.run(token)