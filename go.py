import tkinter as tk
import random
import math

# List of rainbow colors
rainbow_colors = ["#FF0000", "#FF7F00", "#FFFF00", "#00FF00", "#0000FF", "#4B0082", "#8B00FF"]

# Function to get a random color
def get_random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

# Function to change the text color more frequently
def update_text_color():
    new_color = get_random_color()
    canvas.itemconfig(text_id, fill=new_color)
    root.after(500, update_text_color)  # Change color every 0.5 second

# Function to create a rotating rainbow circle
def create_rotating_rainbow_circle():
    canvas.delete("ring")
    segments = len(rainbow_colors)
    angle_step = 360 / segments
    radius = 190
    ring_thickness = 30

    for i, color in enumerate(rainbow_colors):
        start_angle = i * angle_step
        canvas.create_arc(
            center_x - radius, center_y - radius,
            center_x + radius, center_y + radius,
            start=start_angle,
            extent=angle_step,
            outline=color, style="arc", width=ring_thickness,
            tags="ring"
        )

    rainbow_colors.insert(0, rainbow_colors.pop())
    root.after(45, create_rotating_rainbow_circle)

# Function to create a bursting cracker effect
def create_cracker(x, y):
    for _ in range(20):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 6)
        dx = speed * math.cos(angle)
        dy = speed * math.sin(angle)
        particle_id = canvas.create_oval(
            x - 2, y - 2, x + 2, y + 2,
            fill=get_random_color(), outline=""
        )
        animate_particle(particle_id, dx, dy, 0)

# Function to animate each particle
def animate_particle(particle_id, dx, dy, age):
    if age < 15:
        canvas.move(particle_id, dx, dy)
        canvas.after(50, lambda: animate_particle(particle_id, dx, dy, age + 1))
    else:
        canvas.delete(particle_id)

# Function to create heart shape burst pointing downward
def create_heart_burst(x, y):
    num_particles = 50
    for i in range(num_particles):
        angle = (i / num_particles) * 2 * math.pi
        dx = 16 * math.sin(angle) ** 3
        dy = -(13 * math.cos(angle) - 5 * math.cos(2 * angle) - 2 * math.cos(3 * angle) - math.cos(4 * angle))  # Pointing downward
        particle_id = canvas.create_oval(
            x - 2, y - 2, x + 2, y + 2,
            fill=get_random_color(), outline=""
        )
        animate_heart_particle(particle_id, dx, dy, 0)

# Function to animate heart burst particles, making them move downward
def animate_heart_particle(particle_id, dx, dy, age):
    if age < 15:
        canvas.move(particle_id, dx, dy)
        canvas.after(50, lambda: animate_heart_particle(particle_id, dx * 0.9, dy * 0.9, age + 1))  # Gradually reduce speed for a smoother fall
    else:
        canvas.delete(particle_id)

# Function to create triangle burst for flower pot cracker
def create_triangle_burst(x, y):
    num_particles = 30
    for i in range(num_particles):
        angle = (i / num_particles) * 2 * math.pi
        radius = random.uniform(15, 30)
        dx = radius * math.cos(angle)
        dy = radius * math.sin(angle)
        particle_id = canvas.create_oval(
            x - 2, y - 2, x + 2, y + 2,
            fill=get_random_color(), outline=""
        )
        animate_particle(particle_id, dx, dy, 0)

# Function to create the sky shot cracker animation with trail hiding
def create_sky_shot(x, y):
    height = random.randint(100, 300)
    trail = create_ascending_particle(x, y, height)
    root.after(700, lambda: create_heart_burst(x, y))  # Burst as heart shape at peak
    root.after(800, lambda: canvas.delete(trail))  # Hide trail after burst

# Function to animate a sky shot particle going up with trail
def create_ascending_particle(x, y, height, step=0, trail=None):
    if trail is None:
        trail = canvas.create_line(x, y, x, y - height, fill="white")
    if step < height:
        canvas.move(trail, 0, -5)
        canvas.after(20, lambda: create_ascending_particle(x, y - 5, height, step + 5, trail))
    return trail

# Function to create the flower pot cracker
def create_flower_pot_cracker(x, y):
    for _ in range(5):
        angle = random.uniform(-math.pi / 6, math.pi / 6)
        speed = random.uniform(5, 8)
        dx = speed * math.cos(angle)
        dy = speed * math.sin(angle)
        particle_id = canvas.create_oval(
            x - 3, y - 3, x + 3, y + 3,
            fill=get_random_color(), outline=""
        )
        animate_flower_pot_particle(particle_id, dx, dy, 0)

    root.after(600, lambda: create_triangle_burst(x, y))

# Function to animate upward particles of flower pot cracker
def animate_flower_pot_particle(particle_id, dx, dy, age):
    if age < 10:
        canvas.move(particle_id, dx, dy)
        canvas.after(50, lambda: animate_flower_pot_particle(particle_id, dx, dy, age + 1))
    else:
        canvas.delete(particle_id)

# Function to periodically launch different types of crackers at random positions
def launch_crackers():
    x = random.randint(100, 400)
    y = random.randint(100, 400)
    choice = random.choice(["cracker", "flower_pot", "sky_shot"])
    if choice == "cracker":
        create_cracker(x, y)
    elif choice == "flower_pot":
        create_flower_pot_cracker(x, y)
    elif choice == "sky_shot":
        create_sky_shot(x, y)
    root.after(800, launch_crackers)

# Set up the Tkinter window
root = tk.Tk()
root.title("Happy Children's Day Greeting")
root.geometry("500x500")
root.configure(bg="black")

# Create a canvas widget
canvas = tk.Canvas(root, width=500, height=500, bg="black", highlightthickness=0)
canvas.pack()

# Center position for the circle and text
center_x, center_y = 250, 250

# Draw the initial rainbow circle around the text
create_rotating_rainbow_circle()

# Display the text "Happy Children's Day" in the center of the circle
text_id = canvas.create_text(center_x, center_y, text="Happy Children's Day",
                             font=("Sans serif", 24, "bold"), fill="white")

# Start the color-changing, rotation, and cracker-launching functions
update_text_color()
launch_crackers()

# Run the Tkinter event loop
root.mainloop()

