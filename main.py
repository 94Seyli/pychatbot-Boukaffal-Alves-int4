# 16/12 23h
from function3 import *

if __name__ == "__main__":

    # Call of the function
    directory = "./speeches-20231123"
    files_names = list_of_files(directory, "txt")

    last_list = new_list(files_names)
    last_column_list = sorted(last_list)
    president_list = del_duplicates(last_list)

    cleaned(files_names)

    word_collection = {}
    directory_cleaned = "./cleaned"
    word_collection = cpt_word(directory_cleaned)

    files_into_speeches = [f for f in os.listdir('./speeches-20231123') if f.endswith('.txt')]

    # Calling cleaning function
    cleaned(files_into_speeches)

    coll_IDF = IDF_score_coll(directory_cleaned)

    Matrix = TFIDF_matrix(directory_cleaned)

    # To display the Matrix
    for i in range(len(Matrix)):
        print(Matrix[i])

    word_not_important = []
    for j in range(1, len(Matrix)):
        TF_IDF = Matrix[j][1]
        if TF_IDF == 0:
            sum_TF_IDF = 0
            for k in range(2, 9):
                sum_TF_IDF = sum_TF_IDF + Matrix[j][k]
            if sum_TF_IDF == 0:
                word_not_important.append(Matrix[j][0])

    # Initialise variables to store the word with the highest score
    highest_score = 0
    word_import_folder = ""

    # Iteration on each row and column of the Matrix (ignoring the first row and column)
    for i in range(1, len(Matrix)):
        for j in range(1, len(Matrix[i])):
            if Matrix[i][j] > highest_score:
                highest_score = Matrix[i][j]
                word_import_folder = Matrix[i][0]

    # Initialise variables to store the word with the highest score
    highest_score = 0
    word_import_chirac = ""

    # Iteration on each row and column of the Matrix (ignoring the first row and column)
    for i in range(1, len(Matrix)):
        for j in range(1, 3):
            if Matrix[i][j] > highest_score:
                highest_score = Matrix[i][j]
                word_import_chirac = Matrix[i][0]

    president_nation = []
    index_word_nation = 0
    for i in range(len(Matrix)):
        if Matrix[i][0] == "nation":
            index_word_nation = i
    find_Chirac = False
    find_Mitterrand = False
    for i in range(2, 9):
        if Matrix[index_word_nation][i] > 0:
            if i == 1 or i == 2 and find_Chirac == False:
                find_Chirac = True
                president_nation.append("Chirac")
            if i == 3:
                president_nation.append("Giscard")
            if i == 4:
                president_nation.append("Hollande")
            if i == 5:
                president_nation.append("Macron")
            if i == 6 or i == 7 and find_Mitterrand == False:
                find_Mitterrand = True
                president_nation.append("Mitterrand")
            if i == 8:
                president_nation.append("Sarkozy")

    index_high_IDF = 0
    for i in range(2, 8):
        if Matrix[index_word_nation][i] < Matrix[index_word_nation][i + 1]:
            index_high_IDF = i + 1
        else:
            index_high_IDF = i

    if index_high_IDF == 1 or index_high_IDF == 2:
        presi_nation = "Chirac"
    if index_high_IDF == 3:
        presi_nation = "Giscard"
    if index_high_IDF == 4:
        presi_nation = "Hollande"
    if index_high_IDF == 5:
        presi_nation = "Macron"
    if index_high_IDF == 6 or index_high_IDF == 7:
        presi_nation = "Mitterrand"
    if index_high_IDF == 8:
        presi_nation = "Sarkozy"

    word_without_not_import = []
    for i in range(1, len(Matrix)):
        if Matrix[i][0] not in word_not_important:
            word_without_not_import.append(Matrix[i][0])

    ecolo_index = 0
    for i in range(len(Matrix)):
        if Matrix[i][0] == "climat":
            ecolo_index = i
            break

    # Find the highest score for 'climate'.
    score_max = 0
    ecolo_index_president = 0
    for j in range(1, len(Matrix[ecolo_index])):
        if Matrix[ecolo_index][j] > score_max:
            score_max = Matrix[ecolo_index][j]
            ecolo_index_president = j

    president_ecolo = ""
    if ecolo_index_president == 1 or ecolo_index_president == 2:
        president_ecolo = "Chirac"
    if ecolo_index_president == 3:
        president_ecolo = "Giscard"
    if ecolo_index_president == 4:
        president_ecolo = "Hollande"
    if ecolo_index_president == 5:
        president_ecolo = "Macron"
    if ecolo_index_president == 6 or ecolo_index_president == 7:
        president_ecolo = "Mitterrand"
    if ecolo_index_president == 8:
        president_ecolo = "Sarkozy"

    # Main menu loop
    flag = True
    while flag:
        print("\n--- Menu ---\n\n"
              "- To display the least important words, enter 1\n"
              "- To display the most important words, enter 2\n"
              "- To display the most important word by Chirac, enter 3\n"
              "- To display the presidents who talk about the Nation, as well as the one who talks about it the most, enter 4\n"
              "- To display the president who speaks most about ecology, enter 5\n"
              "- Sorry, this command is not available at the moment : (To access the bot, enter 0.)\n")
        value_menu = saisie()  # Saisie d'un caractère (nombre de 0 à 5)
        if value_menu == 1:
            print("\n- Voici les mots les moins importants\n")
            for i in range(len(word_not_important)):
                print(word_not_important[i])
        elif value_menu == 2:
            print("\n- Voici le mot le plus important du dossier :\n", word_import_folder)
        elif value_menu == 3:
            print("\n- Voici le mot le plus important des discours de Chirac : ", word_import_chirac)
        elif value_menu == 4:
            print("\n- Voici les présidents parlant de Nation\n")
            for i in range(len(president_nation)):
                print(president_nation[i])
            print("\n-", presi_nation, "parle le plus de Nation")
        elif value_menu == 5:
            print("\n-", president_ecolo, "est le président qui parle le plus du climat\n")
        elif value_menu == 0:
            flag = False
        else:
            print("Choix incorrect, retour au menu")
