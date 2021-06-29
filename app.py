import os
import streamlit as st
import pandas as pd
from db import Data
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from profiler import get
import json

st.title('linkedin scraper')

folder = "scraped_data"

def opendb():
    engine = create_engine('sqlite:///db.sqlite3') # connect
    Session =  sessionmaker(bind=engine)
    return Session()

def save_file(file,path):
    try:
        db = opendb()
        data = Data(filename=file,extension=".json",filepath=path)
        db.add(data)
        db.commit()
        db.close()
        return True
    except Exception as e:
        st.write("database error:",e)
        return False
@st.cache
def load_company_job():
    df = pd.read_csv(r'scraped_data\companu.csv',index_col='id')
    return df

ch = st.sidebar.selectbox("select option",['scrape profile','company jobs', 'view data','manage data'])
if ch == "company jobs":
    df = load_company_job()
    companies = df.company.unique().tolist()
    companies.sort()
    company = st.selectbox("select a company",companies)
    
    st.title(company)
    companydf = df[df['company']==company].copy()
    st.write(companydf)

if ch == "scrape profile":
    urls = st.text_area("enter a linkedin profile urls, seperated by lines")
    if urls:
        for url in urls.split('\n'):
            name = url.split('/')[4]
            st.info(f"collecting data about {name}")
            filename = os.path.join(folder,name+'.json',)
            st.info(f"storage location: {filename}")
            with st.spinner("this will take some time"):
                get(url,filename)
                st.balloons()
            st.info(f"saving to database")
            save_file(name,filename)
            st.success("saved")
    else:
        st.error("enter linkedin profile urls")
      
if ch == "view data":
    db = opendb()
    results = db.query(Data).all()
    db.close()
    file = st.selectbox("select a profile",results)
    if file and os.path.exists(file.filepath):
        with open(file.filepath) as f:
            st.write(json.loads(f.read()))

if ch == "manage data":
    db = opendb()
    results = db.query(Data).all()
    db.close()
    file = st.selectbox("select a profile",results)
    if file and os.path.exists(file.filepath) and st.button("click to delete"):
        try:
            os.unlink(file.filepath)
        except:
            pass
        db.query(Data).filter(id == file.id).delete()
        st.success("deleted the data")