# Importing libraries
import tkinter as tk
import math 
import numpy
import PIL as pillow


# Creating main window
main_window = tk.Tk()
main_window.state('zoomed')
main_window.title('TrigSolver')


# Creating new canvas class with zoom and pan functionality
class ZoomableCanvas(tk.Canvas):
    def __init__(self, parent, **kwargs):
        tk.Canvas.__init__(self, parent, **kwargs)

        self.bind("<MouseWheel>", self._on_mousewheel)
        self.bind("<Control-MouseWheel>", self._on_ctrl_mousewheel)
        self.bind("<Button-4>", self._on_mousewheel)
        self.bind("<Button-5>", self._on_mousewheel)
        self.bind("<ButtonPress-1>", self._on_button_press)
        self.bind("<B1-Motion>", self._on_move)

        self._scale = 1.0
        self._min_scale = 0.1
        self._max_scale = 3.0
        self._startx = 0
        self._starty = 0

    def _on_mousewheel(self, event):
        scale_factor = 1.1 if event.num == 5 or event.delta < 0 else 0.9

        self._scale *= scale_factor
        self._scale = max(self._min_scale, min(self._max_scale, self._scale))

        self.scale("all", event.x, event.y, scale_factor, scale_factor)

    def _on_ctrl_mousewheel(self, event):
        scale_factor = 1.1 if event.delta < 0 else 0.9

        self._scale *= scale_factor
        self._scale = max(self._min_scale, min(self._max_scale, self._scale))

        self.scale("all", event.x, event.y, scale_factor, scale_factor)

    def _on_button_press(self, event):
        self._startx = event.x
        self._starty = event.y

    def _on_move(self, event):
        dx = event.x - self._startx
        dy = event.y - self._starty

        self._startx = event.x
        self._starty = event.y

        self.move("all", dx, dy)




# Getting screen dimensions
screenHeight = main_window.winfo_screenheight()
screenWidth = main_window.winfo_screenwidth()



# Output labels for calculated properties of triangle
oppositeOutputLabel = tk.Label(main_window, text='Opposite Length')
oppositeOutputLabel.place(x=650, y= 350)

oppositeOutput = tk.Label(main_window, text="N/A")
oppositeOutput.place(x=650, y= 375)


adjacentOutputLabel = tk.Label(main_window, text='Adjacent Length')
adjacentOutputLabel.place(x=650, y= 400)

adjacentOutput = tk.Label(main_window, text="N/A")
adjacentOutput.place(x=650, y= 425)


hypotenuseOutputLabel = tk.Label(main_window, text='Hypotenuse Length')
hypotenuseOutputLabel.place(x=650, y= 450)

hypotenuseOutput = tk.Label(main_window, text="N/A")
hypotenuseOutput.place(x=650, y= 475)


angleOfElevationOutputLabel = tk.Label(main_window, text='Angle of Elevation')
angleOfElevationOutputLabel.place(x=775, y=400)

angleOfElevationOutput = tk.Label(main_window, text='N/A')
angleOfElevationOutput.place(x=775, y=425)


areaOutputLabel = tk.Label(main_window, text='Area')
areaOutputLabel.place(x=775, y=350)

areaOutput = tk.Label(main_window, text='N/A')
areaOutput.place(x=775, y=375)

perimeterOutputLabel = tk.Label(main_window, text='Perimeter')
perimeterOutputLabel.place(x=775, y=450)

perimeterOutput = tk.Label(main_window, text='N/A')
perimeterOutput.place(x=775, y=475)






# Labels and entries for user input
oppositeEntryLabel = tk.Label(main_window, text='Opposite Length (Leave Empty if Unknown)', anchor='center')
oppositeEntryLabel.place(x=screenHeight/2, y=350)

oppositeEntry = tk.Entry(main_window)
oppositeEntry.place(x=screenHeight/2, y=375)


adjacentEntryLabel = tk.Label(main_window, text='Adjacent Length (Leave Empty if Unknown)', anchor='center')
adjacentEntryLabel.place(x=screenHeight/2, y=400)

adjacentEntry = tk.Entry(main_window)
adjacentEntry.place(x=screenHeight/2, y=425)


hypotenuseEntryLabel = tk.Label(main_window, text='Hypotenuse Length (Leave Empty if Unknown)', anchor='center')
hypotenuseEntryLabel.place(x=screenHeight/2, y=450)

hypotenuseEntry = tk.Entry(main_window)
hypotenuseEntry.place(x=screenHeight/2, y=475)




# Creating the canvas
canvasWidth = 500
canvasHeight = 300

canvas = ZoomableCanvas(main_window, bg='#e6e6e6', width=canvasWidth, height=canvasHeight)
canvas.place(x=screenHeight/2, y=0)





# Function for creating the triangle
def scale_triangle():

    # Deleting the previous triangle
    canvas.delete("triangle")

    # Retrieving entry data and creating variable for each side
    oppositeEntryData = oppositeEntry.get()
    adjacentEntryData = adjacentEntry.get()
    hypotenuseEntryData = hypotenuseEntry.get()

    # Converting data to integer and calculating the missing side
    if oppositeEntryData:
     oppositeEntryData = int(oppositeEntryData)
    else:
      oppositeEntryData = math.sqrt(int(hypotenuseEntryData)**2 - int(adjacentEntryData)**2) 
    if adjacentEntryData:
     adjacentEntryData = int(adjacentEntryData)
    else:
      adjacentEntryData = math.sqrt(int(hypotenuseEntryData)**2 - int(oppositeEntryData)**2) 
    if hypotenuseEntryData:
      hypotenuseEntryData = int(hypotenuseEntryData)
    else:
      hypotenuseEntryData = math.sqrt(int(adjacentEntryData)**2 + int(oppositeEntryData)**2)
    
    # Angle of elevation
    angleOfElevation = (numpy.arcsin([oppositeEntryData/hypotenuseEntryData]))* 180/numpy.pi

    x1, y1 = canvasWidth/2, canvasHeight/2
    x2, y2 = x1, y1 - oppositeEntryData
    x3, y3 = x1 + adjacentEntryData, y1


    
  


    # Creating the triangle
    canvas.create_polygon(x1, y1, x2, y2, x3, y3, fill='black', tags='triangle')
    bbox = canvas.bbox("triangle")
    z1, z2, w1, w2, = bbox
    cx, cy = (z1 +z2)/2, (w1 + w2)/2
    canvas.scale("triangle", cx, cy,  100/oppositeEntryData, 100/adjacentEntryData)
    bbox = canvas.bbox("triangle")
    z1, z2, w1, w2, = bbox
    cx, cy = (z1 +z2)/2, (w1 + w2)
    canvas.moveto("triangle", canvasWidth/2, canvasHeight/2)
       

     
     

    # Rounding the data alues
    hypotenuseEntryData = round(float(hypotenuseEntryData), 2)
    adjacentEntryData = round(float(adjacentEntryData), 2)
    oppositeEntryData = round(float(oppositeEntryData), 2)
    angleOfElevation = round(float(angleOfElevation), 2)
    triangleArea = round(((oppositeEntryData * adjacentEntryData)/2), 2)
    trianglePerimeter = (round((oppositeEntryData + adjacentEntryData + hypotenuseEntryData), 2))
    # Print the properties of the triangle
    print(f'\
          Hypotenuse length: {hypotenuseEntryData}\n\
          Adjacent length: {adjacentEntryData}\n\
          Opposite length: {oppositeEntryData}\n\
          Angle of Elevation: {angleOfElevation} degrees\n\
          Area: {triangleArea}\n\
          Perimeter: {trianglePerimeter}\n')
    
    # Display the properties of the triangle
    hypotenuseOutput.config(text=f'{hypotenuseEntryData}')
    adjacentOutput.config(text=f'{adjacentEntryData}')
    oppositeOutput.config(text=f'{oppositeEntryData}')
    angleOfElevationOutput.config(text=f'{angleOfElevation} degrees')
    perimeterOutput.config(text=f'{trianglePerimeter}')
    areaOutput.config(text=f'{triangleArea}')
    


# Corresponding button for scale_triangle function
button = tk.Button(main_window, text='Scale Triangle', command=scale_triangle)
button.place(x=screenHeight//2, y=500)

main_window.mainloop()