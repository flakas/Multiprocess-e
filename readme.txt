Dviejų e formulių palyginimas ir ilgiausios sekos paieška
=========================================================

Programa veikia 2 etapais:
- Paskaičiuojamas dviejų e formulių palyginimas pagal vartotojo pateiktus skaičius
- Naudojant visus sistemos branduolius (arba tiek, kiek nurodo vartotojas)
  kuo tiksliau paskaičiuojamas e ir ieškoma ilgiausių kuo dažniau pasikartojančių
  posekių.


Programos paleidimas
--------------------

Paleidimo pavyzdys:
python main.py 50 50 50000 14000 8

- `python main.py` programos paleidimas
- Parametrai:
  * `50` - kiek skaičių po kablelio naudoti formulių palyginime
  * `50` - n. T.y. kiek iteracijų daryti palyginimui
  * `50000` - kiek skaičių po kablelio naudoti e skaičiavimui (antroji dalis)
  * `14000` - kiek iteracijų daryti e skaičiavimui (antroji dalis)
  * `8` - Turimų (ar norimų naudoti skaičiavimui) branduolių skaičius
