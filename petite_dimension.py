import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Paramètres de la simulation
num_grains = 20  # Nombre de grains
size_range = (1, 3)  # Taille des grains (rayon)
speed_range = (0.1, 0.5)  # Vitesse des grains (réduite)
prob_collage = 0.1  # Probabilité de collage lors d'une collision (réduite)
critical_speed = 0.3  # Vitesse critique pour décider entre rebond et collage

# Dimensions de la zone de simulation
width, height = 100, 100

# Initialisation des grains
grains = []
for _ in range(num_grains):
    grain = {
        'pos': np.array([np.random.uniform(0, width), np.random.uniform(0, height)]),
        'vel': np.random.uniform(-speed_range[1], speed_range[1], size=2),
        'radius': np.random.uniform(size_range[0], size_range[1]),
        'color': np.random.rand(3,)
    }
    grains.append(grain)

def update_grains(grains):
    for grain in grains:
        # Mise à jour de la position
        grain['pos'] += grain['vel']
        
        # Gestion des collisions avec les parois
        if grain['pos'][0] - grain['radius'] < 0 or grain['pos'][0] + grain['radius'] > width:
            grain['vel'][0] *= -1
        if grain['pos'][1] - grain['radius'] < 0 or grain['pos'][1] + grain['radius'] > height:
            grain['vel'][1] *= -1

    # Gestion des collisions entre grains
    for i in range(len(grains)):
        for j in range(i + 1, len(grains)):
            grain1 = grains[i]
            grain2 = grains[j]
            dist = np.linalg.norm(grain1['pos'] - grain2['pos'])
            if dist < grain1['radius'] + grain2['radius']:
                relative_speed = np.linalg.norm(grain1['vel'] - grain2['vel'])
                if relative_speed > critical_speed and np.random.rand() > prob_collage:
                    # Rebonds élastiques
                    direction = (grain1['pos'] - grain2['pos']) / dist
                    grain1['vel'], grain2['vel'] = grain2['vel'] - 2 * np.dot(grain2['vel'], direction) * direction, grain1['vel'] - 2 * np.dot(grain1['vel'], direction) * direction
                else:
                    # Collage des grains
                    total_radius = grain1['radius'] + grain2['radius']
                    new_pos = (grain1['pos'] * grain1['radius'] + grain2['pos'] * grain2['radius']) / total_radius
                    new_vel = (grain1['vel'] * grain1['radius'] + grain2['vel'] * grain2['radius']) / total_radius
                    new_grain = {
                        'pos': new_pos,
                        'vel': new_vel,
                        'radius': total_radius,
                        'color': (grain1['color'] + grain2['color']) / 2
                    }
                    grains[i] = new_grain
                    grains.pop(j)
                    break  # Sortir de la boucle intérieure

# Collecte des données sans instabilité et turbulence
sizes_over_time_no_turbulence = []
num_grains_over_time_no_turbulence = []
velocities_over_time_no_turbulence = []

def simulate_no_turbulence(iterations):
    global grains, sizes_over_time_no_turbulence, num_grains_over_time_no_turbulence, velocities_over_time_no_turbulence
    grains = []
    for _ in range(num_grains):
        grain = {
            'pos': np.array([np.random.uniform(0, width), np.random.uniform(0, height)]),
            'vel': np.random.uniform(-speed_range[1], speed_range[1], size=2),
            'radius': np.random.uniform(size_range[0], size_range[1]),
            'color': np.random.rand(3,)
        }
        grains.append(grain)
    
    for _ in range(iterations):
        update_grains(grains)
        current_sizes = [grain['radius'] for grain in grains]
        current_velocities = [np.linalg.norm(grain['vel']) for grain in grains]
        
        sizes_over_time_no_turbulence.append(np.mean(current_sizes))
        num_grains_over_time_no_turbulence.append(len(grains))
        velocities_over_time_no_turbulence.append(np.mean(current_velocities))

simulate_no_turbulence(200)

# Temps (simulé ici)
time = np.arange(1, len(sizes_over_time_no_turbulence) + 1)

# Tracer les données collectées sans instabilité et turbulence
plt.figure(figsize=(12, 8))

# Évolution des tailles des grains sans instabilité et turbulence
plt.subplot(3, 1, 1)
plt.plot(time, sizes_over_time_no_turbulence, marker='o', linestyle='-', color='b', label='Taille moyenne des grains')
plt.xlabel('Temps')
plt.ylabel('Taille moyenne')
plt.legend()

# Nombre total de grains sans instabilité et turbulence
plt.subplot(3, 1, 2)
plt.plot(time, num_grains_over_time_no_turbulence, marker='o', linestyle='-', color='g', label='Nombre total de grains')
plt.xlabel('Temps')
plt.ylabel('Nombre de grains')
plt.legend()

# Vitesse moyenne des grains sans instabilité et turbulence
plt.subplot(3, 1, 3)
plt.plot(time, velocities_over_time_no_turbulence, marker='o', linestyle='-', color='r', label='Vitesse moyenne des grains')
plt.xlabel('Temps')
plt.ylabel('Vitesse moyenne')
plt.legend()

plt.tight_layout()
plt.show()

num_grains = 20  # Nombre de grains
size_range = (1, 3)  # Taille des grains (rayon)
speed_range = (0.1, 0.5)  # Vitesse des grains (réduite)
prob_collage = 0.1  # Probabilité de collage lors d'une collision (réduite)
critical_speed = 0.3  # Vitesse critique pour décider entre rebond et collage

# Dimensions de la zone de simulation
width, height = 100, 100
turbulence_intensity = 0.1  # Intensité des perturbations turbulentes

grains = []
for _ in range(num_grains):
    grain = {
        'pos': np.array([np.random.uniform(0, width), np.random.uniform(0, height)]),
        'vel': np.random.uniform(-speed_range[1], speed_range[1], size=2),
        'radius': np.random.uniform(size_range[0], size_range[1]),
        'color': np.random.rand(3,)
    }
    grains.append(grain)

# Collecte des données
sizes_over_time = []
num_grains_over_time = []
velocities_over_time = []

def update_grains(grains):
    global sizes_over_time, num_grains_over_time, velocities_over_time
    current_sizes = []
    current_velocities = []
    
    for grain in grains:
        # Ajout de perturbations turbulentes
        grain['vel'] += np.random.uniform(-turbulence_intensity, turbulence_intensity, size=2)
        
        # Mise à jour de la position
        grain['pos'] += grain['vel']
        
        # Gestion des collisions avec les parois
        if grain['pos'][0] - grain['radius'] < 0 or grain['pos'][0] + grain['radius'] > width:
            grain['vel'][0] *= -1
        if grain['pos'][1] - grain['radius'] < 0 or grain['pos'][1] + grain['radius'] > height:
            grain['vel'][1] *= -1
        
        current_sizes.append(grain['radius'])
        current_velocities.append(np.linalg.norm(grain['vel']))

    # Gestion des collisions entre grains
    for i in range(len(grains)):
        for j in range(i + 1, len(grains)):
            grain1 = grains[i]
            grain2 = grains[j]
            dist = np.linalg.norm(grain1['pos'] - grain2['pos'])
            if dist < grain1['radius'] + grain2['radius']:
                relative_speed = np.linalg.norm(grain1['vel'] - grain2['vel'])
                if relative_speed > critical_speed and np.random.rand() > prob_collage:
                    # Rebonds élastiques
                    direction = (grain1['pos'] - grain2['pos']) / dist
                    grain1['vel'], grain2['vel'] = grain2['vel'] - 2 * np.dot(grain2['vel'], direction) * direction, grain1['vel'] - 2 * np.dot(grain1['vel'], direction) * direction
                else:
                    # Collage des grains
                    total_radius = grain1['radius'] + grain2['radius']
                    new_pos = (grain1['pos'] * grain1['radius'] + grain2['pos'] * grain2['radius']) / total_radius
                    new_vel = (grain1['vel'] * grain1['radius'] + grain2['vel'] * grain2['radius']) / total_radius
                    new_grain = {
                        'pos': new_pos,
                        'vel': new_vel,
                        'radius': total_radius,
                        'color': (grain1['color'] + grain2['color']) / 2
                    }
                    grains[i] = new_grain
                    grains.pop(j)
                    break  # Sortir de la boucle intérieure

    sizes_over_time.append(np.mean(current_sizes))
    num_grains_over_time.append(len(grains))
    velocities_over_time.append(np.mean(current_velocities))

def animate(frame):
    update_grains(grains)
    ax.clear()
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    for grain in grains:
        circle = plt.Circle(grain['pos'], grain['radius'], color=grain['color'])
        ax.add_patch(circle)

# Création de la figure
fig, ax = plt.subplots()
ax.set_xlim(0, width)
ax.set_ylim(0, height)

# Animation
ani = FuncAnimation(fig, animate, frames=200, interval=50)
plt.show()

# Tracer les données collectées
plt.figure(figsize=(12, 8))

# Évolution des tailles des grains
plt.subplot(3, 1, 1)
plt.plot(sizes_over_time, label='Taille moyenne des grains')
plt.xlabel('Temps')
plt.ylabel('Taille moyenne')
plt.legend()

# Nombre total de grains
plt.subplot(3, 1, 2)
plt.plot(num_grains_over_time, label='Nombre total de grains')
plt.xlabel('Temps')
plt.ylabel('Nombre de grains')
plt.legend()

# Vitesse moyenne des grains
plt.subplot(3, 1, 3)
plt.plot(velocities_over_time, label='Vitesse moyenne des grains')
plt.xlabel('Temps')
plt.ylabel('Vitesse moyenne')
plt.legend()

plt.tight_layout()
plt.show()