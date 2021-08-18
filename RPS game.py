rock = '''
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
'''

paper = '''
    _______
---'   ____)____
          ______)
          _______)
         _______)
---.__________)
'''

scissors = '''
    _______
---'   ____)____
          ______)
       __________)
      (____) 
---.__(___)
'''
import random
li=[rock,paper,scissors]
choice=int(input("What do you choose?Type 0 for rock,1 for Paper,2 for Scissor\n"))
print("Your Choice")
print(li[choice])
computer_choice=random.randint(0,2)
print("Computer's Choice")
print(li[computer_choice])
if(choice-computer_choice==1 or (choice==0 and computer_choice==2)):
  print("User Won")
elif(choice==computer_choice):
  print("Tie")
else:
  print("Computer Won")
