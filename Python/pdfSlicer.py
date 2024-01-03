import sys
from tkinter import Tk, Label, Button, Entry, StringVar, messagebox
from pypdf import PdfReader, PdfWriter

class PdfSlicerApp:
    def __init__(self, master):
        self.master = master
        master.title("PDF Slicer")

        self.label = Label(master, text="Enter file name, the Starting and Ending pages:")
        self.label.pack()

        self.start_page_var = StringVar()
        self.end_page_var = StringVar()
        self.file = StringVar()

        self.file = Entry(master, textvariable=self.file)
        self.file.pack()

        self.start_page_entry = Entry(master, textvariable=self.start_page_var)
        self.start_page_entry.pack()

        self.end_page_entry = Entry(master, textvariable=self.end_page_var)
        self.end_page_entry.pack()

        self.slice_button = Button(master, text="Slice PDF", command=self.slice_pdf)
        self.slice_button.pack()

    def slice_pdf(self):
        try:
            start_page = int(self.start_page_var.get())
            end_page = int(self.end_page_var.get())
        except ValueError:
            messagebox.showerror("Error", "Enter valid page numbers.")
            return
        
        pdf_reader = PdfReader(str(self.file.get()))
        output_pdf = PdfWriter()

        try:
            for page in pdf_reader.pages[start_page - 1:end_page]:
                output_pdf.add_page(page)
            output_pdf.write("sliced_doc.pdf")
            messagebox.showinfo("Success", "PDF sliced successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")

if __name__ == "__main__":
    root = Tk()
    app = PdfSlicerApp(root)
    root.mainloop()
