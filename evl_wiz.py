import random

# Base Character class
class Character:
    def __init__(self, name, health, attack_power):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.max_health = health  
        # Status flags for abilities
        self.evade_next = False     # completely dodge next attack
        self.shield_next = False    # reduce next attack

    def attack(self, opponent):
        """Basic attack with randomized damage."""
        min_dmg = max(1, int(self.attack_power * 0.8))
        max_dmg = int(self.attack_power * 1.2)
        damage = random.randint(min_dmg, max_dmg)
        print(f"{self.name} attacks {opponent.name} for {damage} damage!")
        opponent.take_damage(damage)

    def take_damage(self, damage):
        """Apply damage, considering evade/shield effects."""
        if self.evade_next:
            print(f"{self.name} evades the attack and takes no damage!")
            self.evade_next = False
            return

        if self.shield_next:
            reduced = max(0, damage // 2)
            print(f"{self.name}'s shield reduces the damage from {damage} to {reduced}!")
            damage = reduced
            self.shield_next = False

        self.health -= damage
        print(f"{self.name} now has {self.health} health.")

        if self.health <= 0:
            print(f"{self.name} has been defeated!")

    def heal(self):
        """Restore health without exceeding max_health."""
        heal_amount = 20
        if self.health >= self.max_health:
            print(f"{self.name} is already at full health!")
            return

        new_health = min(self.max_health, self.health + heal_amount)
        actual_heal = new_health - self.health
        self.health = new_health
        print(f"{self.name} heals for {actual_heal} points! Current health: {self.health}/{self.max_health}")

    def display_stats(self):
        print(f"{self.name}'s Stats - Health: {self.health}/{self.max_health}, Attack Power: {self.attack_power}")

    def use_ability(self, opponent):
        """Default: no abilities (overridden in subclasses)."""
        print(f"{self.name} has no special abilities.")


# Warrior class (inherits from Character)
class Warrior(Character):
    def __init__(self, name):
        super().__init__(name, health=140, attack_power=25)

    def use_ability(self, opponent):
        print("\nWarrior Abilities:")
        print("1. Power Strike (heavy single attack)")
        print("2. Shield Block (halve damage of next incoming attack)")
        choice = input("Choose a Warrior ability: ")

        if choice == '1':
            bonus = 15
            damage = self.attack_power + bonus
            print(f"{self.name} uses Power Strike for {damage} damage!")
            opponent.take_damage(damage)
        elif choice == '2':
            self.shield_next = True
            print(f"{self.name} raises a shield and will take reduced damage from the next attack!")
        else:
            print("Invalid ability choice, turn wasted!")


# Mage class (inherits from Character)
class Mage(Character):
    def __init__(self, name):
        super().__init__(name, health=100, attack_power=35)

    def use_ability(self, opponent):
        print("\nMage Abilities:")
        print("1. Fireball (high damage spell)")
        print("2. Mana Shield (reduce damage from the next attack)")
        choice = input("Choose a Mage ability: ")

        if choice == '1':
            min_dmg = int(self.attack_power * 1.1)
            max_dmg = int(self.attack_power * 1.5)
            damage = random.randint(min_dmg, max_dmg)
            print(f"{self.name} casts Fireball for {damage} damage!")
            opponent.take_damage(damage)
        elif choice == '2':
            self.shield_next = True
            print(f"{self.name} conjures a Mana Shield to reduce damage from the next attack!")
        else:
            print("Invalid ability choice, turn wasted!")


# EvilWizard class (inherits from Character)
class EvilWizard(Character):
    def __init__(self, name):
        super().__init__(name, health=150, attack_power=15)

    def regenerate(self):
        """Wizard regenerates a small amount of health each turn."""
        regen_amount = 5
        if self.health <= 0:
            return

        new_health = min(self.max_health, self.health + regen_amount)
        actual = new_health - self.health
        self.health = new_health
        print(f"{self.name} regenerates {actual} health! Current health: {self.health}/{self.max_health}")


# Archer class
class Archer(Character):
    def __init__(self, name):
        super().__init__(name, health=110, attack_power=20)

    def use_ability(self, opponent):
        print("\nArcher Abilities:")
        print("1. Quick Shot (two rapid, lighter attacks)")
        print("2. Evade (completely dodge the next attack)")
        choice = input("Choose an Archer ability: ")

        if choice == '1':
            # Two weaker hits
            for i in range(2):
                min_dmg = max(1, int(self.attack_power * 0.5))
                max_dmg = int(self.attack_power * 0.9)
                damage = random.randint(min_dmg, max_dmg)
                print(f"{self.name} fires arrow {i+1} for {damage} damage!")
                opponent.take_damage(damage)
                if opponent.health <= 0:
                    break
        elif choice == '2':
            self.evade_next = True
            print(f"{self.name} prepares to Evade the next incoming attack!")
        else:
            print("Invalid ability choice, turn wasted!")


# Paladin class
class Paladin(Character):
    def __init__(self, name):
        super().__init__(name, health=130, attack_power=22)

    def use_ability(self, opponent):
        print("\nPaladin Abilities:")
        print("1. Holy Strike (attack with bonus holy damage)")
        print("2. Divine Shield (block next attack and heal slightly)")
        choice = input("Choose a Paladin ability: ")

        if choice == '1':
            bonus = random.randint(8, 15)
            damage = self.attack_power + bonus
            print(f"{self.name} smites with Holy Strike for {damage} damage!")
            opponent.take_damage(damage)
        elif choice == '2':
            self.evade_next = True  # next attack fully dodged
            heal_amount = 10
            old_health = self.health
            self.health = min(self.max_health, self.health + heal_amount)
            actual = self.health - old_health
            print(f"{self.name} is wrapped in Divine Shield, will fully block the next attack and heals for {actual}!")
        else:
            print("Invalid ability choice, turn wasted!")


def create_character():
    print("Choose your character class:")
    print("1. Warrior")
    print("2. Mage")
    print("3. Archer") 
    print("4. Paladin")  

    class_choice = input("Enter the number of your class choice: ")
    name = input("Enter your character's name: ")

    if class_choice == '1':
        return Warrior(name)
    elif class_choice == '2':
        return Mage(name)
    elif class_choice == '3':
        return Archer(name)
    elif class_choice == '4':
        return Paladin(name)
    else:
        print("Invalid choice. Defaulting to Warrior.")
        return Warrior(name)


def battle(player, wizard):
    print(f"\nA dark presence looms... The evil wizard {wizard.name} appears!")
    while wizard.health > 0 and player.health > 0:
        print("\n--- Your Turn ---")
        print("1. Attack")
        print("2. Use Special Ability")
        print("3. Heal")
        print("4. View Stats")

        choice = input("Choose an action: ")

        if choice == '1':
            player.attack(wizard)
        elif choice == '2':
            player.use_ability(wizard)
        elif choice == '3':
            player.heal()
        elif choice == '4':
            player.display_stats()
            wizard.display_stats()
        else:
            print("Invalid choice. Turn skipped!")

        # Check if wizard is defeated before it can act
        if wizard.health <= 0:
            break

        print("\n--- Evil Wizard's Turn ---")
        wizard.regenerate()
        if wizard.health > 0:
            wizard.attack(player)

        if player.health <= 0:
            print(f"{player.name} has fallen in battle...")
            break

    # End-of-battle messages
    if wizard.health <= 0 and player.health > 0:
        print(f"\nVictory! The evil wizard {wizard.name} has been defeated by {player.name}!")
    elif player.health <= 0 and wizard.health > 0:
        print(f"\nDefeat... {player.name} was slain by the evil wizard {wizard.name}.")
    else:
        print("\nBoth combatants have fallen. It's a draw!")


def main():
    player = create_character()
    wizard = EvilWizard("The Dark Wizard")
    battle(player, wizard)


if __name__ == "__main__":
    main()