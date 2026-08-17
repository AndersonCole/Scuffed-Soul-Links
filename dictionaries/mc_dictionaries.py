mcFileLocations = {
    'ServerPort': 'text_files/minecraft_server/server_port.txt',
    'RconIp': 'text_files/minecraft_server/rcon_ip.txt',
    'RconPort': 'text_files/minecraft_server/rcon_port.txt',
    'RconPassword': 'text_files/minecraft_server/rcon_password.txt',
    'GoogleDrive': 'text_files/minecraft_server/google_drive_link.txt',
    'ModInfo': 'text_files/minecraft_server/mod_info.txt',
    'Moai': 'text_files/minecraft_server/moai.txt',
    'Boats': 'text_files/minecraft_server/boats.txt'
}

mcImagePaths = {
    'AmberShuckle': 'https://i.imgur.com/oC02eDj.png',
    'ShinyAmberShuckle': 'https://i.imgur.com/Np0NjY2.png'
}

mcEmbedColour = 14914576

dimensions = [
    {'Name': 'Overworld', 'CmdName': 'minecraft:overworld'}, 
    {'Name': 'Nether', 'CmdName': 'minecraft:the_nether'}, 
    {'Name': 'End', 'CmdName': 'minecraft:the_end'},
    {'Name': 'Anu\'s Lair', 'CmdName': 'fossil:anu_lair'}
]

defaultModifiers = {
    'Dimension': 'minecraft:overworld',
    'XCoordinate': 0,
    'ZCoordinate': 0,

    'GridSearch': False,
    'GridRange': 250,
    
    'OverworldLockdownRange': 1200,
    'NetherLockdownRange': 600,

    'SearchFor': 'biome',
    'Target': ''
}