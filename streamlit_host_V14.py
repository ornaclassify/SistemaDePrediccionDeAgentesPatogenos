import numpy as np
import streamlit as st
from tensorflow import keras
import pandas as pd
import os,datetime
from bd import *
from PIL import Image, ImageOps
import matplotlib.pyplot as plt

from keras.preprocessing.image import img_to_array
from keras.applications.imagenet_utils import preprocess_input


st.image(Image.open(os.path.join('logoOnacol.jpg')))
st.title("Predicción de Agentes Patógenos")

st.write("---")

st.header("Predicción")
model = keras.models.load_model('modeloPatog3V14.h5')

st.set_option('deprecation.showfileUploaderEncoding',False)
uploaded_file = st.file_uploader("Elija una imágen del dispositivo", type=["jpg", "jpeg", "png"])

############################################## CLASIFICACIÓN ##################################################
map_dict = {0: 'Araña roja',
            1: 'Pulgón',
            2: 'Sana'
            }

def import_and_predict(image_data, model):
    size = (224,224)
    image = ImageOps.fit(image_data, size )#Image.ANTIALIAS
    img = img_to_array(image) #img = np.asarray(image)
    y = np.expand_dims(img, axis=0) ###non
    #img_reshape = img[np.newaxis,...]
    img_reshape = preprocess_input(y)
    prediction = model.predict(img_reshape)
    return prediction

if uploaded_file is not None:
    imagen=st.image(uploaded_file, channels="RGB",width=350)

    Genrate_pred = st.button("Clasificar")    
    if Genrate_pred: 
        image = Image.open(uploaded_file)
        predictions = import_and_predict(image, model)
        prediction1="La casificaión es: "+map_dict[np.argmax(predictions)]
        st.title(prediction1)

st.write("---")

############################################## REGISTRO ##########################################################################
st.header("Registro")

createTable()

with st.form(key="registro_prediction"):
    prediccion=st.selectbox("Predicción",("Araña Roja","Pulgón","Sana"))
    vivero=st.selectbox("Vivero",("006 Vivero Palma Rosa","008 Vivero Massangeana SPR de RL","0014 Vivero Los Olivos","0018 Vivero del Centro","Otro 1","Otro 2"))
    fecha_registro=st.date_input("Fecha", datetime.datetime.now())
    boton_guardar=st.form_submit_button("Guardar datos")

if boton_guardar:
    add_data(prediccion,vivero,fecha_registro)

    ## add_data(x1,prediction,vivero,date)

    st.success("Datos guardados")

st.write("---")
st.subheader("Tabla de registros")
verDatos = view_all_data()

defi = pd.DataFrame(verDatos,columns=["id_prediccion", "Predicción", "Vivero", "Fecha"])
st.dataframe(defi,width=700)

st.markdown('**Eliminar registro**')
unique_list = [i[0] for i in view_all_rowid()]
eliminar_prov =  st.selectbox("Seleccione No. de registro a eliminar",unique_list)
if st.button("Eliminar"):
    delete_data(eliminar_prov)
    st.success("Registro eliminado")

st.write("---")

######################################### TABLA DE REGISTROS ##########################################################

#defi = pd.read_csv('Registros_Ornacol.csv', encoding='latin-1',error_bad_lines=False)

#st.dataframe(defi)

st.header("Reportes")


################################################ REPORTES #################################################################
st.subheader("Proporcional")
Rep_HyM=st.checkbox("Gráfico de círculo de proporciones entre tipo de patógeno")
if Rep_HyM:
    circ_report=defi.Predicción.value_counts(normalize=True)
    x=circ_report.values
    plt.pie(x,labels=['Pulgón',"Araña Roja", "Sana"], autopct='%1.1f%%')
    plt.show()

    st.pyplot(plt)
    plt.clf()
    

st.subheader("Por vivero")
Rep_NE=st.checkbox("Reporte de detección de patógenos según vivero")
if Rep_NE:
    chicas2=defi.Vivero.loc[defi.Predicción=="Araña Roja"].value_counts()
    chicas3=defi.Vivero.loc[defi.Predicción=="Pulgón"].value_counts()
    chicas4=defi.Vivero.loc[defi.Predicción=="Sana"].value_counts()
    x33=chicas2.index
    y33=chicas2.values
    x11=chicas3.index
    y11=chicas3.values
    x111=chicas4.index
    y111=chicas4.values

    plt.barh(x11,y11, label='Pulgón',height=0.4,align='center')
    plt.barh(x33,y33, label='Araña roja',height=-0.4,align='edge')
    plt.barh(x111,y111, label='Sana',height=-0.2,align='center')
    plt.legend()
    plt.title('Reporte de detección de patógenos según vivero')
    plt.ylabel('Vivero')
    plt.xlabel('Cantidad')
    plt.show()

    st.pyplot(plt)
    plt.clf()


st.subheader("Por fecha")
Rep_NE2=st.checkbox("Reporte de detección de patógenos según fecha")
if Rep_NE2:
    chicas44=defi.Fecha.loc[defi.Predicción=="Araña Roja"].value_counts()
    chicas5=defi.Fecha.loc[defi.Predicción=="Pulgón"].value_counts()
    chicas6=defi.Fecha.loc[defi.Predicción=="Sana"].value_counts()
    x333=chicas44.index
    y333=chicas44.values
    x111=chicas5.index
    y111=chicas5.values
    x1111=chicas6.index
    y1111=chicas6.values

    plt.barh(x111,y111, label='Pulgón',height=0.4,align='center')
    plt.barh(x333,y333, label='Araña roja',height=-0.4,align='edge')
    plt.barh(x1111,y1111, label='Sana',height=-0.2,align='center')
    plt.legend()
    plt.title('Reporte de detección de patógenos según fecha')
    plt.ylabel('Fecha')
    plt.xlabel('Cantidad')
    plt.show()

    st.pyplot(plt)
    plt.clf()

st.write("---")
