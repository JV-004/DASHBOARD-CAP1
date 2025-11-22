from ultralytics import YOLO
import cv2
import os

def analisar_imagens():
    print("\n=== Fase 6 – Visão Computacional Ativada ===")

    # Carregar modelo YOLO (pré-treinado ou custom)
    modelo = YOLO("phase6/model/yolov8n.pt")

    pasta_imagens = "phase6/images/"

    for arquivo in os.listdir(pasta_imagens):
        caminho_img = os.path.join(pasta_imagens, arquivo)

        if arquivo.lower().endswith((".jpg", ".png", ".jpeg")):
            print(f"\n🔍 Analisando imagem: {arquivo}")

            resultados = modelo(caminho_img)

            img = cv2.imread(caminho_img)

            praga_detectada = False
            diagnostico = "Nenhuma praga detectada."

            for det in resultados[0].boxes:
                classe = int(det.cls[0])
                confianca = float(det.conf[0])
                nome_classe = resultados[0].names[classe]

                x1, y1, x2, y2 = map(int, det.xyxy[0])

                # Desenha bounding box
                cv2.rectangle(img, (x1, y1), (x2, y2), (0,255,0), 2)
                cv2.putText(img, f"{nome_classe} ({confianca:.2f})", 
                            (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 
                            0.6, (0,255,0), 2)

                print(f"🪲 Detecção: {nome_classe} – confiança {confianca:.2f}")

                praga_detectada = True
                diagnostico = "⚠ Praga detectada! Recomendamos inspeção imediata."

            # Salvar imagem anotada
            saida = f"phase6/output/detect_{arquivo}"
            os.makedirs("phase6/output", exist_ok=True)
            cv2.imwrite(saida, img)

            print(f"📸 Imagem processada salva em: {saida}")
            print("📌 Diagnóstico:", diagnostico)

            # --------------------------------------
            # 🚨 GATILHO PARA A FASE 7 (AWS ALERTA)
            # --------------------------------------
            if praga_detectada:
                print("🚨 ALERTA GERADO – enviar e-mail/SMS via AWS!")
                # Aqui chamaremos o serviço SNS na Fase 7.
    
    print("\n✔ Análise concluída.")
