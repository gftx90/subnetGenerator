# Class for structuring questions

# Example of structure

class Question:
    def __init__(self, question, answer, tip):
        self.question = question
        self.answer = answer
        self.tip = tip
        
    def present_question(self):
        while True:
            guess = (input("{}:\n\t".format(self.question)))
            if guess == str(self.answer):
                print("\tCorrect!\n")
                break
            elif guess == "s":
                print("\t{}\n".format(self.tip))
                break
            else:
                print("\tguess again\n")
