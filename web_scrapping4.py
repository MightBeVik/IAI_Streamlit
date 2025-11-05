import streamlit as st
from bs4 import BeautifulSoup
import requests
import pandas as pd


def get_data(dept, designs):
    url = requests.get(f'https://www.{dept}.ruet.ac.bd/teacher_list').text
    soup = BeautifulSoup(url, 'lxml')
    teachers = soup.find_all('tr')[1:]

    names_en = []
    designations = []
    emails = []
    phones = []
    departments = []

    for teacher in teachers:
        name_en = teacher.find_all('td')[1].text.strip()
        designation = teacher.find_all('td')[3].text.strip()
        email = teacher.find_all('td')[5].text.strip()
        phone = teacher.find_all('td')[6].text.strip()
        department = teacher.find_all('td')[4].text.strip()
        if designs:
            if designation in designs:
                names_en.append(name_en)
                designations.append(designation)
                emails.append(email)
                phones.append(phone)
                departments.append(department)

        
    data = pd.DataFrame({
        'Name': names_en,
        'Designation': designations,
        'Email': emails,
        'Phone': phones,
        'Department': departments
        })
    return data



def main():
    st.title('RUET Teachers\' Information')
    #department selection
    depts = ['EEE', 'CSE', 'ETE', 'ECE', 'CHEM', 'MATH', 'PHY', 'IPE', 'CHE', 'BECM', 'ME', 'URP', 'ARCHI', 'CE']
    dept = st.sidebar.selectbox('Select Department', depts).lower()
    prof = st.sidebar.checkbox('Professor', value = True)
    assistant_prof = st.sidebar.checkbox('Assistant Professor', value = True)
    associate_prof = st.sidebar.checkbox('Associate Professor', value = True)
    lecturer = st.sidebar.checkbox('Lecturer', value = True)
    senior_lecturer = st.sidebar.checkbox('Senior Lecturer', value = True)
    instructor = st.sidebar.checkbox('Instructor', value = True)
    options = []

    if prof:
        options.append('Professor')
    if assistant_prof:
        options.append('Assistant Professor')
    if associate_prof:
        options.append('Associate Professor')
    if lecturer:
        options.append('Lecturer')
    if senior_lecturer:
        options.append('Senior Lecturer')
    if instructor:
        options.append('Instructor')

    if dept:
        filtered_data = get_data(dept, options)
        st.dataframe(filtered_data)
        



#CONSTRUCTOR
if __name__ == '__main__':
    main()
