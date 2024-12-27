from tkinter import Tk, Entry, Button, Label, StringVar

window = Tk()
window.geometry("800*300")
window.title("zulu_dictionary")

entry_text = Entry(window)
entry_text.pack()

result = StringVar()
result_label = Label(window, textvariable=result)
result_label.pack()

zulu_dictionary = {'wena': "you",
                   'noma': "or",
                   'lo': "the",
                   'kwadingeka': "had",
                   'kwenzinye': "some",
                   'kuyinto': "is",
                   'eyodwa': "one",
                   'kusuka': "from",
                   'thina': "we",
                   'futhi': "and",
                   'ezinye' "other"
                   'lokho': "what",
                   'ade': "have",
                   'igama': "word",
                   'it': "it",
                   'loba': "invite",
                   'le': "this",
                   'esishisayo': "hot",
                   'ukuphuma': "out",
                   'kodwana': "but",
                   }


def search(word):
    if word in zulu_dictionary.keys():
        result.set(zulu_dictionary[word])
        print(zulu_dictionary[word])
    else:
        result.set("Not found")

        search_btn = Button(window, text="search", command=lambda: search(entry_text.get()))
        search_btn.pack()
        window.mainloop()
