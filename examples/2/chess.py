import cv2
import numpy as np

def generate_chessboard(num_cells, cell_side_length):
    total_size = num_cells * cell_side_length

    # Create a white background
    chessboard = 255 * np.ones((total_size, total_size), dtype=np.uint8)

    for i in range(num_cells):
        for j in range(num_cells):
            # Calculate the starting point of each cell
            x = j * cell_side_length
            y = i * cell_side_length

            # Draw a black or white square based on the cell indices
            if (i + j) % 2 == 0:
                cv2.rectangle(chessboard, (x, y), (x + cell_side_length, y + cell_side_length), 0, thickness=-1)

    return chessboard

# Get user input for the number of cells and cell side length
num_cells = int(input("Enter the number of cells per row and column: "))
cell_side_length = int(input("Enter the side length of each cell: "))

# Generate chessboard
chessboard = generate_chessboard(num_cells, cell_side_length)

# Display the chessboard
cv2.imshow('Chessboard', chessboard)
cv2.waitKey(0)
cv2.destroyAllWindows()
