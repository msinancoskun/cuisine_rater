from tkinter import *
import random


users = dict()
users_list_box = list()


def load_dataset():
    userprofile = dict()
    places = dict()
    places_cuisine = dict()

    # Loads data from userprofile and parses it to listbox.
    with open('userprofile.csv') as user_profile:
        i = 0
        for line in user_profile:
            if i == 0:  # This line skips the first 2 columns of the csv file.
                i += 1
            else:
                id_num, name = line.strip().split(";")
                listbox_user.insert(int(id_num[1:]), name)
                userprofile[id_num] = name
                listbox_user.clipboard_append(name)
                users_list_box.append(name)

    # Loads data from places.csv
    with open('places.csv') as places_csv:
        i = 0
        for line in places_csv:
            if i == 0:  # This line skips the first 2 columns of the csv file.
                i += 1
            else:
                id_num, name = line.strip().split(";")
                places[id_num] = name

    # Loads data from place_cuisine.csv
    with open('place_cuisine.csv') as places_cuisine_csv:
        i = 0
        for line in places_cuisine_csv:
            if i == 0:  # This line skips the first 2 columns of the csv file.
                i += 1
            else:
                id_num, name = line.strip().split(';')
                if id_num in places_cuisine.keys():
                    places_cuisine[id_num].append(name)
                else:
                    places_cuisine[id_num] = [name]

    with open('ratings.csv') as csv_file:
        i = 0
        for line in csv_file:
            if i == 0:  # This line skips the first 2 columns of the csv file.
                i += 1
            else:
                user_id, place_id, r_rating, food_rating, service_rating = line.strip().split(";")
                overall_cuisine_rating = (int(r_rating) * 1.4 + int(food_rating) * 2.5
                                          + int(service_rating) * 1.8 + random.randint(0.0, 1.0))
                #    * rank_of_the_cuisine_for_that_restaurant
                users.setdefault(userprofile[user_id], dict())
                if place_id in places_cuisine.keys():
                    value = 2.0
                    for cuisine in places_cuisine[place_id]:
                        users[userprofile[user_id]][cuisine] = overall_cuisine_rating * value
                        if len(places_cuisine[place_id]) == 1:
                            break
                        value -= value - (1 / (len(places_cuisine[place_id]) - 1))
                else:
                    users[userprofile[user_id]]['regular'] = overall_cuisine_rating * value

    # Calculate the similarity data and show in the box at the top.
    # similarity_data =
    # for key in similarity_data.keys():
    #     s = key + '\n'
    #     for item in similarity_data[key]:
    #         s += ' ' + item[1]
    #     s += '\n'
    #     text_load.insert(END, s)


root = Tk()
root.title("Cuisine Reccomendation System")
root.geometry('720x480-8-200')

# overall_cuisine_rating = (general_restaurant_rating * 1.4 + food_rating * 2,5 + service_rating * 1.8 +
# some_random_number_between_0.0_and_1.0) * rank_of_the_cuisine_for_that_restaurant

data_set_text = """After the datasets have been loaded, cuisine similarity data should be 
display here (at most 5 similar cuisines for each cuisine)."""

# TOP SECTION OF THE GRID SYSTEM
label_main = Label(root, text="Cuisine Reccomendation System")
label_main.grid(row=0, column=0, columnspan=3)

button_load = Button(root, text="Load Dataset Files", width=15, command=load_dataset)
button_load.grid(row=1, column=0)

scrollbar_load = Scrollbar()
text_load = Text(yscrollcommand=scrollbar_load.set, width=40, height=5)
text_load.grid(row=1, column=1, columnspan=2)
scrollbar_load.grid(row=1, column=3, sticky=W)
scrollbar_load.config(command=text_load.yview)


# Middle Section Settings
label_settings = Label(root, text="Settings")
label_settings.grid(row=2, column=0, columnspan=3)


# TOTAL NUMBER OF RECCOMENDATIONS PART OF THE GUI
label_recommendation = Label(root, text="Total Number of Reccomendations")
label_recommendation.grid(row=3, column=0)
number_of_reccomendation = IntVar()
number_of_reccomendation_entry = Entry(root, textvariable=number_of_reccomendation, width=3)
number_of_reccomendation_entry.grid(row=4, column=0)


# RECCOMENDATION MODEL PART OF THE GUI
label_recom_model = Label(root, text="Reccomendation Model")
label_recom_model.grid(row=3, column=1, padx=20)
reccomendation_model = IntVar()
radio_recom1 = Radiobutton(root, text="User-based", variable=label_recom_model, value=1)
radio_recom2 = Radiobutton(root, text="Item-based", variable=label_recom_model, value=2)
radio_recom1.grid(row=4, column=1)
radio_recom2.grid(row=5, column=1)


# SIMILARITY METRIC PART OF THE GUI
label_similarity_metric = Label(root, text="Similarity Metric")
label_similarity_metric.grid(row=3, column=2, padx=20)
similarity_metric = IntVar()
radio_button_metric1 = Radiobutton(root, text="Euclidian", variable=similarity_metric, value=1)
radio_button_metric2 = Radiobutton(root, text="Pearson", variable=similarity_metric, value=2)
radio_button_metric1.grid(row=4, column=2)
radio_button_metric2.grid(row=5, column=2)


# BOTTOM SECTION
# SELECT USER WIDGET
label_select = Label(root, text="Select A User")
label_select.grid(row=6, column=1, pady=10)
scrollbar_user = Scrollbar()
listbox_user = Listbox(yscrollcommand=scrollbar_user.set, width=30, height=5)
listbox_user.grid(row=7, column=1)
scrollbar_user.grid(row=7, column=2)


# LIST USERS WIDGET
button_user = Button(root, text="List Similar Users")
button_user.grid(row=8, column=0)
scrollbar_users = Scrollbar()
text_users = Text(yscrollcommand=scrollbar_users.set, width=20, height=5)
text_users.grid(row=9, column=0)
scrollbar_users.grid(row=9, column=1)
scrollbar_users.config(command=text_users.yview)


# GET CUISINE RECCOMENDATIONS WIDGET
button_recom = Button(root, text="Get Cuisine Reccomendations")
button_recom.grid(row=8, column=3)
scrollbar_recoms = Scrollbar()
text_recoms = Text(yscrollcommand=scrollbar_recoms.set, width=20, height=5)
text_recoms.grid(row=9, column=3)
scrollbar_recoms.grid(row=9, column=4)
scrollbar_recoms.config(command=text_recoms.yview)


if __name__ == '__main__':
    root.mainloop()
