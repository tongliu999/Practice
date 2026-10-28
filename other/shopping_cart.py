from collections import defaultdict

class RecipeCart:
    def __init__(self, recipes, discounts):
        self.cart = defaultdict(int)
        self.recipes = recipes
        self.discounts = discounts
        self.total_discount = 0
        self.used = set()
        self.versions = {}
        self.version = 1

    def add_recipe(self, recipe_id):
        if recipe_id in self.used:
            return False
        
        self.versions[self.version] = ("add", recipe_id)
        self.version += 1

        self.used.add(recipe_id)
        recipe = self.recipes[recipe_id]
        for ingredient in recipe.keys():
            if ingredient in self.discounts and self.discounts[ingredient][0] > self.cart[ingredient] and self.discounts[ingredient][0] <= self.cart[ingredient] + recipe[ingredient]:
                self.total_discount += self.discounts[ingredient][1]
            self.cart[ingredient] += recipe[ingredient]
        
        return True
    
    def remove_recipe(self, recipe_id):
        if recipe_id not in self.used:
            return False

        self.versions[self.version] = ("remove", recipe_id)
        self.version += 1

        self.used.remove(recipe_id)
        recipe = self.recipes[recipe_id]
        for ingredient in recipe.keys():
            if ingredient in self.discounts and self.discounts[ingredient][0] <= self.cart[ingredient] and self.discounts[ingredient][0] > self.cart[ingredient] - recipe[ingredient]:
                self.total_discount -= self.discounts[ingredient][1]
            self.cart[ingredient] -= recipe[ingredient]
        
        return True


    def get_total_discounts(self):
        return self.total_discount

    def get_version(self, version):
        temp_cart = defaultdict(int)

        for i in range(1, version + 1):
            action = self.versions[i]
            recipe = self.recipes[action[1]]
            if action[0] == "add":
                for i in recipe.keys():
                    temp_cart[i] += recipe[i]
            
            if action[0] == "remove":
                for i in recipe.keys():
                    temp_cart[i] -= recipe[i]

        return temp_cart

    def check_out(self, version):
        self.cart = defaultdict(int)
        self.total_discount = 0
        self.used = set()

        for i in range(1, version + 1):
            action = self.versions[i]
            if action[0] == "add":
                self.add_recipe(action[1])
            
            if action[0] == "remove":
                self.remove_recipe(action[1])

        for i in range(version + 1, len(self.versions) + 1):
            del self.versions[i]
        self.version = version + 1
        




def test_versions():
    recipes = {
        "pasta": {"tomato": 2, "garlic": 1},
        "soup": {"tomato": 3, "onion": 1},
    }
    cart = RecipeCart(recipes, {"tomato": (5, 2)})

    assert cart.get_version(0) == {}

    cart.add_recipe("pasta")          # v1
    cart.add_recipe("pasta")          # No new version
    cart.add_recipe("soup")           # v2

    assert cart.get_version(1) == recipes["pasta"]
    assert cart.get_version(2) == {
        "tomato": 5, "garlic": 1, "onion": 1
    }

    snapshot = cart.get_version(1)
    snapshot["tomato"] = 999
    assert cart.get_version(1)["tomato"] == 2
    assert cart.get_total_discounts() == 2

    cart.check_out(1)
    assert cart.get_total_discounts() == 0
    assert dict(cart.cart) == recipes["pasta"]
    assert cart.used == {"pasta"}
    assert set(cart.versions) == {1}

    cart.add_recipe("soup")           # New v2
    assert cart.get_total_discounts() == 2
    assert set(cart.versions) == {1, 2}

    cart.check_out(0)
    assert not cart.used
    assert not cart.versions
    assert cart.get_total_discounts() == 0

    cart.add_recipe("soup")           # New v1
    assert cart.get_version(1) == recipes["soup"]

    print("All version tests passed!")

test_versions()