import sys
from PIL import Image, ImageOps, ImageDraw


def main():
    if len(sys.argv) < 2:
        print("Usage: python DiceToImage.py <Image_File_Location> [-n <Dice_Size> optional. might now work if set less than 10]")
        return

    fileAddress = sys.argv[1]
    optional_integer = None

    if "-n" in sys.argv:
        index = sys.argv.index("-n")
        if index + 1 < len(sys.argv):
            try:
                optional_integer = int(sys.argv[index + 1])
            except ValueError:
                print("Optional integer should be an integer.")
                return

    if not fileAddress:
        print("Please provide a name as the first argument.")
    else:
        diceTheImage(fileAddress, optional_integer)
        
    
    if optional_integer is not None:
        print("Optional integer:", optional_integer)



def diceTheImage(path, ds=10):
    img = Image.open(rf"{path}")
    height = 1080
    width = int(height / img.height * img.width)
    img = img.resize((width, height))
    img = ImageOps.grayscale(img)
    img = ImageOps.equalize(img)


    diceSize = ds  # Given dice size
    img_width = 1100  # Given image width

    # Calculate the maximum number of dice that can fit in a row
    dicesInaRow = int(img_width / diceSize)



    newImage = Image.new("L", (img.width, img.height), "white")
    newDraw = ImageDraw.Draw(newImage)

    # Create a dictionary to count the occurrences of each dice value
    dice_count = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}

    for column in range(0, img.height - diceSize, diceSize):
        for row in range(0, img.width - diceSize, diceSize):
            pixelSum = 0  # Initialize sum for the dice-sized block
            for diceHeight in range(0, diceSize):
                for diceWidth in range(0, diceSize):
                    pixelColor = img.getpixel((row + diceWidth, column + diceHeight))
                    pixelSum += pixelColor  # Add pixel value to the sum
            pixelColor = pixelSum // (diceSize ** 2)  # Calculate average pixel value
            newDraw.rectangle(xy=[(row, column), (row + diceSize, column + diceSize)], fill= "white")

            # Convert the pixel value to a dice value
            diceForThisPixel = int((pixelColor / 255) * 6)   #map a range of values from one scale to another
            if diceForThisPixel == 0:
                diceForThisPixel = 1
            print(diceForThisPixel, end=" ")
            
            # Update the dice count dictionary
            if 1 <= diceForThisPixel <= 6:
                dice_count[diceForThisPixel] += 1
            elif diceForThisPixel == 0:
                dice_count[1] += 1
            else:
                print(f"Invalid dice value: {diceForThisPixel}")
                
            # Draw the corresponding dice symbol or dots
            dot_size = diceSize // 10
            
            if diceForThisPixel == 6:  # Mapping: 6 -> 1
                dot_x = row + diceSize // 2
                dot_y = column + diceSize // 2
                newDraw.ellipse([(dot_x - dot_size, dot_y - dot_size), (dot_x + dot_size, dot_y + dot_size)], fill="black")
                
            elif diceForThisPixel == 5:  # Mapping: 5 -> 2
                dot_positions = [
                    (row + diceSize // 4, column + diceSize // 4),
                    (row + (3 * diceSize) // 4, column + (3 * diceSize) // 4)
                ]
                for dot_x, dot_y in dot_positions:
                    newDraw.ellipse([(dot_x - dot_size, dot_y - dot_size), (dot_x + dot_size, dot_y + dot_size)], fill="black")
                
            elif diceForThisPixel == 4:  # Mapping: 4 -> 3
                dot_positions = [
                    (row + diceSize // 4, column + diceSize // 4),
                    (row + diceSize // 2, column + diceSize // 2),
                    (row + (3 * diceSize) // 4, column + (3 * diceSize) // 4)
                ]
                for dot_x, dot_y in dot_positions:
                    newDraw.ellipse([(dot_x - dot_size, dot_y - dot_size), (dot_x + dot_size, dot_y + dot_size)], fill="black")
                
            elif diceForThisPixel == 3:  # Mapping: 3 -> 4
                dot_positions = [
                    (row + diceSize // 4, column + diceSize // 4),
                    (row + diceSize // 4, column + (3 * diceSize) // 4),
                    (row + (3 * diceSize) // 4, column + diceSize // 4),
                    (row + (3 * diceSize) // 4, column + (3 * diceSize) // 4)
                ]
                for dot_x, dot_y in dot_positions:
                    newDraw.ellipse([(dot_x - dot_size, dot_y - dot_size), (dot_x + dot_size, dot_y + dot_size)], fill="black")
                
            elif diceForThisPixel == 2:  # Mapping: 2 -> 5
                dot_positions = [
                    (row + diceSize // 4, column + diceSize // 4),
                    (row + diceSize // 4, column + (3 * diceSize) // 4),
                    (row + diceSize // 2, column + diceSize // 2),
                    (row + (3 * diceSize) // 4, column + diceSize // 4),
                    (row + (3 * diceSize) // 4, column + (3 * diceSize) // 4)
                ]
                for dot_x, dot_y in dot_positions:
                    newDraw.ellipse([(dot_x - dot_size, dot_y - dot_size), (dot_x + dot_size, dot_y + dot_size)], fill="black")
                
            elif diceForThisPixel == 1:  # Mapping: 1 -> 6
                dot_positions = [
                    (row + diceSize // 4, column + diceSize // 4),
                    (row + diceSize // 4, column + diceSize // 2),
                    (row + diceSize // 4, column + (3 * diceSize) // 4),
                    (row + (3 * diceSize) // 4, column + diceSize // 4),
                    (row + (3 * diceSize) // 4, column + diceSize // 2),
                    (row + (3 * diceSize) // 4, column + (3 * diceSize) // 4)
                ]
                for dot_x, dot_y in dot_positions:
                    newDraw.ellipse([(dot_x - dot_size, dot_y - dot_size), (dot_x + dot_size, dot_y + dot_size)], fill="black")

        print()

    newImage.show()
    # Print the total required dice for each number
    for value, count in dice_count.items():
        print(f"Number {value}: {count} dice")


if __name__ == "__main__":
    main()