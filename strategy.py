

def nearest(enemies):
    if enemies:
        enemies.sort(key=lambda enemy: enemy.distance_travelled)
        return enemies[-1]