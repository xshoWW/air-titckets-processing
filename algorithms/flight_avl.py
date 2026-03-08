from entities.flight import Flight

class AVLNode:
    def __init__(self, flight):
        self.flight = flight
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None
    
    def _height(self, node):
        if not node:
            return 0
        return node.height
    
    def _update_height(self, node):
        if not node:
            return
        node.height = 1 + max(self._height(node.left), self._height(node.right))
    
    def _balance_factor(self, node):
        if not node:
            return 0
        return self._height(node.left) - self._height(node.right)
    
    def _rotate_right(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        self._update_height(y)
        self._update_height(x)
        return x
    
    def _rotate_left(self, x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        self._update_height(x)
        self._update_height(y)
        return y
    
    def _balance(self, node):
        if not node:
            return node
        bf = self._balance_factor(node)
        if bf > 1:
            if self._balance_factor(node.left) < 0:
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        if bf < -1:
            if self._balance_factor(node.right) > 0:
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        return node
    
    def insert(self, flight):
        self.root = self._insert(self.root, flight)
    
    def _insert(self, node, flight):
        if not node:
            return AVLNode(flight)
        if flight.flight_number < node.flight.flight_number:
            node.left = self._insert(node.left, flight)
        elif flight.flight_number > node.flight.flight_number:
            node.right = self._insert(node.right, flight)
        else:
            return node
        self._update_height(node)
        return self._balance(node)
    
    def find(self, flight_number):
        return self._find(self.root, flight_number)
    
    def _find(self, node, flight_number):
        if not node:
            return None
        if flight_number < node.flight.flight_number:
            return self._find(node.left, flight_number)
        if flight_number > node.flight.flight_number:
            return self._find(node.right, flight_number)
        return node.flight
    
    def delete(self, flight_number):
        self.root = self._delete(self.root, flight_number)
    
    def _delete(self, node, flight_number):
        if not node:
            return None
        if flight_number < node.flight.flight_number:
            node.left = self._delete(node.left, flight_number)
        elif flight_number > node.flight.flight_number:
            node.right = self._delete(node.right, flight_number)
        else:
            if not node.left:
                return node.right
            if not node.right:
                return node.left
            min_node = self._find_min(node.right)
            node.flight = min_node.flight
            node.right = self._delete(node.right, min_node.flight.flight_number)
        self._update_height(node)
        return self._balance(node)
    
    def _find_min(self, node):
        while node.left:
            node = node.left
        return node
    
    def reverse_traversal(self):
        result = []
        self._reverse(self.root, result)
        return result
    
    def _reverse(self, node, result):
        if node:
            self._reverse(node.left, result)
            self._reverse(node.right, result)
            result.append(node.flight)
    
    def print_tree_text(self):
        if not self.root:
            print("   🌱 Дерево пусто")
            return
        
        print("\n" + "=" * 60)
        print("📐 СТРУКТУРА АВЛ-ДЕРЕВА")
        print("=" * 60)
        
        print(f"КОРЕНЬ: {self.root.flight}")
        print()
        
        if self.root.left:
            print("  ЛЕВОЕ ПОДДЕРЕВО (меньше корня):")
            self._print_subtree(self.root.left, self.root, "    ", "левое")
        else:
            print("  Левое поддерево: пусто")
        
        print()
        
        if self.root.right:
            print("  ПРАВОЕ ПОДДЕРЕВО (больше корня):")
            self._print_subtree(self.root.right, self.root, "    ", "правое")
        
        print("=" * 60)
    
    def _print_subtree(self, node, parent, indent, direction):
        if not node:
            return
        
        if direction == "левое":
            dir_text = f"левое поддерево (меньше {parent.flight})"
        else:
            dir_text = f"правое поддерево (больше {parent.flight})"
        
        print(f"{indent}└─ Узел: {node.flight} (родитель: {parent.flight}, {dir_text})")
        
        if node.left or node.right:
            new_indent = indent + "   "
            if node.left:
                self._print_subtree(node.left, node, new_indent, "левое")
            if node.right:
                self._print_subtree(node.right, node, new_indent, "правое")