import random
import re

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split('(\d+)', text) ]

def generate_up_series(stack):
    '''
    generate a new series from the stack.
    rules: at least 3 sequential cards with the same color, after 13 can be only 1 (13, 1, 2 is legal)
    '''
    found = False
    counter = 0
    while ((not found) and (counter < 50)):
        counter += 1
        chosen_card = random.randint(0,len(stack)-1)
        chosen_card = stack[chosen_card]
        #print chosen_card
        series = [chosen_card]
        number_of_cards = random.randint(3,6)
        for length in range(number_of_cards, 2, -1):
            for adding_card in range(1,length):
                direction = random.random()%2
                series.sort(key=natural_keys)
                speical = False
                if (series[0][1:] == "1") and (series[-1][1:] == "13"):#need another speical sorting :)
                    a = series.pop(0) #take out the 1
                    series.append(a)  #push it in the end
                    speical = True
                if (direction == True) and (speical == False):#up, not illegal when we have 13,1
                    highest_card = series[-1]
                    next_card = upper_card[0]+str((int(upper_card[1:])+1)%14)
                    if next_card[1:] == "0":
                        next_card=next_card[0]+"1"
                    if next_card in stack:
                        series.append(next_card)
                    else: #lets try count down
                        smallest_card = series[0]
                        next_card = smallest_card[0]+str((int(smallest_card[1:])-1)%14)
                        if (next_card[1:] == "0") and (len(series) < 2): #if series only has x1, else it is illegal
                            next_card=next_card[0]+"13"
                        if next_card in stack:
                            series.append(next_card)
                else: #down
                    smallest_card = series[0]
                    next_card = smallest_card[0]+str((int(smallest_card[1:])-1)%14)
                    if (next_card[1:] == "0") and (len(series) < 2): #if series only has x1, else it is illegal
                        next_card=next_card[0]+"13"
                    if next_card in stack:
                        series.append(next_card)
                    elif (speical == False): #lets try count up, not illegal when we have 13,1
                        highest_card = series[-1]
                        next_card = highest_card[0]+str((int(highest_card[1:])+1)%14)
                        if next_card[1:] == "0":
                            next_sp_card=next_card[0]+"1"
                        if next_card in stack:
                            series.append(next_card)
            #let's check if we found a series
            if len(series) == length:
                print series
                found = True
                break
        
    #update the stack
    if found == True:
        for i in series:
            stack.remove(i)
    else: #series not found really...
        series = []
    return series




def generate_pattern_series(stack):
    '''
    generate a new series from the stack.
    rules: 3 or 4 same cards with the different color (r2,r2,b2 is illegal)
    '''
    found = False
    counter = 0
    while ((not found) and (counter < 20)):
        counter += 1
        color_list = ['r','b','g','y']    
        chosen_card = random.randint(0,len(stack)-1)
        chosen_card = stack[chosen_card]
        series = [chosen_card]
        color = chosen_card[0]
        number = chosen_card[1:]       
        number_of_cards = random.randint(3,4)
        #for length in range(number_of_cards, 2, -1):
#        print color, color_list, chosen_card, length
        color_list.remove(color)
        random.shuffle(color_list)
        for adding_card in range(1,number_of_cards):#length):
            color_check = color_list.pop()
            if (color_check+number in stack):
                series.append(color_check+number)
            else:
                break
        if len(series) == number_of_cards:#length:
            print series
            found = True
        #    break
        
    #update the stack
    if found == True:
        for i in series:
            stack.remove(i)
    else: #series not found really...
        series = []
    return series




        
