import regex as re
import json
import os

def formatName(move_name):
    move = re.sub(r'[_\s]', '-', str(move_name).strip(':').lower())
    return move

def initVars():
    return False, False, True, '', 0, 0, 0, 0

print(os.getcwd())
changed_moves = []

with open('text_files/dps/move_changes_raw.txt', 'r') as file:
    power_changed, energy_changed, new_move, move_name, move_old_power, move_new_power, move_old_energy, move_new_energy = initVars()
    for line in file:
        line = line.strip()
        if line == '':
            if power_changed:
                changed_moves.append({
                    'Name': move_name,
                    'OldPower': move_old_power,
                    'NewPower': move_new_power,
                    'OldEnergy': move_old_energy,
                    'NewEnergy': move_new_energy,
                    'PowerChanged': power_changed,
                    'EnergyChanged': energy_changed
                })
            power_changed, energy_changed, new_move, move_name, move_old_power, move_new_power, move_old_energy, move_new_energy = initVars()
            continue

        if new_move:
            move_name = formatName(line)
            new_move = False
        
        if 'power' in line:
            power_changed = True
            # â†’ is the →
            move_powers = re.split('â†’', line[7:])
            move_old_power = float(move_powers[0].strip())
            move_new_power = float(move_powers[1].strip())

        if 'energy_delta' in line:
            energy_changed = True
            # â†’ is the →
            move_energies = re.split('â†’', line[13:])
            move_old_energy = float(move_energies[0].strip())
            move_new_energy = float(move_energies[1].strip())

with open('text_files/dps/move_changes.txt', 'w') as file:
    file.write(json.dumps(changed_moves))