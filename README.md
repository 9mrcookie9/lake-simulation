# Lake Ecosystem Simulation

This project is a simulation of a lake ecosystem, featuring fish, plant life, and their interactions. The simulation takes into account various factors such as fish population, food sources, oxygen levels, and seasonal changes.

## Requirements

This project requires Python 3 and the libraries listed in the `requirements.txt` file.

### Installing Requirements

To install the required libraries listed in the `requirements.txt` file, you need to use pip, which is a package manager for Python. You can install these libraries by running the following command in your terminal:

```bash
pip install -r requirements.txt
```

## Files

### lake.py

This file contains the `Lake` class which represents the lake ecosystem. The lake has a certain width and height, an initial fish population, initial food amount, and a list of plants. The lake also has properties such as oxygen level, generation count, reproduction interval, and season length.

The `Lake` class also includes methods for creating log files (`create_log_files`) and logging data (`log_data`) to CSV files. These files log the fish population, food amount, and oxygen level over time.

The `update` method in the `Lake` class is responsible for updating the state of the lake ecosystem at each time step. This includes updating the generation count, current season, and the oxygen level. It also handles plant reproduction and death.

### fish.py

This file contains the `Fish` class which represents a fish in the lake. Each fish has an id, energy level, position, and velocity. The fish can move around the lake, seek food, and die.

The `Fish` class includes methods for moving (`move`), steering (`steer`), seeking food (`seek_food`), eating (`eat`), and dying (`die`). The steering behavior of the fish is determined by a combination of separation, alignment, and cohesion forces.

### plant.py

This file contains the `Plant` class which represents a plant in the lake. Each plant has a position and a food amount. The plant can generate food over time.

### fisherman.py

This file contains the `Fisherman` class which represents a fisherman in the lake. The fisherman has a probability of catching a fish and a defined fishing area.

The `Fisherman` class includes methods for fishing (`fish`) and checking if a position is within the fishing area (`is_in_fishing_area`).

### main.py

This file contains the main function to start the simulation (`start_simulation`) and a function to handle the confirmation of the simulation parameters (`on_confirm`).

The `start_simulation` function initializes the pygame, sets up the screen dimensions, clears the `/analyze` folder, initializes the lake and fisherman, and starts the main loop of the simulation.

The `on_confirm` function is triggered when the "Confirm" button is clicked in the GUI. It retrieves the values from the input fields, validates them, and starts the simulation with these parameters.

The file also includes the code for setting up the GUI for the simulation configuration.

## Usage

To run the simulation, you need to create an instance of the `Lake` class and call the `update` method in a loop. You can then use the log files to analyze the state of the lake ecosystem over time.
