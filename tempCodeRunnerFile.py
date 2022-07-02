        square = [x, y, pygame.Rect(
                        self.squareSize * y, 
                        self.squareSize * x,
                        self.squareSize, 
                        self.squareSize 
                    )]
        self.add_a_chess(self.botPiece, square, BOT)