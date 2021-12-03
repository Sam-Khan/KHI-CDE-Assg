import streamlit as st
import pymongo
import pandas as pd
import matplotlib.pyplot as plt

from streamlit_pandas_profiling import st_profile_report

from pandas_profiling import ProfileReport

# Initialize connection.
client = pymongo.MongoClient("mongodb+srv://aa:aa@cluster0.7xby5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

db = client.Scrapped_Data
cursor_items = db.complaints.find()

st.title('Karachi AI CDE - Final Assg')
st.header('CFPB - Financial Consumer Complaints Dashboard')

st.write("Total Complaints Count", cursor_items.count(), 
         "Timely Done Complaints", db.complaints.count_documents({ "timely": "Yes"}), 
         "Timely Not Done", db.complaints.count_documents({ "timely": {"$ne":"Yes"}}),
         "No of States", len(db.complaints.distinct( "state" ))
         )

all_records = []
for item in cursor_items:
    del item['_id']
    all_records.append(item)
df = pd.DataFrame(all_records)

TOTAL_COMPLAINTS = df['complaint_id'].count()
TIMELY_COMPLETED =  df[df['timely']=='Yes']['complaint_id'].count()
TIMELY_INCOMPLETED =  df[df['timely']=='No']['complaint_id'].count()
TOTAL_NO_STATES =  len(db.complaints.distinct( "state" ))

profile = ProfileReport(df,

                        title="Financial Consumer Data",

        dataset={

        "description": "This is the Final Assg - Karachi AI CDE ",
        "Demo URL": "https://github.com/Sam-Khan/KHI-CDE-Assg"
        
    }
)
st_profile_report(profile)

# In a static table
st.table(df)

# Graph Plotting

# Only a subset of options selected
x_options = [
    'AL', 'AK', 'AS', 'AZ', 'AR', 'CA','WA'   
]

# Allow use to choose
x_axis = st.sidebar.selectbox('Which value do you want to explore?', x_options)

# 1. plot the value - TIMELY_COMPLETED

fig = px.scatter(df,
                x=x_axis,
                y=TIMELY_COMPLETED,
                hover_name='name',
                title=f'State. {x_axis}')

st.subheader(‘TIMELY COMPLETED’)
st.plotly_chart(fig)

# 2. plot the value - TOTAL_COMPLAINTS
fig = px.scatter(df,
                x=x_axis,
                y=TOTAL_COMPLAINTS,
                hover_name='name',
                title=f'State. {x_axis}')

st.subheader(‘TOTAL COMPLAINTS’)
st.plotly_chart(fig)

# 3. plot the value - TIMELY_INCOMPLETED
fig = px.scatter(df,
                x=x_axis,
                y=TIMELY_INCOMPLETED,
                hover_name='name',
                title=f'State. {x_axis}')

st.subheader(‘TIMELY INCOMPLETED’)
st.plotly_chart(fig)

# 4. plot the value - TOTAL_NO_STATES
fig = px.scatter(df,
                x=x_axis,
                y=TOTAL_NO_STATES,
                hover_name='name',
                title=f'State. {x_axis}')

st.subheader(‘TOTAL NO OF STATES’)
st.plotly_chart(fig)

st.footer('Created By - Samreen Quayum')