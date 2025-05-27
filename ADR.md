Dzień dobry,

Chcielibyśmy dziś zaprezentować nasz wspólny projekt gry komputerowej, który stworzyliśmy w języku Python z wykorzystaniem biblioteki Pygame. Do pracy nad projektem użyliśmy edytora Visual Studio Code oraz systemu kontroli wersji Git.

Chcielibyśmy na chwilę zatrzymać się przy Gicie, ponieważ nie wszyscy mogą znać to narzędzie. Git to bardzo popularny system kontroli wersji, który wykorzystaliśmy w naszym projekcie. Jego główną zaletą jest możliwość śledzenia wszystkich zmian wprowadzanych w kodzie – każdą modyfikację, nawet najmniejszą, zapisywaliśmy w repozytorium. Dzięki temu mogliśmy w każdej chwili wrócić do wcześniejszych wersji projektu, gdy coś przestawało działać.

Wspólnie pracowaliśmy nad różnymi funkcjonalnościami w osobnych gałęziach (branchach), co dało nam dużą swobodę eksperymentowania bez ryzyka uszkodzenia głównej wersji gry. W trakcie pracy łączyliśmy nasze zmiany i rozwiązywaliśmy ewentualne konflikty w kodzie.

Dodatkowo, korzystaliśmy z platformy GitHub, dzięki której przechowywaliśmy kopię zapasową projektu w chmurze i mogliśmy łatwo dzielić się naszym kodem.

Nasz wspólny projekt to gra typu top-down shooter, w której razem opracowaliśmy system przemierzania kolejnych pokoi, walki z przeciwnikami, unikania pułapek i zbierania przedmiotów. Wspólnie stworzyliśmy różne rodzaje broni, mechanikę rzucania granatów oraz interaktywne elementy otoczenia, takie jak niszczalne ściany czy kolce. Naszym wspólnym celem było stworzenie gry, gdzie gracz musi pokonać wszystkich wrogów oraz bossa na końcu poziomu.


Gra wita nas takim oto ekranem tytułowym z menu głównym. W głównym menu widać przyciski, które zmieniają swój kolor i rozmiar, gdy są aktywne. Zwróćcie też uwagę na unoszące się cząsteczki w dolnej części ekranu – ten element dodaje dynamiki naszemu ekranowi głównemu.

Za chwilę opowiemy, jak zostały stworzone te elementy. Zacznijmy od interaktywnych przycisków, które płynnie zmieniają swoją szerokość. Osiągnęliśmy to w następujący sposób: w każdej klatce animacji do początkowej szerokości dodawany jest współczynnik zależny od szerokości ekranu. Równomierne rozłożenie zmian na poszczególne klatki pozwoliło nam stworzyć efektowny interfejs użytkownika (UI) bez większego wysiłku.

Jeśli chodzi o zmianę aktywności przycisków – reagują one na naciśnięcie klawiszy strzałek. Miłym dodatkiem do designu jest również migająca strzałka wskazująca aktualnie wybraną opcję.


Na samej zaszczce widzimy postać specjalisty – czyli naszego głównego bohatera.


Przechodzimy do ustawień. W menu opcji widzimy minimalistyczny interfejs z kilkoma przyciskami. W sekcji trudności mamy do wyboru kilka poziomów: łatwy, średni i trudny.


Dalej znajduje się przycisk odpowiadający za rozdzielczość gry – to jeden z najbardziej problematycznych elementów, który powodował liczne błędy podczas rozwoju projektu. System rozdzielczości dynamicznie dostosowuje się do różnych rozmiarów ekranów, zapewniając optymalne wrażenia wizualne.

Teraz przejdźmy do sedna rozgrywki. Nasza gra w wielu aspektach nawiązuje do takich tytułów jak Soul Knight czy The Binding of Isaac, które zdobyły serca graczy na całym świecie. Mechanika polega na eksploracji kolejnych pomieszczeń i eliminowaniu napotkanych przeciwników.

Gracz ma do dyspozycji cztery różnorodne typy broni. Podstawę stanowi pistolet, który choć cechuje się stosunkowo niską szybkostrzelnością i obrażeniami, pozostaje najbardziej uniwersalną opcją. Dla tych, którzy preferują bardziej zrównoważone podejście, przygotowaliśmy karabin. Prawdziwi miłośnicy precyzyjnego strzelania docenią natomiast karabin snajperski. W sytuacjach kryzysowych warto sięgnąć po granaty, pozwalające na likwidację całych grup wrogów jednocześnie.

Każdy rodzaj broni posiada unikalny system strzelania i indywidualny zapas amunicji. Co ważne, pokonani przeciwnicy mogą zostawiać po sobie amunicję - każda znaleziona paczka uzupełnia o jeden magazynek wszystkie posiadane przez gracza rodzaje broni.

Kluczowym elementem rozgrywki jest system walki w zamkniętych pomieszczeniach. W momencie wejścia do pokoju drzwi automatycznie się zamykają, uniemożliwiając odwrót do momentu wyeliminowania wszystkich przeciwników. Gracz musi uważnie monitorować pasek zdrowia swojego bohatera - jego całkowite opróżnienie oznacza natychmiastową porażkę i konieczność rozpoczęcia poziomu od nowa.

