import cv2
import pandas as pd

# Paths to images and csv file
img_paths = ['pic1.jpg', 'pic2.jpg', 'pic3.jpg']
csv_path = 'colors.csv'

# Reading csv file
index = ['color', 'color_name', 'hex', 'R', 'G', 'B']
df = pd.read_csv(csv_path, names=index, header=None)

# Declaring global variables
clicked = False
r = g = b = xpos = ypos = 0

# Function to calculate minimum distance from all colors and get the most matching color
def get_color_name(R, G, B):
    minimum = 1000
    cname = ''
    for i in range(len(df)):
        d = abs(R - int(df.loc[i, 'R'])) + abs(G - int(df.loc[i, 'G'])) + abs(B - int(df.loc[i, 'B']))
        if d <= minimum:
            minimum = d
            cname = df.loc[i, 'color_name']
    return cname

# Function to get x, y coordinates of mouse double click
def draw_function(event, x, y, flags, params):
    global b, g, r, xpos, ypos, clicked
    if event == cv2.EVENT_LBUTTONDBLCLK:
        clicked = True
        xpos = x
        ypos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)

def process_image(img_path):
    global img, clicked
    clicked = False

    # Reading and resizing image
    img = cv2.imread(img_path)
    img = cv2.resize(img, (800, 600))

    # Creating window
    window_name = img_path.split('/')[-1]
    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, draw_function)

    while True:
        cv2.imshow(window_name, img)
        if clicked:
            # Drawing rectangle and text
            cv2.rectangle(img, (20, 20), (600, 60), (b, g, r), -1)
            text = get_color_name(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)
            cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

            # For very light colors display text in black
            if r + g + b >= 600:
                cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

        if cv2.waitKey(20) & 0xFF == 27:
            break

    cv2.destroyAllWindows()

# Process each image
for img_path in img_paths:
    process_image(img_path)
