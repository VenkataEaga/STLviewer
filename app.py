import streamlit as st
from vedo import load, show
import os
import uuid
from pathlib import Path
from multiprocessing import Process, Queue
import time

# Title of the app
st.title("STL Viewer with Streamlit and Vedo")

def load_show(stl_path: str, queue: Queue): 
    mesh = load(stl_path).color('#ffc800')  
    show(mesh, bg='white',title='Geometry',axes=4,)
    queue.put('done') 

# Sidebar for file upload
st.sidebar.header("Upload STL File")
uploaded_file = st.sidebar.file_uploader("", type="stl")

if uploaded_file is not None:  # Checking if a file has been uploaded
    unique_id = str(uuid.uuid4())  # Generating a unique identifier

    os.makedirs(f'./data/{unique_id}', exist_ok=True)  # Creating a new directory for the uploaded file
    file_path = f'./data/{unique_id}/file.stl'  # Setting the path for the uploaded file
    
    with open(file_path, 'wb') as f:  # Opening the file in write mode
        f.write(uploaded_file.getbuffer())  # Writing the uploaded file to the new path

    st.success("File uploaded and saved in directory: " + str(file_path))  # Displaying a success message with the file path

    if st.button('Show Mesh'):  # Creating a button for displaying the 3D object
        queue = Queue()  # Creating a queue for parallel processing
        p = Process(target=load_show, args=(file_path, queue))  # Creating a process for loading and showing the 3D object
        p.start()  # Starting the process
        while True:  # Creating an infinite loop
            if not queue.empty():  # Checking if the queue is not empty
                break  # Breaking the loop if the queue is not empty
            time.sleep(0.1)  # Pausing the loop for 0.1 seconds


