# _________________________Modules_________________________#
import os
import random
import math

# _________________________Basic functions_________________________#
# function to run through the list of files with a given extension and in a given directory and return a list of names
def list_of_files(directory, extension):
    files_names = []
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            files_names.append(filename)
    return files_names


# function to associate first and last name of presidents
def associate_name_presidents(president_name):
    president_f_name = {
        "Giscard dEstaing": "Valéry",
        "Mitterand": "François",
        "Chirac": "Jacques",
        "Sarkozy": "Nicolas",
        "Hollande": "François",
        "Macron": "Emmanuel",
    }
    return president_f_name.get(president_name, " Unknow ")


# function which takes the list of files and extracts only the name of the presidents and stored them in a list
def new_list(l):
    list = []
    for i in range(len(l)):
        val = l[i][11:-4]  # removes the file format (-4th index) and "nomination_" (11th index)
        for j in range(len(val)):
            if val[j] == '1' or val[j] == '2':  # if there is a 1 or a 2 in the string
                val = val[:-1]  # removes them from the last position
        list.append(val)
    return list


# function for removing duplicates from a list and return the list without duplicates
def del_duplicates(l):
    l = list(set(l))  # set allows to delete automatically duplicates
    return l


# function to convert a text/string to lower cases and return the text in lower case
def lower_case(txt):
    txt = list(txt)
    for i in range(len(txt)):
        if ord(txt[i]) >= ord("A") and ord(txt[i]) <= ord("Z"):  # if a character is between ASCII code of A and Z
            txt[i] = chr(ord(txt[i]) + ord("a") - ord("A"))  # change upper case to lower case
    return "".join(txt)


# function that removes punctuation from a string
def punctuation_str(l):
    list_punctuation = ["!", "+", "#", ".", ",", "?", ";", ":", "(", ")", ":", "=", "`", '"']
    list_s_punctuation = ["'", "-"]
    list = []
    string = ""
    for i in range(len(l)):
        list.append(l[i])
        if list[i] in list_s_punctuation:
            list[i] = " "
        if list[i] in list_punctuation:
            list[i] = ""
        string = string + list[i]
    return string


# function to cleans files and adds them to cleaned depository
def cleaned(files_list):
    if os.path.exists("./cleaned"):  # if cleaned directory exist, delete it automatically
        for file in os.listdir("./cleaned"):
            path_file = os.path.join("./cleaned", file)
            os.remove(path_file)
        os.rmdir("./cleaned")

    os.mkdir('./cleaned/')  # Create Cleaned directory

    for file_name in files_list:
        path_in = os.path.join('./speeches-20231123', file_name)
        path_out = os.path.join('./cleaned', "cleaned_" + file_name)
        with open(path_in, "r", encoding="utf-8") as f:
            content = f.read()

        # Use punctuation and lower case functions
        cleaned_content = punctuation_str(lower_case(content))

        with open(path_out, 'w', encoding='utf-8') as p:
            p.write(cleaned_content)


# _______________________________TF-IDF_______________________________#

# function to scan line of string and return a collection with the words of strings
def scan_line(string):
    coll = {}
    word = ""
    string = string + " "

    for i in range(len(string)):
        if string[i] != " ":
            word = word + string[i]
        else:
            if word == "d" or word == "j" or word == "s" or word == "n":  # otherwise add an e after the letters d, j, s, n
                word = word + "e"
            if word == "c":  # if it's a c, add an ela
                word = word + "ela"
            if word == "l":  # if it's an l, there's a 50/50 chance that it's an a or an e
                a_or_e = random.randint(1, 2)
                if a_or_e == 1:
                    word = word + "e"
                else:
                    word = word + "a"
                if word in coll:  # if the content of the variable word is in the collection, add 1
                    coll[word] = coll[word] + 1
                else:
                    coll[word] = 1
            else:
                if word in coll:  # if the content of the variable word is in the collection, add 1
                    coll[word] = coll[word] + 1
                else:
                    coll[word] = 1
            word = ""
    return coll


# function to calcul iteration of word and put it in a collection
def cpt_word(directory):
    collection = {}
    text = ""
    name_list = list_of_files(directory, "txt")
    for i in range(len(name_list)):
        loc_file = "./" + str(directory) + "/" + name_list[i]
        with open(loc_file, "r") as f:
            line = f.readline()
            while line != "":
                line = line.replace("\n", "")
                text = text + line + " "
                line = f.readline()
        collection = scan_line(text)
    return collection


# function to compute the IDF score of a word and put it in a collection
def IDF_score_coll(directory):
    TF = {}
    coll = {}
    name_list = list_of_files(directory, "txt")
    for i in range(len(name_list)):
        loc_file = "/" + name_list[i]
        with open(directory + loc_file, 'r') as f:
            content_ = f.read()
            content_ = content_.replace("\n", " ")
            TF = scan_line(content_)
        for word in TF.keys():  # Browse keys to the TF collection, i.e. all the words in text
            if word not in coll.keys():
                coll[word] = 1  # If the word is not in the IDF collection, then value = 1
            else:
                coll[word] = coll[word] + 1  # If the word is in the IDF collection, then value = +1
    for word, count in coll.items():
        coll[word] = float(math.log((len(name_list) / count), 10))  # Formula of IDF score
    return coll


# function that takes a directory and returns TF-IDF matrix based on each queue
def TFIDF_matrix(directory):
    coll_TFIDF = {}
    coll_TF = {}
    List = []

    name_list = list_of_files(directory, "txt")
    name_list = sorted(name_list)
    List.append("word")

    coll_IDF = IDF_score_coll(directory)  # Calculation of the IDF score for each word in the directory
    all_word = cpt_word(directory)  # Counts the number of occurrences of each word in all the documents

    if "" in all_word:  # Deletes the empty key if there is one
        del all_word[""]

    matrix = []
    line_numb = int(len(name_list)) + 1  # number of lines in the matrix (number of words + 1 for titles)
    for l in range(len(all_word) + 1):  # Creates a matrix filled with zeros
        line = [0] * line_numb
        matrix.append(line)
    cpt = 1

    for word in all_word.keys():  # Fill the first column of the matrix with the words
        matrix[cpt][0] = word
        cpt += 1
    for i in range(len(name_list)):  # Loop over the queues to fill the matrix with TF-IDF values

        loc_file = "./" + str(directory) + "/" + name_list[i]  # Follows the path of the file
        with open(loc_file, "r") as f:
            lineTF = f.read()
            lineTF = lineTF.replace("\n", "")
            coll_TF = scan_line(lineTF)  # Calculation of TF-IDF values for each word in the file
            for words in coll_TF.keys():
                if words in coll_IDF:
                    coll_TFIDF[words] = coll_IDF[words] * coll_TF[words]
            coll_TF.clear()

            matrix[0][i + 1] = name_list[i]  # Filling the first line of the matrix with file names

            for h in range(len(matrix)):  # Filling the matrix with TF-IDF values

                for word in coll_TFIDF.keys():
                    if word == matrix[h][0]:
                        matrix[h][i + 1] = coll_TFIDF[word]
            coll_TFIDF.clear()
    return matrix


# ----------------------------------
'''
       Input function for a number between 0 and 9.

       No input arguments.

       Output:
       - value: int
           Numeric value between 0 and 9 (a single character entered).

       The function uses a loop to ensure correct and valid input.
       If the input contains more than one character, the function ignores the input and continues the loop.
       If the input is a number between 0 and 5, the function returns this value as an integer.
       '''


def saisie():
    flag = True
    entry = ""
    while flag:
        entry = input("Enter a number between 0 and 5 : ")
        if len(entry) > 1:
            break
        elif ord(entry) > 47 and ord(entry) < 54:  # Entry is a number between 0 and 9
            return int(entry)


def word_question(string):
    list = []
    word = ""
    string = string + " "
    for i in range(len(string)):
        if string[i] != " ":
            word = word + string[i]
        else:
            if word == "d" or word == "j" or word == "s" or word == "n":  # otherwise add an e after the letters d, j, s, n
                word = word + "e"
            if word == "c":  # if it's a c, add an ela
                word = word + "ela"
            if word == "l":  # if it's an l, there's a 50/50 chance that it's an a or an e
                a_or_e = random.randint(1, 2)
                if a_or_e == 1:
                    word = word + "e"
                else:
                    word = word + "a"
            if word not in list:  # if the content of the variable word is in the collection, add 1
                list.append(word)
            word = ""
    return list


def important_word(list, matrix):
    word_list = []
    for word in list:
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] == word:
                    word_list.append(word)
    return word_list


def cpt_word_question(coll):
    cpt_total = 0
    for number in coll.values():
        cpt_total = cpt_total + number
    return cpt_total


def matrix_filtre_matrix(coll, matrix, coll_IDF):
    matrix = []
    line_0 = [0, "Question"]
    matrix.append(line_0)
    for word in coll.keys():
        for i in range(len(matrix)):
            if matrix[i][0] == word:
                L = []
                TF_IDF = coll[word] * coll_IDF[word]
                L.append(word)
                L.append(TF_IDF)
                matrix.append(L)

        print(matrix)
    return matrix


def cross_word_question_corpus(matrix_corpus, matrix_question):
    matrix_dimension_M = []
    for h in range(len(matrix_question)):
        for i in range(len(matrix_corpus)):
            if matrix_question[h][0] == matrix_corpus[i][0]:
                matrix_dimension_M.append(matrix_corpus[i])

    return matrix_dimension_M


def file_clean_to_speach(file):
    file = file[8:]
    return file


def important_word_question(matrix_question):
    for i in range(1, len(matrix_question) - 1):
        if matrix_question[i][1] > matrix_question[i + 1][1]:
            index_i = i
        else:
            index_i = i + 1
    impactant_word = matrix_question[index_i][0]
    return impactant_word


# ______________________________Response-PART-II______________________________#
def display_less_important_words(word_not_important):
    set_word_not_important = ""
    for i in range(len(word_not_important)):
        set_word_not_important = set_word_not_important + word_not_important[i] + "\n"
    # Create a new top-level window
    dialog = tk.Toplevel()
    dialog.title("Words Less Importants")
    dialog.geometry("1000x300")  # Set your desired size

    # Create a scrolled text widget for displaying information
    txt = scrolledtext.ScrolledText(dialog, wrap=tk.WORD, width=40, height=10)
    txt.pack(padx=10, pady=10)

    # Inserting some text (replace this with your actual content)
    txt.insert(tk.INSERT, set_word_not_important)

    # Disable editing of the text
    txt.configure(state='disabled')

    # Button to close the dialog
    btn_close = tk.Button(dialog, text="Close", command=dialog.destroy)
    btn_close.pack(pady=10)


def display_most_important_words(word_import_folder):
    # Logic for displaying the most important words
    messagebox.showinfo("Here is the most important word in the directory :\n", word_import_folder)


# Variable globale pour stocker le text entré
question = ""


def display_most_important_words_Chirac(word_import_chirac):
    # Logic for displaying the most important words
    messagebox.showinfo("more important words", "more important words here :\n" + word_import_chirac)


# Variable globale pour stocker le text entré

def display_presi_nation(president_nation, presi_nation):
    string = ""
    for i in range(len(president_nation)):
        string = string + president_nation[i]
    # Logic for displaying the most important words
    messagebox.showinfo("Here are the presidents talking about Nation :\n", string, "\n-", presi_nation,
                        "speaks most of Nation")


# Variable globale pour stocker le text entré

def display_presi_ecolo(president_ecolo):
    # Logic for displaying the most important words
    messagebox.showinfo("Here's the president who talks most about ecology :\n", president_ecolo)
