from transformers import AutoModelForCausalLM, AutoTokenizer
import streamlit as st
import torch


tokenizer = AutoTokenizer.from_pretrained("ansumanpandey/codgen-finetuned-SQLQueryGeneration")
model = AutoModelForCausalLM.from_pretrained("ansumanpandey/codgen-finetuned-SQLQueryGeneration")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)


def get_sql(query):
    input_text = "<s> Query to %s </s>" % query
    features = tokenizer([input_text], return_tensors='pt')

   
    output = model.generate(input_ids=features['input_ids'],
                            attention_mask=features['attention_mask'],
                            max_length=150,
                            num_return_sequences=1)     
   
    sql_query = tokenizer.decode(output[0], skip_special_tokens=True)
    return sql_query




st.title("Model SQL Query Generator")
input_text = st.text_area("Write a SQL query to:", "Give me name and age of the employee from a table")
output_query = ""  
string1=""
if st.button('Generate SQL Query'):
  
    output_query = get_sql(input_text)
list1 =['']
list2=['']
list3=['']
list4=['']
debug_string=""
debug_string=output_query
if ';' in output_query:
    list1= output_query.split(';')
    if(list1!=[]):
       string1=list1[0]
if  ']' in output_query:
    list2= output_query.split(']')
    if(list2!=[]):
       string1=list2[0]
if  '[' in string1:
    list3=string1.split('[')
    if(list3!=[]):
      string1=list3[0]
if '  ' in string1:
    list4= string1.split('  ')
    if(list4!=[]):
       string1=list4[0]


st.text_area("Generated SQL Query:",string1, height=300)
st.text_area("Output SQL Query:",debug_string, height=300)



