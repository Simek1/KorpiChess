[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) ![Pygame-powered](https://www.pygame.org/docs/_static/pygame_powered_lowres.png)
---


**Table of contents**

1. [Introduction](#introduction)
2. [Instruction](#instruction)
3. [Code requirements](#code-requirements)
4. [Wprowadzenie 🇵🇱](#wprowadzenie)
5. [Instrukcja 🇵🇱](#instrukcja)
6. [Wymagania kodu 🇵🇱](#wymagania-kodu)


# Introduction

Project made as a part of my master thesis. It brings a modified version of chess into the digital realm, allowing players to enjoy the game both over a local area network (LAN) and in a hotseat mode. Korpalski Chess introduces new elements to the classic game, offering chess enthusiasts the opportunity to explore various variations of this strategic game. The physical game's creator is Robert Korpalski, whose creations you can discover [here](https://szachydzieciom.pl/?page_id=67492).

# Instruction

You can find full list of EN game rules [here](https://www.apronus.com/chess/korpalskichess.htm).

![menu.png](/readme_imgs/menu.png)

1- Set your nick in LAN mode here

2- Hotseat mode

3- LAN mode

4- Settings

5- Exit

**How to play on LAN**

*You can play with people outside your LAN if both of you are on the same [Hamachi](https://vpn.net) network.*

![LAN menu](/readme_imgs/joincreate.png)

**The hosting person** creates a server (section number 2 in the image) by providing the server's IP address (number 7 in the image) and port (number 8 in the image), then press the "Stwórz" button. Leaving the default IP (0.0.0.0) will allow joining the server using all IPs associated with the computer. For instance, it will be possible to connect using IP from the Hamachi network as well as the local IP. In section number 4 of the image, both your internal IP, which should be provided by the person joining the server connecting through LAN, and your external IP (censored) are displayed.

**The person joining the server** (section number 1 in the image) needs to provide the server's IP address (number 5 in the image) and the port it's open on (number 6 in the image), then press the "Dołącz" button.

**Game window**

![Game window](/readme_imgs/gamewindow.png)

1- Chessboard.

2- Your captured pieces, which you can exchange for a pawn when it reaches the transformation line.

3- Your opponent's captured pieces.

4- Your unused piecies.

5- Your opponent's unused pieces.

6- Chat window (only in LAN game).

**Settings**

![Settings](/readme_imgs/settings.png)

1- You can turn on/off and set timers there.

2- You can change resolution and turn on/off full screen there.

# Code requirements

In releases tab, there is an exe file that can be launched even without python on your computer but it needs to be in same folder as folder "images".
Code has been written in Python 3.10. It uses the following libraries:
- Pygame, user interface.

- Socket, for online game.

- Threading, for multitasking.

- Requests, to get your external IP.

---

# Wprowadzenie

Projekt został stworzony jako część mojej pracy magisterskiej. Przenosi zmodyfikowaną wersję szachów do świata cyfrowego, pozwalając graczom cieszyć się grą zarówno poprzez lokalną sieć (LAN), jak i w trybie hotseat. Korpalski Chess wprowadza nowe elementy do klasycznej gry, oferując pasjonatom szachów możliwość eksploracji różnorodnych wariantów tej strategicznej gry. Twórcą fizycznej wersji gry jest Robert Korpalski, którego twórczość możesz poznać [tutaj](https://szachydzieciom.pl/?page_id=67492).

# Instrukcja

Pełny spis zasad oraz opis gry znajdują się [tutaj](https://szachydzieciom.pl/?page_id=67492).

**Jak grać przez LAN**

Pełna instrukcja połączenia się przez sieć LAN oraz przez hamachi została zamieszczona w pliku "Instrukcja do gry sieciowej" spakowana wraz z plikiem exe.

**Okno gry**

![Game window](/readme_imgs/gamewindow.png)

1- Szachownica.

2- Twoje zbite figury, w które może zmienić się pionek po dojściu na linię transformacji.

3- Zbite pionki twojego przeciwnika.

4- Twoje nie użyte jeszcze bierki.

5- Nie użyte jeszcze bierki twojego przeciwnika.

6- Okno czatu (tylko w grze sieciowej).

**Ustawienia**

![Settings](/readme_imgs/settings.png)

1- Możesz tu włączyć/wyłączyć liczniki czasu oraz ustawić ich wartość.

2- Możesz tu zmienić rozdzielczość oraz włączyć/wyłączyć tryb pełnego ekranu.

# Wymagania kodu

W zakładce releases jest plik exe, który nie wymaga nawet aby python był zainstalowany na twoim komputerze, jednak musi on znajdować się w tym samym folderze co folder "images".
Kod został napisany w Pythonie 3.10. Używane są w nim następujące biblioteki:
- Pygame, interfejs użytkownika.

- Socket, do gry online.

- Threading, do multizadaniowości.

- Requests, aby określić IP zewnętrzne.

---
