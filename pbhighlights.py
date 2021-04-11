#!/usr/bin/python

import sqlite3

def gethighlightsfromdb(path="books.db"):
    conn = sqlite3.connect('books.db')

    rows = conn.execute( \
        "select Title, Authors, json_extract(Highlight, '$.text') as Text from Books \
            inner join (select OID as BookID, Highlight from Items \
                inner join (select ParentID, Highlight from Items \
                    inner join (select ItemID, Val as Highlight from Tags \
                        where TagID = 104 and Val <> '{\"text\":\"Bookmark\"}') as Highlights \
                    on Highlights.ItemID = OID) as Highlights \
                on Highlights.ParentID = OID) as Highlights \
            on BookID = OID;")

    books = {}
    for row in rows:
        title = row[0]
        authors = row[1]
        highlight = row[2]
        if not any (title in key for key in books.keys()):
            books.update({ title: { 'highlights': [], 'authors': authors } })
        books[row[0]]['highlights'].append("".join(highlight.rstrip().splitlines()))

    conn.close()
    return books

def printtoconsole(books):
    for book in books:
        print("Title:", book)
        print("Highlights:", len(books[book]['highlights']))
        for h in books[book]['highlights']:
            print("-", h)
        print("")

def writetofile(books, file="highlights.md"):
    f = open(file, "w")
    f.write("# Highlights from books\n\n")
    for book in books:
        f.write("## " + book + "\n\n")
        f.write("_*Highlights: " + str(len(books[book]['highlights'])) + "*_\n\n")
        for h in books[book]['highlights']:
            f.write(h + '\n\n')
        f.write("\n")
    f.close()

if __name__ == "__main__":
    books = gethighlightsfromdb()
    writetofile(books=books)
