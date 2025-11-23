import streamlit as st

import streamlit as st
import os
import gdown
import zipfile
import time

import streamlit as st
import gdown
import zipfile
import time

import shutil
from tensorflow.keras.preprocessing.image import ImageDataGenerator

import streamlit as st
import numpy as np
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

st.markdown('''
Esse pedaço do código é responsável por configurar o ambiente inicial. Ele baixa o arquivo compactado (.zip) que contém todo o dataset de imagens (treino, validação e teste) e o descompacta em um diretório de trabalho específico, garantindo que os dados estejam prontos para serem acessados pelas etapas seguintes.
''')

st.markdown('Garante que as imagens de teste estejam separadas em subpastas de classe (caneca e pote), um formato obrigatório para que o carregador de dados do TensorFlow/Keras consiga inferir corretamente os rótulos de cada imagem.')

st.markdown("# Caneca ou Pote?")
st.markdown("### Preparando o dataset...")

pasta = "dataset"
arquivo_zip = os.path.join(pasta, "dataset_imgs.zip")
os.makedirs(pasta, exist_ok=True)

# Elementos de feedback
status = st.empty()
progress_bar = st.progress(0)

# === 1. Verifica e faz download se necessário ===
if not os.path.exists(arquivo_zip):
    status.markdown("⏳ **Baixando o dataset (~200MB)...**")
    progress_bar.progress(30)
    gdown.download(
        "https://drive.google.com/uc?id=1IIBVb_WyhxokNdHeF3kerjOHCpL_Y8GK",
        arquivo_zip,
        quiet=False
    )
    status.markdown("✅ **Download concluído com sucesso!**")
    progress_bar.progress(60)
else:
    status.markdown("✅ **Dataset já baixado anteriormente**")
    progress_bar.progress(60)

# === 2. Verifica e descompacta se necessário ===
if len(os.listdir(pasta)) <= 1:  # só tem o zip (ou está vazio)
    status.markdown("⏳ **Descompactando os arquivos...**")
    with zipfile.ZipFile(arquivo_zip, 'r') as f:
        f.extractall(pasta)
    progress_bar.progress(100)
    time.sleep(0.8)
    status.markdown("🎉 **Dataset descompactado e pronto para uso!**")
else:
    status.markdown("✅ **Dataset já descompactado e pronto**")
    progress_bar.progress(100)

# Finalização
time.sleep(1)
progress_bar.empty()
status.empty()
st.markdown("**Tudo carregado com sucesso!** 🚀")
st.markdown("---")

st.markdown('Esta célula realiza a conversão essencial de um formato de dataset (YOLO, com imagens e rótulos separados) para o formato exigido pelo Keras para Classificação: imagens organizadas em subpastas de classe (Caneca e Pote).')

st.markdown("### Organizando o dataset (só na primeira vez)...")

# Barra de progresso + status
progress_bar = st.progress(0)
status = st.empty()

# Diretórios
base_dir = 'dataset/colab_fase6_cap1/arquivos'
train_dir = os.path.join(base_dir, 'imagens/treino')
val_dir   = os.path.join(base_dir, 'imagens/val')
test_dir  = os.path.join(base_dir, 'teste')

# Passo 1: Criar pastas
status.markdown("Criando estrutura de pastas (Caneca / Pote)...")
for dir_path in [train_dir, val_dir, test_dir]:
    os.makedirs(os.path.join(dir_path, 'Caneca'), exist_ok=True)
    os.makedirs(os.path.join(dir_path, 'Pote'),   exist_ok=True)
progress_bar.progress(20)

# Passo 2: Organizar treino e validação (com .txt)
status.markdown("Organizando imagens de treino e validação usando arquivos .txt...")
def organize_with_labels(src):
    count = 0
    for f in os.listdir(src):
        if f.endswith('.png'):
            txt = os.path.join(src, f.replace('.png', '.txt'))
            if os.path.exists(txt):
                label = int(open(txt).readline().split()[0])
                cls = 'Caneca' if label == 0 else 'Pote'
                dest = os.path.join(src, cls, f)
                if not os.path.exists(dest):
                    shutil.copy(os.path.join(src, f), dest)
                    count += 1
    return count

organize_with_labels(train_dir)
organize_with_labels(val_dir)
progress_bar.progress(60)

# Passo 3: Organizar teste por nome
status.markdown("Organizando imagens de teste por nome (frame → Caneca | rotated → Pote)...")
count_test = 0
for f in os.listdir(test_dir):
    if f.endswith('.png'):
        src = os.path.join(test_dir, f)
        if f.startswith('frame'):
            shutil.copy(src, os.path.join(test_dir, 'Caneca', f))
            count_test += 1
        elif f.startswith('rotated'):
            shutil.copy(src, os.path.join(test_dir, 'Pote', f))
            count_test += 1
progress_bar.progress(90)

# Passo 4: Criar generators
status.markdown("Criando geradores de dados...")
datagen = ImageDataGenerator(rescale=1./255)
train_gen = datagen.flow_from_directory(train_dir, target_size=(150,150), batch_size=32, class_mode='binary')
val_gen   = datagen.flow_from_directory(val_dir,   target_size=(150,150), batch_size=32, class_mode='binary')
test_gen  = datagen.flow_from_directory(test_dir,  target_size=(150,150), batch_size=32, class_mode='binary', shuffle=False)

progress_bar.progress(100)
status.markdown("**Tudo pronto! Dataset organizado e geradores criados**")
st.success(f"Dataset preparado: {train_gen.samples} treino | {val_gen.samples} val | {test_gen.samples} teste")
st.markdown("---")

# Limpa a barra depois de 2 segundos
import time
time.sleep(2)
progress_bar.empty()
status.empty()

st.markdown('Esta célula constrói a arquitetura completa da Rede Neural Convolucional (CNN) do zero e a prepara para o treinamento, definindo como ela aprenderá e como seu desempenho será medido.')

import streamlit as st
from tensorflow.keras import Sequential, layers
import tensorflow as tf

st.markdown("### Criando e compilando o modelo CNN...")

with st.spinner("Montando a rede neural..."):
    model = Sequential([
        layers.Conv2D(16, (3,3), activation='relu', input_shape=(150,150,3)),
        layers.MaxPooling2D(2,2),
        layers.Conv2D(32, (3,3), activation='relu'),
        layers.MaxPooling2D(2,2),
        layers.Conv2D(64, (3,3), activation='relu'),
        layers.MaxPooling2D(2,2),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dense(1, activation='sigmoid')
    ])

    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy']
    )

# Exibe o resumo do modelo de forma bonita
st.markdown("**Modelo criado com sucesso!** Aqui está a arquitetura:")
with st.expander("Ver detalhes da CNN", expanded=False):
    # Captura o summary como texto
    stream = st.text("")
    model.summary(print_fn=lambda x: stream.markdown(f"`{x}`"))
    
st.success("Modelo CNN pronto para treinamento!")
st.markdown("---")

st.markdown('Esta célula inicia o processo de aprendizado da CNN (model.fit) e utiliza o mecanismo Early Stopping para controlar a duração do treinamento, garantindo que o modelo pare de treinar assim que o desempenho parar de melhorar na validação, prevenindo o overfitting e otimizando o tempo.')

import streamlit as st
from tensorflow.keras.callbacks import EarlyStopping
import time

st.markdown("### Treinando o modelo CNN...")

# EarlyStopping
es = EarlyStopping(
    monitor='val_accuracy',
    patience=7,
    restore_best_weights=True,
    verbose=1
)

# Placeholder para barra e métricas
progress_bar = st.progress(0)
status_text = st.empty()
loss_placeholder = st.empty()
acc_placeholder = st.empty()

# Callback customizado para atualizar a barra em tempo real
class StreamlitCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        logs = logs or {}
        progress = (epoch + 1) / self.params['epochs']
        progress_bar.progress(progress)
        
        status_text.markdown(f"**Época {epoch + 1}/{self.params['epochs']}**")
        loss_placeholder.metric("Loss (treino)", f"{logs.get('loss', 0):.4f}")
        acc_placeholder.metric("Acurácia (val)", f"{logs.get('val_accuracy', 0):.4%}")
        
        if logs.get('val_accuracy', 0) >= 0.98:
            status_text.markdown("**Acurácia excelente! Parando antes...**")
            self.model.stop_training = True

# Treinamento
start_time = time.time()

with st.spinner("Treinando a rede neural... Isso pode levar alguns minutos"):
    history = model.fit(
        train_gen,
        epochs=50,
        validation_data=val_gen,
        callbacks=[es, StreamlitCallback()],
        verbose=0
    )

train_time = time.time() - start_time

# Resultado final
progress_bar.progress(1.0)
st.success(f"**Treinamento concluído em {train_time:.1f} segundos!**")

# Métricas finais
final_val_acc = max(history.history['val_accuracy'])
st.metric("Melhor acurácia de validação", f"{final_val_acc:.4%}")

# Salva o modelo automaticamente
model.save("modelo_caneca_pote.h5")
st.markdown("**Modelo treinado e salvo como `modelo_caneca_pote.h5`**")

st.markdown("---")

st.markdown('Esta célula realiza a etapa final do processo de classificação: avaliar o desempenho real do modelo no conjunto de Teste e diagnosticar seus erros através da visualização da Matriz de Confusão.')

st.markdown("### Avaliando o modelo no conjunto de teste...")

with st.spinner("Gerando previsões no conjunto de teste..."):
    # Previsão
    predictions = model.predict(test_gen, steps=len(test_gen), verbose=0)
    y_pred = (predictions > 0.5).astype(int).ravel()
    y_true = test_gen.labels

    # Matriz de confusão
    cm = confusion_matrix(y_true, y_pred)
    class_names = ['Caneca', 'Pote']  # ordem correta (0=Caneca, 1=Pote)

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=class_names, yticklabels=class_names,
                ax=ax, cbar=False)
    plt.title('Matriz de Confusão no Conjunto de Teste', fontsize=16, pad=20)
    plt.ylabel('Rótulo Verdadeiro', fontsize=12)
    plt.xlabel('Rótulo Predito', fontsize=12)
    
    st.pyplot(fig)

    # Métricas rápidas
    accuracy = np.mean(y_pred == y_true)
    st.metric("Acurácia no conjunto de teste", f"{accuracy:.4%}")

    # Resumo bonito
    st.success(f"Modelo acertou {int(accuracy*len(y_true))}/{len(y_true)} imagens de teste!")
    
    if accuracy == 1.0:
        st.balloons()
        st.markdown("**PERFEITO! 100% de acerto no teste!**")

st.markdown("---")