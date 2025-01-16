
def dist(x1,y1,x2,y2):
    return ((x1 - x2)**2 + (y1 - y2)**2)**.5

# The naive implementation of a k-d-tree (k=2)
class Cell:
    def __init__(self,x,y,z, value, split):
        self.x = x
        self.y = y
        self.z = z
        self.value = value
        self.split = split
        self.left = None
        self.right = None
    
    def find_closest(self, x,y,z):
        best_z = self.z
        best_value = self.value
        best_dist = dist(x,y, self.x, self.y)
        something = False
        other_value, other_dist, other_z = None, None, None
        # From here onward it is essentially uncharted 
        # territory, we wrote it but realize it is practically unreadable

        # Essentially if two approximations are too near each other a 
        # tie breaker has to be done, to do so we use the height (which
        # we know is the most discriminatory value, not to mention
        # the one we do a lot of heuristics about).
        if self.split == "x":
            if abs(self.x - x) < 20:
                if self.left != None:
                    l_value, l_dist, l_z = self.left.find_closest(x,y,z)
                    something = True
                if self.right != None:
                    r_value, r_dist, r_z = self.right.find_closest(x,y,z)
                    something = True
                if self.right != None and self.left != None:
                    if abs(l_dist - r_dist) < 1:
                        l_diff = z - l_z
                        r_diff = z - r_z
                        if l_diff < 0 and r_diff < 0 or l_diff > 0 and r_diff > 0: 
                            if abs(l_diff) < abs(r_diff):
                                other_value, other_dist, other_z = l_value, l_dist, l_z
                            else:
                                other_value, other_dist, other_z = r_value, r_dist, r_z
                        elif l_diff < -50 and r_diff < 50:
                            other_value, other_dist, other_z = r_value, r_dist, r_z
                        elif l_diff < 50  and r_diff < -50:
                            other_value, other_dist, other_z = l_value, l_dist, l_z
                        elif abs(l_diff) < abs(r_diff):
                            other_value, other_dist, other_z = l_value, l_dist, l_z
                        else:
                            other_value, other_dist, other_z = r_value, r_dist, r_z
                    elif l_dist < r_dist:
                        other_value, other_dist, other_z = l_value, l_dist, l_z
                    else:
                        other_value, other_dist, other_z = r_value, r_dist, r_z
                elif self.left != None:
                    other_value, other_dist, other_z = l_value, l_dist, l_z
                elif self.right != None:
                    other_value, other_dist, other_z = r_value, r_dist, r_z
            elif x < self.x:
                if self.left != None:
                    other_value, other_dist, other_z = self.left.find_closest(x,y,z)
                    something = True
            else:
                if self.right != None:
                    other_value, other_dist, other_z = self.right.find_closest(x,y,z)
                    something = True
        else:
            if abs(self.y - y) < 20:
                if self.left != None:
                    l_value, l_dist, l_z = self.left.find_closest(x,y,z)
                    something = True
                if self.right != None:
                    r_value, r_dist, r_z = self.right.find_closest(x,y,z)
                    something = True
                if self.right != None and self.left != None:
                    if abs(l_dist - r_dist) < 1:
                        l_diff = z - l_z
                        r_diff = z - r_z
                        if l_diff < 0 and r_diff < 0 or l_diff > 0 and r_diff > 0: 
                            if abs(l_diff) < abs(r_diff):
                                other_value, other_dist, other_z = l_value, l_dist, l_z
                            else:
                                other_value, other_dist, other_z = r_value, r_dist, r_z
                        elif l_diff < -50 and r_diff < 50:
                            other_value, other_dist, other_z = r_value, r_dist, r_z
                        elif l_diff < 50  and r_diff < -50:
                            other_value, other_dist, other_z = l_value, l_dist, l_z
                        elif abs(l_diff) < abs(r_diff):
                            other_value, other_dist, other_z = l_value, l_dist, l_z
                        else:
                            other_value, other_dist, other_z = r_value, r_dist, r_z
                    elif l_dist < r_dist:
                        other_value, other_dist, other_z = l_value, l_dist, l_z
                    else:
                        other_value, other_dist, other_z = r_value, r_dist, r_z
                elif self.left != None:
                    other_value, other_dist, other_z = l_value, l_dist, l_z
                elif self.right != None:
                    other_value, other_dist, other_z = r_value, r_dist, r_z
            elif y < self.y:
                if self.left != None:
                    other_value, other_dist, other_z = self.left.find_closest(x,y,z)
                    something = True
            else:
                if self.right != None:
                    other_value, other_dist, other_z = self.right.find_closest(x,y,z)
                    something = True

        if something:
            if abs(other_dist - best_dist) < 1:
                diff_best = z - best_z
                diff_other = z - other_z
                if diff_best < 0 and diff_other < 0 or diff_best > 0 and diff_other > 0:
                    if abs(diff_other) < abs(diff_best):
                        best_value, best_dist, best_z = other_value, other_dist, other_z
                elif diff_best < -50 and diff_other < 50:
                    best_value, best_dist, best_z = other_value, other_dist, other_z
                elif abs(diff_other) < abs(diff_best):
                    best_value, best_dist, best_z = other_value, other_dist, other_z
            elif other_dist < best_dist:
                best_value, best_dist, best_z = other_value, other_dist, other_z
        
        return best_value, best_dist, best_z
        
    
def construct_2d_tree(lst, split = "x"):
    k = lambda item: item[0]
    if split == "y":
        k = lambda item: item[1]

    sorted_lst = sorted(lst, key=k)

    l = len(sorted_lst)
    mid = sorted_lst[l//2]
    left = sorted_lst[:l//2]
    right = sorted_lst[l//2 + 1:]
    
    root = Cell(mid[0], mid[1], mid[2], mid[3], split)

    new_split = "y"
    if split == "y":
        new_split = "x"
    
    if len(left) > 0:
        root.left = construct_2d_tree(left, new_split)
    if len(right) > 0:
        root.right = construct_2d_tree(right, new_split)

    return root