# Bot de Discord - Moderación y Bienvenida

## Descripción General
Bot de Discord desarrollado en Python con discord.py que proporciona funcionalidades de moderación y envía mensajes de bienvenida automáticos cuando nuevos miembros se unen al servidor.

## Fecha de Creación
31 de octubre de 2025

## Características Principales

### Mensajes de Bienvenida
- Envía mensajes automáticos cuando un nuevo miembro (usuario o bot) se une al servidor
- Canal de bienvenida configurado: ID `1433467091574329417`
- Mensajes con embeds elegantes mostrando avatar del usuario y número de miembro

### Comandos de Moderación (Slash Commands)

#### `/kick`
- Expulsa a un usuario del servidor
- Requiere permisos: `kick_members`
- Parámetros:
  - `miembro`: Usuario a expulsar
  - `razon`: Razón de la expulsión (opcional)

#### `/ban`
- Banea a un usuario del servidor
- Requiere permisos: `ban_members`
- Parámetros:
  - `miembro`: Usuario a banear
  - `razon`: Razón del baneo (opcional)

#### `/timeout`
- Silencia temporalmente a un usuario
- Requiere permisos: `moderate_members`
- Parámetros:
  - `miembro`: Usuario a silenciar
  - `minutos`: Duración del silencio (1-40320 minutos / 28 días)
  - `razon`: Razón del silencio (opcional)

#### `/purge`
- Elimina una cantidad específica de mensajes del canal
- Requiere permisos: `manage_messages`
- Parámetros:
  - `cantidad`: Número de mensajes a eliminar (1-100)

#### `/warn`
- Advierte a un usuario y registra la advertencia
- Requiere permisos: `moderate_members`
- Envía DM al usuario advertido
- Parámetros:
  - `miembro`: Usuario a advertir
  - `razon`: Razón de la advertencia

#### `/warnings`
- Muestra todas las advertencias de un usuario
- Requiere permisos: `moderate_members`
- Parámetros:
  - `miembro`: Usuario del que ver las advertencias

## Arquitectura del Proyecto

### Estructura de Archivos
```
.
├── main.py              # Archivo principal del bot
├── .env                 # Variables de entorno (no versionado)
├── .env.example         # Ejemplo de variables de entorno
├── .gitignore          # Archivos a ignorar en git
├── pyproject.toml      # Dependencias del proyecto
└── replit.md           # Documentación del proyecto
```

### Dependencias
- `discord.py`: Biblioteca principal para interactuar con la API de Discord
- `python-dotenv`: Manejo de variables de entorno

### Sistema de Almacenamiento
- Las advertencias se almacenan en memoria usando `defaultdict`
- **Nota**: Las advertencias se pierden al reiniciar el bot (temporal, sin base de datos)

## Configuración Necesaria

### Variables de Entorno
- `DISCORD_TOKEN`: Token del bot de Discord (requerido)

### Permisos del Bot en Discord
El bot necesita los siguientes permisos en el servidor:
- Kick Members (Expulsar miembros)
- Ban Members (Banear miembros)
- Moderate Members (Moderar miembros / timeouts)
- Manage Messages (Gestionar mensajes)
- Send Messages (Enviar mensajes)
- Embed Links (Insertar enlaces)
- Read Message History (Leer historial de mensajes)

### Intents Requeridos
En el Discord Developer Portal, habilitar:
- Server Members Intent (para eventos de miembros)
- Message Content Intent (para contenido de mensajes)

## Cambios Recientes
- **31/10/2025**: Creación inicial del bot con todos los comandos de moderación y sistema de bienvenida

## Preferencias del Usuario
- Idioma: Español
- Canal de bienvenida: ID `1433467091574329417`

## Próximas Mejoras Sugeridas
1. Sistema de logs en canal dedicado para acciones de moderación
2. Base de datos persistente para almacenar advertencias
3. Comandos para ver historial completo de advertencias
4. Sistema de auto-moderación (filtro de palabras, anti-spam)
5. Roles de moderador con diferentes niveles de permisos
