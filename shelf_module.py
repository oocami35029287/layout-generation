import math

class Module(object):
    def __init__(self, module_size, shelves):
        self.module_size = module_size  # (width, height)
        self.shelves = shelves  # [[posx, posy, rot(deg)]]
    def __str__(self):
        return f"Module(module_size={self.module_size}, shelves={self.shelves})"
    def get_size(self):
        return self.module_size 

class Module1(Module):  # along walls
    def __init__(self, aisle_size, shelf_size):
        module_size = (shelf_size[0], shelf_size[1] + aisle_size)
        shelves = [[0, 0, 0]]
        super().__init__(module_size, shelves)
    def __str__(self):
        return f"Module1(module_size={self.module_size}, shelves={self.shelves})"
    
    @classmethod
    def generate_modules(cls, aisle_size_full, shelf_size):
        aisle_size = int(aisle_size_full / 2)
        module1 = cls(aisle_size, shelf_size)
        return module1

class Module2(Module):  # side by side
    def __init__(self, aisle_size, shelf_size, adjac_num):
        module_size = (shelf_size[0] * adjac_num + aisle_size * 2, (shelf_size[1] + aisle_size) * 2)
        shelves = []
        for i in range(adjac_num):
            shelf1 = [aisle_size + shelf_size[0]*i, aisle_size + shelf_size[1], 0]
            shelf2 = [aisle_size + shelf_size[0]*(i+1), aisle_size + shelf_size[1], -180]
            shelves = shelves + [shelf1, shelf2]
        super().__init__(module_size, shelves)

    @classmethod
    def generate_modules(cls, aisle_size_full, shelf_size, space_size):
        aisle_size = math.ceil(aisle_size_full / 2)
        max_value = space_size[0] if space_size[0] > space_size[1] else space_size[1]
        max_adjac = math.ceil(max_value / ((shelf_size[1] + aisle_size) * 2) / 2)
        module2 = {}
        for i in range(max_adjac):
            module2[i] = cls(aisle_size, shelf_size, (i+1))
        return module2
    def __str__(self):
        return f"Module2(module_size={self.module_size}, shelves={self.shelves})"
class ModuleContainer():
    def __init__(self, module, pos, rot):
        self.module = module
        self.pos = pos
        self.rot = rot  #degree
    def __str__(self):
        return f"Module(module_size={self.module.module_size}, pos={self.pos,self.rot})" 
    def get_pos(self):
        return self.pos
    def get_rot(self):
        return self.rot
    def get_module(self):
        return self.module
    def set_pos(self,pos):
        self.pos = pos
    def set_inner_module_rot(self):
        self.rot = 90
        print("inner rot", self.pos[0]+self.module.get_size()[1],self.pos[1])
    def get_shelves(self):
        all_shelves = []
        for shelf in self.module.shelves:
            shelf_posx = shelf[0]*math.cos(math.radians(self.rot))-shelf[1]*math.sin(math.radians(self.rot))+self.pos[0]
            shelf_posy = shelf[0]*math.sin(math.radians(self.rot))+shelf[1]*math.cos(math.radians(self.rot))+self.pos[1]
            # rotation_matrix = cv2.getRotationMatrix2D((0, 0), rotation, 1)
            # print("module",self.pos[0],self.pos[1])
            # print("shelf",shelf_posx,shelf_posy)
            rot = shelf[2]+self.rot
            while rot>180:
                rot = rot-360
            all_shelves.append({'x': shelf_posx, 'y': shelf_posy, 'rot': rot})
        return all_shelves
    def get_sq_problem(self):
        return {"width":  self.module.get_size()[0], "height": self.module.get_size()[1], "rotatable": True}
if __name__ == "__main__":
    # Example usage:
    aisle_size = 30
    shelf_size = [80, 40]
    space_size = [400, 300]
    module1 = Module1.generate_modules(aisle_size, shelf_size)
    module2_array = Module2.generate_modules(aisle_size, shelf_size, space_size)
    module = []
    for i in range(10):
        module.append(ModuleContainer(module1,(i,i),i*10))
    for i in module:
        print(i)
    
    for module2 in generated_module2_array.values():
        print(module2)
