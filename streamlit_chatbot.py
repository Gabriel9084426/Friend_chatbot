import streamlit as st 
import os
import json
import time 
from openai import OpenAI 
client = OpenAI(api_key=os.getenv("Api_key"))
st.set_page_config(
    page_title="my chatbot",
    page_icon="%",
    layout="wide"
)

st.markdown("""
    <style>
    .stApp {
        background-color: #001F3F; /* dark navy blue */
        color: white;
    }
    section[data-testid="stSidebar"] {
        background-color: #002B5B; /* sidebar dark blue */
        color: white;
    }
    .stTextInput > div > div > input {
        background-color: #003366; 
        color: white;
    }
    div.stButton > button {
        background-color: #004080;
        color: white;
        border: 1px solid #0059b3;
        border-radius: 5px;
    }
    div.stButton > button:hover {
        background-color: #0059b3;
        color: #ffffff;
    }
    h1, h2, h3 {
        color: #66B2FF;
    }
    </style>
""", unsafe_allow_html=True)
st.title("Welcome to your own chatbot!")
st.write("your friend!")

friends_folder = "friends"
os.makedirs(friends_folder, exist_ok=True)
friend_files = [f for f in os.listdir(friends_folder) if f.endswith(".json")]
friend_files.append("+create a new friend")
choice = st.sidebar.selectbox("select a friend:   ", friend_files)




if choice=="+create a new friend":

    st.title("create a new friend")
    st.markdown("---")
    name=st.text_input("your friend's name here")
    personality=st.text_input("your friend's personality")
    hobbies=st.text_input("your friend's hobby")

    if st.button("Save Friend"):
        new_friend={
            "name": name,
            "personality": personality,
            "hobbies": hobbies
        }
        saving_path=os.path.join("friends",f"{name.lower().replace(' ', '_')}.json")
        with open(saving_path,"w") as f:
            json.dump(new_friend,f)
        st.success(f"✅ New friend {name} created")
        time.sleep(2)

        st.rerun()
    st.stop()






#os.path.join()


with open(os.path.join(friends_folder,choice),"r") as f :
    friend=json.load(f)
    
st.sidebar.success(f"friend {friend['name']} Load")
st.sidebar.write(f"personality:{friend['personality']}")
st.sidebar.write(f"Hobbies:{friend['hobbies']}")
    

#implementing the message history
if "history" not in st.session_state:
    st.session_state.history = []




st.title(f" Chat with {friend['name']}")


#Message's bubbles
for role, content in st.session_state.history:
    with st.chat_message(role):
        st.markdown(content)






st.subheader("chat window")

chat_question = st.text_input("type your message here")

if chat_question:

    st.session_state.history.append(("user",chat_question))
    with st.chat_message("user"):
        st.markdown(chat_question)
        
     
    
    prompt=f"""
    you are {friend['name']},a chatbot friend,your personality is {friend['personality']},your hobbies are {friend['hobbies']} now answer this question:

    """

    messages=[{"role": "system","content": prompt}]
    for role, content in st.session_state.history:
        messages.append({"role":role, "content": content})
        
    response = client.chat.completions.create(
        
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.7,
        max_completion_tokens=230
        ) 


    reply = response.choices[0].message.content.strip()
    st.session_state.history.append(("assistant",reply))

    with st.chat_message("assistant"):
        st.markdown(reply)








