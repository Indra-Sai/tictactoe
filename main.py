import socket
import threading

class TICTACTOE : 
    
    def __init__(self):
        self.board=[[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]
        self.turn='X'
        self.you= 'X' # game hosting man
        self.opponent = 'O' # joined person
        self.winner=None
        self.game_over=False
        self.counter=0
        
    def host_game(self,host,port):
        server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server.bind((host,port))
        server.listen(True)
        
        client,add= server.accept()
        self.you= 'X' 
        self.opponent = 'O'
        threading.Thread(target=self.handle_connection, args=(client,)).start()
        server.close()
        
    def connect_to_game(self,host, port):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host,port))
        self.you= 'O' 
        self.opponent = 'X' 
        threading.Thread(target=self.handle_connection, args=(client,)).start()
        
    def handle_connection(self, client):
        while not self.game_over:
            if self.turn==self.you:
                move=input("Enter a move row,col :").strip()
                if self.check_valid_move(move.split(',')):
                    self.apply_move(move.split(','),self.you)
                    self.turn=self.opponent
                    self.get_result()
                    client.send(move.encode('utf-8'))
                    
                else:
                    print('Invalid move!')
            else:
                data=client.recv(1024)
                if not data:
                    break
                else:
                    self.apply_move(data.decode('utf-8').split(','),self.opponent)
                    self.get_result()
                    self.turn = self.you
        client.close()   
         
    def get_result(self):
        if self.check_if_won():
            if self.winner==self.you:
                print("You Won !")
                # exit()
                return
            elif self.winner==self.opponent:
                print('You lose !')
                # exit()
                return
        else:
            if self.counter==9 :
                print('It is a tie !')
                # exit()
                return
                
    def apply_move(self, move, player):
        if self.game_over:
            return
        self.counter+=1
        self.board[int(move[0])][int(move[1])] = player
        self.print_board()
        
    
    def check_valid_move(self, move):
        x,y=map(int,move)
        return x<3 and y<3 and self.board[x][y]==' '
    
    def check_if_won(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != ' ':
                self.winner = self.board[i][0]
                self.game_over=True
                return True
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != ' ':
                self.winner = self.board[0][i]
                self.game_over=True
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            self.winner = self.board[1][1]
            self.game_over=True
            return True
        if self.board[2][0] == self.board[1][1] == self.board[0][2] != ' ':
            self.winner = self.board[1][1]
            self.game_over=True
            return True
        return False
    
    def print_board(self):
        for row in range(3):
            print(" | ".join(self.board[row]))
            if row != 2:
                print("-"*9)
        print("\n\n")