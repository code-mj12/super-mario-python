import json
import random
import os

def generate_initial_population(population_size):
    population = []
    for _ in range(population_size):
        new_level = create_random_level()
        population.append(new_level)
    return population



generated_ids = set()

def generate_unique_id():
    while True:
        random_id = random.randint(1, 1000)
        if random_id not in generated_ids:
            generated_ids.add(random_id)
            return random_id

def create_random_level():
    # Add your logic here to create a random level
    unique_id = generate_unique_id()
    level = {
        "id": unique_id,
        "length": 60,
        "level": {
            "objects": {
                "bush": [[random.randint(0, 59), 12] for _ in range(random.randint(1, 10))],
                "sky": [[random.randint(0, 59), random.randint(0, 12)] for _ in range(random.randint(1, 20))],
                "cloud": [[random.randint(0, 59), random.randint(2, 5)] for _ in range(random.randint(1, 10))],
                "pipe": [[random.randint(0, 59), random.randint(9, 12), random.randint(4, 7)] for _ in range(random.randint(1, 5))],
                "ground": [[random.randint(0, 59), random.randint(9, 16)] for _ in range(random.randint(1, 50))]
            },
            "layers": {
                "sky": {
                    "x": [0, 60],
                    "y": [0, 13]
                },
                "ground": {
                    "x": [0, 60],
                    "y": [14, 16]
                }
            },
            "entities": {
                "CoinBox": [[random.randint(0, 59), random.randint(2, 8)] for _ in range(random.randint(1, 10))],
                "coinBrick": [[random.randint(0, 59), random.randint(5, 9)] for _ in range(random.randint(1, 5))],
                "coin": [[random.randint(0, 59), random.randint(2, 12)] for _ in range(random.randint(1, 20))],
                "Goomba": [[random.randint(0, 59), random.randint(10, 15)] for _ in range(random.randint(1, 5))],
                "Koopa": [[random.randint(0, 59), random.randint(15, 40)] for _ in range(random.randint(1, 5))],
                "RandomBox": [[random.randint(0, 59), random.randint(2, 5), "RedMushroom"] for _ in range(random.randint(1, 5))]
            }
        }
    }
    return level

def calculate_fitness(level):
    # Calculate fitness based on the number of coins and enemies
    coins = len(level["level"]["entities"]["coin"])
    enemies = len(level["level"]["entities"]["Goomba"]) + len(level["level"]["entities"]["Koopa"])

    # Reward more coins and penalize more enemies
    fitness = coins - (0.5 * enemies)
    return fitness/16

def selection(population):
    # Select parents using tournament selection
    tournament_size = 4
    selected_parents = []
    
    for _ in range(len(population)):
        contenders = random.sample(population, tournament_size)
        winner = max(contenders, key=calculate_fitness)
        selected_parents.append(winner)

    return selected_parents

def crossover(parent1, parent2):
    # Perform one-point crossover on the "coin" entities
    crossover_point = random.randint(1, len(parent1["level"]["entities"]["coin"]) - 1)

    child1 = parent1.copy()
    child2 = parent2.copy()

    child1["level"]["entities"]["coin"] = parent1["level"]["entities"]["coin"][:crossover_point] + parent2["level"]["entities"]["coin"][crossover_point:]
    child2["level"]["entities"]["coin"] = parent2["level"]["entities"]["coin"][:crossover_point] + parent1["level"]["entities"]["coin"][crossover_point:]

    return child1, child2

def mutation(level, mutation_rate):
    mutated_level = level.copy()

    # Mutate coin positions with a given mutation_rate
    for i, coin in enumerate(mutated_level["level"]["entities"]["coin"]):
        if random.random() < mutation_rate:
            mutated_level["level"]["entities"]["coin"][i] = [random.randint(0, 59), random.randint(2, 12)]

    return mutated_level


def save_population(population, generation):
    if not os.path.exists("populations"):
        os.mkdir("populations")
    selected_parents=selection(population)
    print(len(selected_parents))
    for i, level in enumerate(selected_parents):
        with open(f"level_gen{generation}_ind{i}.json", "w") as f:
            json.dump(level, f, indent=4)

def main():
    population_size = 10
    generations = 10
    mutation_rate = 0.1
    population = generate_initial_population(population_size)

    for gen in range(generations):
        print(f"Generation {gen}")

        # Calculate fitness
        fitness_scores = [calculate_fitness(level) for level in population]

        # Selection
        parents = selection(population)

        # Crossover
        offspring = []
        for i in range(population_size // 2):
            parent1 = random.choice(parents)
            parent2 = random.choice(parents)
            child1, child2 = crossover(parent1, parent2)
            offspring.append(child1)
            offspring.append(child2)

        # Mutation
        mutated_offspring = [mutation(child, mutation_rate) for child in offspring]

        # Replace old population with new offspring
        population = mutated_offspring

        # Save the population
        save_population(population, gen)

    print("Evolution process completed.")

if __name__ == '__main__':
    main()
