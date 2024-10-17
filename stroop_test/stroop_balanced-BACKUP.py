import pygame
import random
import time
import os
import numpy as np
import matplotlib.pyplot as plt  # Per la creazione del grafico
from scipy.stats import norm  # Per la regressione gaussiana

# Inizializzazione di pygame
pygame.init()

# Impostazione della finestra (massimizzata)
screen = pygame.display.set_mode((1280, 960))
pygame.display.set_caption("Test di Stroop")

# Definire i colori RGB
COLORI = {
    "Blu": (0, 0, 255),
    "Giallo": (255, 255, 0),
    "Verde": (0, 255, 0),
    "Rosso": (255, 0, 0)
}

# Definire la lista delle parole
PAROLE = ["Blu", "Giallo", "Verde", "Rosso"]

# Font e dimensioni
font = pygame.font.SysFont(None, 200)

# Funzione per visualizzare testo
def mostra_testo(testo, colore, posizione):
    testo_renderizzato = font.render(testo, True, colore)
    screen.blit(testo_renderizzato, posizione)
    pygame.display.update()

# Funzione per visualizzare il simbolo "+" per il cambio di parola
def mostra_simbolo_cambio():
    screen.fill((255, 255, 255))
    mostra_testo("+", (0, 0, 0), (400, 250))
    pygame.display.update()
    time.sleep(0.5)  # Mostra il simbolo "+" per mezzo secondo

# Funzione per ottenere l'input utente
def get_info():
    print("Inizio input utente.")  # Debug
    nome = input("Nome: ")
    cognome = input("Cognome: ")

    # Input per l'età
    while True:
        try:
            eta = int(input("Età (0-130): "))  # Converti l'input in un intero
            if 0 <= eta <= 130:  # Controlla se l'età è nel range corretto
                break  # Esci dal ciclo se l'età è valida
            else:
                print("Errore: l'età deve essere tra 0 e 130.")
        except ValueError:
            print("Errore: inserisci un numero valido per l'età.")

    # Input per il genere (M/F)
    while True:
        genere = input("Genere (M/F): ").upper()
        if genere in ["M", "F"]:
            break
        else:
            print("Errore: inserisci 'M' per Maschio o 'F' per Femmina.")

    # Richiesta del titolo di studio
    print("Inserire il numero che corrisponde al proprio titolo di studio:")
    print("1) Nessuno")
    print("2) Licenza elementare")
    print("3) Licenza media")
    print("4) Diploma")
    print("5) Laurea triennale")
    print("6) Laurea magistrale")
    print("7) Master specialistico")
    print("8) Dottorato di ricerca")

    titoli = {
        "1": "Nessuno",
        "2": "Licenza elementare",
        "3": "Licenza media",
        "4": "Diploma",
        "5": "Laurea triennale",
        "6": "Laurea magistrale",
        "7": "Master specialistico",
        "8": "Dottorato di ricerca"
    }

    while True:
        titolo_input = input("Numero del titolo di studio: ")
        if titolo_input in titoli:
            titolo_studio = titoli[titolo_input]
            break
        else:
            print("Errore: inserisci un numero valido (1-8).")

    # Scegliere il numero di trials (minimo 30)
    while True:
        try:
            trials = int(input("Numero di trials (minimo 30): "))
            if trials >= 30:
                break
            else:
                print("Errore: il numero di trials deve essere almeno 30.")
        except ValueError:
            print("Errore: inserisci un numero valido.")

    # Creare il nome del file
    file_nome = f"{nome}_{cognome}_{eta}.txt"

    # Aprire il file in scrittura
    with open(file_nome, 'w') as f:
        f.write(f"Nome: {nome}\nCognome: {cognome}\nEtà: {eta}\nGenere: {genere}\nTitolo di studio: {titolo_studio}\n")
        f.write(f"Numero di trials: {trials}\n")
        f.write(f"Risultati del test di Stroop:\n")
        f.write(f"{'Risposta':<10}{'Tempo (ms)':<15}\n")  # Intestazione colonne

    print("Input utente completato. ATTENZIONE: disporre le dita sui tasti 'i' e 'c'. Il test inizia tra pochi secondi.")  # Debug
    return file_nome, trials

# Funzione per calcolare statistiche e indice di Stroop
def calcola_statistiche(risultati):
    tempi_corretti = [t for r, t in risultati if r == "C"]
    tempi_incorretti = [t for r, t in risultati if r == "I"]

    if tempi_corretti:
        media_corretti = np.mean(tempi_corretti)
        varianza_corretti = np.var(tempi_corretti)
        dev_std_corretti = np.std(tempi_corretti)
    else:
        media_corretti = varianza_corretti = dev_std_corretti = 0

    if tempi_incorretti:
        media_incorretti = np.mean(tempi_incorretti)
        varianza_incorretti = np.var(tempi_incorretti)
        dev_std_incorretti = np.std(tempi_incorretti)
    else:
        media_incorretti = varianza_incorretti = dev_std_incorretti = 0

    indice_stroop = media_incorretti - media_corretti

    return (media_corretti, varianza_corretti, dev_std_corretti, 
            media_incorretti, varianza_incorretti, dev_std_incorretti, indice_stroop)

# Funzione per creare il grafico delle gaussiane
def crea_grafico(tempi_corretti, tempi_incorretti, file_nome):
    plt.figure()
    
    # Plot delle distribuzioni gaussiane
    if tempi_corretti:
        plt.hist(tempi_corretti, bins=15, density=True, alpha=0.6, color='g', label='Corretti')
    if tempi_incorretti:
        plt.hist(tempi_incorretti, bins=15, density=True, alpha=0.6, color='r', label='Incorretti')
    
    # Creazione delle gaussiane di regressione
    if tempi_corretti:
        mu_corretti, std_corretti = np.mean(tempi_corretti), np.std(tempi_corretti)
        x_corretti = np.linspace(min(tempi_corretti), max(tempi_corretti), 100)
        p_corretti = norm.pdf(x_corretti, mu_corretti, std_corretti)
        plt.plot(x_corretti, p_corretti, 'k', linewidth=2, label='Gaussiana Corretti')
        
        # Aggiungi linea verticale per la media corretta
        plt.axvline(mu_corretti, color='blue', linestyle='--', label='Media Corretti')
        # Aggiungi linee orizzontali per le deviazioni standard
        plt.hlines(norm.pdf(mu_corretti, mu_corretti, std_corretti), 
                   mu_corretti - std_corretti, mu_corretti + std_corretti, 
                   colors='blue', linestyles='--', label='Dev. Std. Corretti')

    if tempi_incorretti:
        mu_incorretti, std_incorretti = np.mean(tempi_incorretti), np.std(tempi_incorretti)
        x_incorretti = np.linspace(min(tempi_incorretti), max(tempi_incorretti), 100)
        p_incorretti = norm.pdf(x_incorretti, mu_incorretti, std_incorretti)
        plt.plot(x_incorretti, p_incorretti, 'k', linewidth=2, label='Gaussiana Incorretti')
        
        # Aggiungi linea verticale per la media incorretta
        plt.axvline(mu_incorretti, color='red', linestyle='--', label='Media Incorretti')
        # Aggiungi linee orizzontali per le deviazioni standard
        plt.hlines(norm.pdf(mu_incorretti, mu_incorretti, std_incorretti), 
                   mu_incorretti - std_incorretti, mu_incorretti + std_incorretti, 
                   colors='red', linestyles='--', label='Dev. Std. Incorretti')

    plt.title('Distribuzione Tempi di Risposta - Test di Stroop')
    plt.xlabel('Tempo (ms)')
    plt.ylabel('Frequenza')
    plt.legend()
    
    # Salva il grafico come immagine PNG con lo stesso nome del file di testo
    grafico_file = file_nome.replace('.txt', '_grafico.png')
    plt.savefig(grafico_file)
    plt.close()

# Funzione principale per il test di Stroop
def test_stroop(file_nome, trials):
    risultati = []
    stimoli_congruenti = stimoli_incongruenti = 0

    for _ in range(trials):
        mostra_simbolo_cambio()

        parola = random.choice(PAROLE)
        colore = random.choice(list(COLORI.values()))

        # Determina se lo stimolo è congruente o incongruente
        congruente = COLORI[parola] == colore
        if congruente:
            stimoli_congruenti += 1
        else:
            stimoli_incongruenti += 1

        screen.fill((255, 255, 255))
        mostra_testo(parola, colore, (400, 250))

        start_time = time.time()
        risposta_data = False
        risposta = None

        while not risposta_data:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_i:
                        risposta = "C"  # Coerente
                        risposta_data = True
                    elif event.key == pygame.K_c:
                        risposta = "I"  # Incoerente
                        risposta_data = True

        reaction_time = (time.time() - start_time) * 1000  # Tempo in millisecondi
        risultati.append((risposta, reaction_time))

        # Scrivi il risultato nel file
        with open(file_nome, 'a') as f:
            f.write(f"{risposta:<10}{reaction_time:<15.2f}\n")

    # Scrivi le percentuali di stimoli congruenti e incongruenti nel file
    percentuale_congruenti = (stimoli_congruenti / trials) * 100
    percentuale_incongruenti = (stimoli_incongruenti / trials) * 100
    with open(file_nome, 'a') as f:
        f.write(f"\nFrequenza stimoli congruenti: {percentuale_congruenti:.2f}%\n")
        f.write(f"Frequenza stimoli incongruenti: {percentuale_incongruenti:.2f}%\n")

    # Calcola statistiche e indice di Stroop
    (media_corretti, varianza_corretti, dev_std_corretti, 
     media_incorretti, varianza_incorretti, dev_std_incorretti, indice_stroop) = calcola_statistiche(risultati)

    with open(file_nome, 'a') as f:
        f.write(f"\nStatistiche:\n")
        f.write(f"Media tempi corretti: {media_corretti:.2f} ms\n")
        f.write(f"Deviazione standard corretti: {dev_std_corretti:.2f} ms\n")
        f.write(f"Media tempi incorretti: {media_incorretti:.2f} ms\n")
        f.write(f"Deviazione standard incorretti: {dev_std_incorretti:.2f} ms\n")
        f.write(f"Indice di Stroop: {indice_stroop:.2f} ms\n")

    # Separa i tempi corretti e incorretti per il grafico
    tempi_corretti = [t for r, t in risultati if r == "C"]
    tempi_incorretti = [t for r, t in risultati if r == "I"]

    # Crea il grafico
    crea_grafico(tempi_corretti, tempi_incorretti, file_nome)

# Funzione principale per l'esecuzione del programma
def main():
    # Ottenere l'input dell'utente
    file_nome, trials = get_info()

    # Eseguire il test di Stroop
    test_stroop(file_nome, trials)

    print("Test completato. I risultati sono stati salvati.")

if __name__ == "__main__":
    main()

    # Chiudi pygame alla fine
    pygame.quit()