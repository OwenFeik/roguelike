from random import randint

class Room:
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.grid=[[False for x in range(0,self.width)] for y in range(0,self.height)]
        if randint(0,2):
            self.grid=make_obstacle_room(self.grid)

    def center(self):
        center_x=int(((2*self.x)+self.width)/2)
        center_y=int(((2*self.y)+self.height)/2)
        return (center_x,center_y)

    def intersect(self,other):
        return (self.x <= (other.x+other.width) and (self.x+self.width) >= other.x and self.y <= (other.y+other.height) and (self.y+self.height) >= other.y)


def make_obstacle_room(grid):
    height=len(grid)
    width=len(grid[0])
    
    max_width=width//2
    max_height=height//2

    obj_width=randint(1,max_width)
    obj_height=randint(1,max_height)

    wall=randint(0,3)

    #Left wall
    if wall==0:
        top_left=randint(0,height-obj_height) #Pick position along left side that fits object
        protrusion_x=randint(0,obj_height-1) #Choose the position on the object of the protrusion
        if obj_height+top_left<=height-2: #If we can fit a protrusion above, choose an x value for it
            protrusion_y=randint(0,obj_width-1) #X value of protrusion
        else: #Otherwise, we can't fit a protrusion
            protrusion_y=-1 #Set to -1

        for y in range(0,obj_height): #Object rows
            for x in range(0,obj_width): #Object columns
                grid[y+top_left][x]=True #Set to obstacle

        
        grid[top_left+protrusion_x][obj_width]=True #Place the x direction protrusion
        if protrusion_y>=0:
            grid[top_left+obj_height][protrusion_y]=True #If we found a position for y prot, place it

    #Top wall
    elif wall==1:
        top_left=randint(0,width-obj_width)
        protrusion_y=randint(0,obj_width-1)
        if obj_width+top_left<=width-2:
            protrusion_x=randint(0,obj_height-1)
        else:
            protrusion_x=-1

        for y in range(0,obj_height):
            for x in range(0,obj_width):
                grid[y][x+top_left]=True

        grid[obj_height][top_left+protrusion_y]=True
        if protrusion_x>=0:
            grid[protrusion_x][top_left+obj_width]=True

    #Right wall
    elif wall==2:
        top_right=randint(0,height-obj_height)
        protrusion_x=randint(0,obj_height-1)
        if obj_height+top_right<=height-2:
            protrusion_y=randint(0,obj_width-1)
        else:
            protrusion_y=-1

        for y in range(0,obj_height):
            for x in range(0,obj_width):
                grid[height-(y+top_right+1)][width-(x+1)]=True
        
        grid[height-(top_right+protrusion_x+1)][width-(obj_width+1)]=True
        if protrusion_y>=0:
            grid[height-(top_right+obj_height+1)][width-(protrusion_y+1)]=True

    #Bottom wall
    elif wall==3:
        bot_left=randint(0,width-obj_width)
        protrusion_y=randint(0,obj_width-1)
        if obj_width+bot_left<=width-2:
            protrusion_x=randint(0,obj_height-1)
        else:
            protrusion_x=-1

        for y in range(0,obj_height):
            for x in range(0,obj_width):
                grid[height-(y+1)][width-(x+bot_left+1)]=True

        grid[height-(obj_height+1)][width-(bot_left+protrusion_y+1)]=True
        if protrusion_x>=0:
            grid[height-(protrusion_x+1)][width-(bot_left+obj_width+1)]=True
            
    #Add another object?
    again=randint(0,1)
    if again:
        grid=make_obstacle_room(grid)
    return grid