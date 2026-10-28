from collections import defaultdict

class ShoppingCart:
    def __init__(self):
        self.cart = defaultdict(int)
        self.undoStack = []
        self.redoStack = []
        self.curr = -1
        self.recording = False
        self.history = []

    def add_item(self, item_id: str, quantity: int): 
        self.redoStack = []
        self.cart[item_id] += quantity
        self.undoStack.append(("remove", quantity, item_id))

        if self.recording == True:
            self.history[self.curr].append(("remove", quantity, item_id))

        return True

    def remove_item(self, item_id: str, quantity: int):
        if item_id not in self.cart:
            return False
        
        self.redoStack = []
        quantity = min(quantity, self.cart[item_id])
        self.cart[item_id] -= quantity
        if self.cart[item_id] == 0:
            del self.cart[item_id]

        if self.recording == True:
            self.history[self.curr].append(("add", quantity, item_id))

        self.undoStack.append(("add", quantity, item_id))
        return True
    def undo(self):
        if not self.undoStack:
            return False
        
        action, qty, item_id = self.undoStack.pop()
        if action == "add":
            self.cart[item_id] += qty
            self.redoStack.append(("remove", qty, item_id))
            if self.recording == True:
                self.history[self.curr].append(("remove", qty, item_id))
            
        elif action == "remove":
            self.cart[item_id] -= qty
            self.redoStack.append(("add", qty, item_id))
            if self.cart[item_id] == 0:
                del self.cart[item_id]
            if self.recording == True:
                self.history[self.curr].append(("add", qty, item_id))
        
        return True
    def redo(self):
        if not self.redoStack:
            return False
        
        action, qty, item_id = self.redoStack.pop()
        if action == "add":
            self.cart[item_id] += qty
            self.undoStack.append(("remove", qty, item_id))
            if self.recording == True:
                self.history[self.curr].append(("remove", qty, item_id))
        elif action == "remove":
            self.cart[item_id] -= qty
            self.undoStack.append(("add", qty, item_id))
            if self.cart[item_id] == 0:
                del self.cart[item_id]
            if self.recording == True:
                self.history[self.curr].append(("add", qty, item_id))
        
        return True
    def items(self) -> dict[str, int]:
        return self.cart.copy()

    def begin(self):
        self.recording = True
        self.curr += 1
        self.history.append([])
    
    def commit(self):
        if not self.history:
            return

        child = self.history.pop()
        if self.history:
            self.history[-1].extend(child)

        self.curr = len(self.history) - 1
        self.recording = bool(self.history)

    def abort(self):
        if self.curr == -1:
            return
        stack = self.history.pop()
        while stack:
            action, qty, item_id = stack.pop()
            if action == "add":
                self.cart[item_id] += qty
                self.undoStack.append(("remove", qty, item_id))
            elif action == "remove":
                self.cart[item_id] -= qty
                self.undoStack.append(("add", qty, item_id))
                if self.cart[item_id] == 0:
                    del self.cart[item_id]

        self.curr -= 1
        if not self.history:
            self.recording = False
        

def test():
    cart = ShoppingCart()

    cart.undo()
    cart.redo()
    assert cart.items() == {}

    cart.add_item("apple", 3)
    cart.add_item("banana", 2)
    assert cart.items() == {"apple": 3, "banana": 2}

    cart.remove_item("apple", 5)
    assert cart.items() == {"banana": 2}

    cart.undo()
    assert cart.items() == {"apple": 3, "banana": 2}
    cart.undo()
    assert cart.items() == {"apple": 3}
    cart.redo()
    assert cart.items() == {"apple": 3, "banana": 2}

    cart.undo()
    cart.add_item("pear", 1)
    cart.redo()
    assert cart.items() == {"apple": 3, "pear": 1}

    cart.undo()
    cart.remove_item("missing", 2)
    cart.redo()
    assert cart.items() == {"apple": 3, "pear": 1}

    snapshot = cart.items()
    snapshot["apple"] = 999
    assert cart.items()["apple"] == 3

    print("All tests passed!")

test()