#Made by Catalin Chirita
#For FLAT Project 3
#2020
import os,sys
import itertools
from itertools import product
from prettytable import PrettyTable
import pygraphviz as pgv
from IPython.display import Image, display
import re
from PIL import Image

class DFA:
    c_state = None;
    def __init__(self, states, alphabet, transition_func, s_state, a_states):
        self.states = states;
        self.alphabet = alphabet;
        self.transition_func = transition_func;
        self.s_state = s_state; #Start State
        self.a_states = a_states; # Accept State
        self.c_state = s_state; # Current State
        return;
    def transition_state_input(self, input_value): # Transition to state with input
        if ((self.c_state, input_value) not in self.transition_func.keys()):
            self.c_state = None;
            return;
        self.c_state = self.transition_func[(self.c_state, input_value)];
        return;

    def in_accept_state(self,a_states):
        return self.c_state in a_states;

    def dfa_check(self, input_list,a_states):
        self.c_state = self.s_state;
        for inp in input_list:
            self.transition_state_input(inp);
            continue;
        return self.in_accept_state(a_states);
    pass;

class processing:
    def preprocess_data(self,data):
        data = data.split(';')
        data_arr = list()
        for word in data:
            word_to = ""
            i=0
            while i < len(word):
                if word[i] == '\n' or word[i] == '\t' or word[i] == ' ':
                    i = i + 1
                elif word[i] == '#':
                    i = i + 1
                    while word[i] != '\n':
                        i = i + 1
                else:
                    word_to = word_to + word[i]
                    i = i + 1
            data_arr.append(word_to)
        return self.process_data(data_arr)
    def process_data(self,data_arr):
        operation = operations()
        for word in data_arr:
            if '->' in word:
                process = word.split('->')
                if(process[0] == 'states'):
                    states = self.check_data(process[1],process[0])
                elif(process[0] == 'alphabet'):
                    alphabet = self.check_data(process[1],process[0])
                elif(process[0] == 'a_states'):
                    a_states = self.check_data(process[1],process[0])
                elif(process[0] == 's_state'):
                    s_state = self.check_data(process[1],process[0])
                elif(process[0] == 'transition'):
                    transition = self.check_data(process[1],process[0])
                else:
                    operation.error_msg("illegal DFA tuple declaration: %s"%process[0])
            else:
                pass
        return states,alphabet,a_states,s_state,transition
    def check_data(self,data,type):
        data_arr = list()
        operation = operations()
        if(type == "states" or type == "a_states"):
            data = data.split(',')
            if len(data) > 4:
                operation.error_msg("number of states must be less than 5 ")
            for token in data:
                if re.match('^[0-9]',token):
                    data_arr.append(int(token))
                else:
                    operation.error_msg("%s must be an integer"%type)
        elif(type == "s_state"):
            data_arr = int(data)
        elif(type == "alphabet"):
            data = data.split(',')
            for token in data:
                if re.match('^[A-Z,a-z]',token):
                    data_arr.append(str(token))
                else:
                    operation.error_msg("%s must be an alphabet"%type)
        elif(type == "transition"):
            data_arr = dict()
            data = data.split(':')
            data_list = list()
            for transition in data:
                transition_list = list()
                transition = transition.split(',')
                for transition_data in transition:
                    transition_data = transition_data.split('=')
                    transition_data_list= list()
                    for transition_data_value_name in transition_data:
                        transition_data_value_name_map = map(str,transition_data_value_name)
                        array_token_list = ""
                        if '{' in transition_data_value_name_map or '}' in transition_data_value_name_map:
                            array_token = ""
                            for transition_data_value_name_array in transition_data_value_name_map:
                                if(transition_data_value_name_array == '{' or transition_data_value_name_array == '}'):
                                    pass
                                else:
                                    array_token = array_token + transition_data_value_name_array
                            array_token_list = array_token_list + array_token
                        else:
                            array_token_list =array_token_list + transition_data_value_name
                        transition_data_list.append(array_token_list)
                    transition_list.append(transition_data_list)
                data_list.append(transition_list)
            for word in data_list:
                initial = word[0][1]
                value = word[1][1]
                target = word[2][1]
                data_arr[(int(initial),value)] = int(target);

        return data_arr

class operations:
    def lang_generate(self,size,input_word): # Languige genetation
        array_of_language = list()
        for word in itertools.product(input_word,repeat = size):
            generated = ''.join(word)
            array_of_language.append(generated)
        return array_of_language
    def concatenate_list(self,list):
        result= ''
        for element in list:
            result += str(element)
        return result
    def gs(self,arr,pos):
        for i in range(pos,len(arr)):
            if(i+1 != len(arr)):
                if(arr[i+1] == '*'):
                    return 1
                else:
                    return 0
            else:
                break
    def DFA_to_REGEX(self,transition):
        concat = ""
        for word in sorted(transition.iterkeys()):
            target = transition.get(word)
            initial = word[0]
            value = word[1]
            if(target == initial):
                concat = concat + value+"*"
            else:
                concat = concat + value
        return concat
    def error_msg(self,msg):
        print("\n\n%s"%msg)
        sys.exit()
    def print_table(self,approved,denied):
        table = PrettyTable()
        table.field_names = ['accepted', 'rejected']
        for i in approved:
            table.add_row([i,' '])
        for i in denied:
            table.add_row([' ',i])
        print(table)
    def clear(self):
        os.system('cls||clear')
        print(' ----------------------------------------------')
        print('|     DETERMINISTIC FINITE AUTOMATA (DFA)      |')
        print('|       (generator, checker, converter)        |')
        print('|                                              |')
        print('| DFA DATA: data.txt                           |')
        print(' ----------------------------------------------')
    def print_transition(self,states,alphabet,transition):
        table = PrettyTable()
        header = states
        header = ['Values']+header
        table.field_names = header
        print("Transition Table")
        for i in transition:
            for state in states:
                if(transition.get(i) == state):
                    num_of_index = len(states)
                    if(states.index(state) == 0):
                        for j in alphabet:
                            if(i[1] == j):
                                table.add_row([j, i[0],'','',''])
                    elif(states.index(state) == 1):
                        for j in alphabet:
                            if(i[1] == j):
                                table.add_row([j, '',i[0],'',''])
                    elif(states.index(state) == 2):
                        for j in alphabet:
                            if(i[1] == j):
                                table.add_row([j, '','',i[0],''])
                    elif(states.index(state) == 3):
                        for j in alphabet:
                            if(i[1] == j):
                                table.add_row([j, '','','',i[0]])
        print(table)
    def print_DFA_diagram(self,transition):
        G=pgv.AGraph()
        G=pgv.AGraph(strict=False,directed=True)

        to_append = 'digraph G {size="4,4"; '
        for i in transition:
            target = transition.get(i)
            initial = i[0]
            value = i[1]
            to_append = to_append + '%s -> %s [label="%s"];'%(initial,target,value)
        to_append = to_append + 'rankdir=LR'
        to_append = to_append + '}'
        A=pgv.AGraph(to_append)
        A.layout()
        A.layout(prog='dot')
        A.draw('dfa.png')
        a = Image.open('dfa.png')
        a.show()
    def tokenize(self,arr):
        tokenize = map(str,arr)
        tokenize_all = ''
        for word in tokenize:
            if re.match('^[a-z,A-Z]',word):
                tokenize_all = tokenize_all + "(String,%s) "%word
            elif re.match('^[1-9]',word):
                tokenize_all = tokenize_all + "(Integer,%s) "%word
            elif word == '+':
                tokenize_all = tokenize_all + "(Plus,%s) "%word
            elif word == '*':
                tokenize_all = tokenize_all + "(Epsilon,%s) "%word
            elif word == '(' or word == ')':
                tokenize_all = tokenize_all + "(parenthesis,'%s') "%word
            else:
                self.error_msg("Error in parsing: illegal character: %s "%word)
        print(tokenize_all)
        stop = raw_input("Press any key to continue...(except poweroff!)")
    def print_DFA_diagram_language(self,prio,less_prio,title):
        G=pgv.AGraph()
        G=pgv.AGraph(strict=False,directed=True)
        initial = 0
        target = 1
        to_append = 'digraph G {size="4,4"; label="%s";'%title
        prio = prio.split('(')
        for expression in prio:
            if expression == '':
                pass
            else:
                if '+' in expression:
                    arr = expression.split('+')
                    for i in range(0,len(arr)):
                        arr[i] = map(str,arr[i])
                    i = 0
                    indi = 0
                    start_f = list()
                    while i < len(arr):
                        j = 0
                        start = initial
                        while j < len(arr[i]):
                            if(self.gs(arr[i],j) == 1 and re.match('^[a-z,A-Z]',arr[i][j])):
                                to_append = to_append + '%s -> %s [label="%s"];'%(start,start,arr[i][j])
                                j+=2
                            elif(self.gs(arr[i],j) == 1 and arr[i][j]== ')'):
                                to_append = to_append + '%s -> %s;'%(start,target)
                                k=0
                                while k < len(start_f):
                                    to_append = to_append + '%s -> %s;'%(start_f[k],target)
                                    k+=1
                                to_append = to_append + '%s -> %s;'%(target,initial)
                                to_append = to_append + '%s -> %s;'%(initial,target)
                                j+=2
                            elif( arr[i][j] == ')'):
                                to_append = to_append + '%s -> %s;'%(start,target)
                                k=0
                                while k < len(start_f):
                                    to_append = to_append + '%s -> %s;'%(start_f[k],target)
                                    k+=1
                                to_append = to_append + '%s -> %s;'%(target,initial)
                                j+=1

                            else:
                                to_append = to_append + '%s -> %s [label="%s"];'%(start,target,arr[i][j])
                                start = start + 1
                                target = target+1
                                j+=1
                            if(indi > 0):
                                start = target - 1

                        start_f.append(start)
                        start = initial
                        indi = 1
                        i+=1
                    initial = target
                    target = target + 1
                elif ')*' in expression:
                    arr = map(str,expression)
                    i = 0
                    start_in = initial
                    while i < len(arr):
                        if(self.gs(arr,i) == 1 and re.match('^[a-z,A-Z]',arr[i])):
                            to_append = to_append + '%s -> %s [label="%s"];'%(initial,initial,arr[i])
                            i+=2
                        else:
                            if(arr[i] == ')' and arr[i+1] == '*'):
                                to_append = to_append + '%s -> %s;'%(initial,start_in)
                                to_append = to_append + '%s -> %s;'%(start_in,initial)
                                i+=2
                            else:
                                to_append = to_append + '%s -> %s [label="%s"];'%(initial,target,arr[i])
                                initial = initial + 1
                                target = target+1
                                i+=1

                else:
                    arr = map(str,expression)
                    i = 0
                    while i < len(arr):
                        if(self.gs(arr,i) == 1):
                            to_append = to_append + '%s -> %s [label="%s"];'%(initial,initial,arr[i])
                            i+=2
                        else:
                            if(arr[i] == ')'):
                                i+=1
                                pass
                            else:
                                to_append = to_append + '%s -> %s [label="%s"];'%(initial,target,arr[i])
                                initial = initial + 1
                                target = target+1
                                i+=1

        less_prio = less_prio.split('(')
        for expression in less_prio:
            if expression == '':
                pass
            else:
                if '+' in expression:
                    arr = expression.split('+')
                    for i in range(0,len(arr)):
                        arr[i] = map(str,arr[i])
                    i = 0
                    indi = 0
                    start_f = list()
                    while i < len(arr):
                        j = 0
                        start = initial
                        while j < len(arr[i]):
                            if(self.gs(arr[i],j) == 1 and re.match('^[a-z,A-Z]',arr[i][j])):
                                to_append = to_append + '%s -> %s [label="%s"];'%(start,start,arr[i][j])
                                j+=2
                            else:
                                to_append = to_append + '%s -> %s [label="%s"];'%(start,target,arr[i][j])
                                start = start + 1
                                target = target+1
                                j+=1
                            if(indi > 0):
                                start = target - 1
                        if (i+1 == len(arr) ):
                            to_append = to_append + '%s -> %s;'%(start,target)
                            k=0
                            while k < len(start_f):
                                to_append = to_append + '%s -> %s;'%(start_f[k],target)
                                k+=1
                        start_f.append(start)
                        start = initial
                        indi = 1
                        i+=1
                    initial = target
                    target = target + 1
                else:
                    arr = map(str,expression)
                    i = 0
                    while i < len(arr):
                        if(self.gs(arr,i) == 1):
                            to_append = to_append + '%s -> %s [label="%s"];'%(initial,initial,arr[i])
                            i+=2
                        else:
                            to_append = to_append + '%s -> %s [label="%s"];'%(initial,target,arr[i])
                            initial = initial + 1
                            target = target+1
                            i+=1

        to_append = to_append + 'rankdir=LR{ %s [shape=doublecircle]'%initial
        to_append = to_append + '}'
        to_append = to_append + '}'
        A=pgv.AGraph(to_append)
        A.layout()
        A.layout(prog='dot')
        A.draw('dfa-language.png')
        a = Image.open('dfa-language.png')
        a.show()
    def process_regex(self,arr):
        self.tokenize(arr)
        arr_map = map(str,arr)
        i = 0
        priority = list()
        less_prio = list()
        paren = -1
        while i < len(arr_map):
            if arr_map[i] == '(':
                paren = 1
            elif arr_map[i] == ')':
                paren = 0
                priority.append(')')

            if paren == 1:
                priority.append(arr_map[i])
                i +=1
            elif re.match('^[a-z,A-Z,0-9]',arr_map[i]) or arr_map[i] == '+':
                if(self.gs(arr_map,i) == 1):
                    less_prio.append(arr_map[i]+'*')
                    i+=2
                else:
                    less_prio.append(arr_map[i])
                    i+=1
            elif arr_map[i] == '*' and arr_map[i-1] == ')':
                priority.append(arr_map[i])
                i+=1
            else:
                i+=1
        priority = self.concatenate_list(priority)
        less_prio = self.concatenate_list(less_prio)
        self.print_DFA_diagram_language(priority,less_prio,arr)

    def main(self):
        self.clear()
        choice = 0
        while choice != '3':
            self.clear()
            choice = raw_input("Select Option \n\n1: Inialize DFA and check accepted and denied Languages;\n2: Convert Regular Expression to DFA diagram\n3: exit program\n\n: ")
            if(choice == '2'):
                regex = raw_input("Enter Language: ")
                self.process_regex(regex)
            elif(choice == '1'):
                get_input_user_class = processing();
                data = open("data.txt", "r")
                data = data.read()
                data = get_input_user_class.preprocess_data(data)
                states = data[0]
                alphabet = data[1]
                a_states = data[2]
                s_state = data[3]
                transition = data[4]
                self.print_DFA_diagram(transition)
                dfa = DFA(states, alphabet, transition, s_state, a_states);
                input_user_choice = '1'
                while input_user_choice != '3':
                    self.clear()
                    print('states: %s'%states)
                    print('alphabet: %s'%alphabet)
                    self.print_transition(states,alphabet,transition)
                    print('Start state: %s'%s_state)
                    print('Accept States: %s '%a_states)
                    print("Converted DFA to Regular Expression: %s \n\n"%self.DFA_to_REGEX(transition))
                    input_user_choice = raw_input("1 to generate random language\n2 for manual input \n3 go back\n\n: ")
                    if(input_user_choice == '1'):
                        input_user = raw_input("Enter Lenght of language to be generated: ");
                        string_alphabet = self.concatenate_list(alphabet)
                        number_to_generate = int(input_user)
                        generated_value = self.lang_generate(number_to_generate,string_alphabet)
                        accepted = list()
                        denied = list()
                        for i in generated_value:
                            if(dfa.dfa_check(i,a_states)):
                                accepted.append(i)
                            else:
                                denied.append(i)
                        self.print_table(accepted,denied)
                        stop = raw_input("Press any key to continue...(except poweroff!)")
                    elif(input_user_choice == '2'):
                        input_user = raw_input("Enter language: ");
                        accepted = list()
                        denied = list()
                        if(dfa.dfa_check(input_user,a_states)):
                            accepted.append(input_user)
                        else:
                            denied.append(input_user)
                        self.print_table(accepted,denied)
                        stop = raw_input("Press any key to continue...(except poweroff!)")
operation = operations();
try:
    operation.main()
except:
    print("There was an error in running the program.\n")