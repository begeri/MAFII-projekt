# MAFII-projekt
A 2021/22es tanév őszi félévében MAF2 tárgy nagybeadandója. 

A projekt célja egy algoritmus létrehozása, amely képes értelmes döntéseket hozni, ha van elég gondolkodási ideje. Ezt egy Monte Carlo Tree Search eljárásra alapozva csináljuk.

Az algoritmus egy adott játékállásból felépít egy fát, ami a lehetséges játékfolytatásokat reprezentálja. Minden ciklusban hozzávesz egy új lépést a fához, és valamilyen egyszerű függvény alapján értékeli.
Az UCB (Upper Confidence Bound) gondoskodik az ígéretes játékállások boncolgatása és a felfedezetlen ágak felderítése közötti egyensúlyról. Ez a módszer segít abban, hogy az ígéretesnek tűnő lépéseket jobban megvizsgáljuk, mint amiket alapból sem tűnnek hasznosnak.

