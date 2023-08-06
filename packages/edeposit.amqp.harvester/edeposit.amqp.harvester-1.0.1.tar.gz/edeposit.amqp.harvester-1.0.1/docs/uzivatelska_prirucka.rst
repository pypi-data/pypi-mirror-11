edeposit.amqp.harvester
=======================
Tento modul obsahuje funkce pro stahování metadat ze stránek několika vybraných vydavatelů. Momentálně jsou k dispozici programové komponenty pro webové prezentace nakladatelství `Ben <http://ben.cz>`_, `Grada <http://grada.cz>`_, `CPress <http://cpress.cz>`_ a `ZonerPress <http://zonerpress.cz>`_.

Instalace modulu
----------------
Modul je možné nainstalovat na prakticky každý linuxový systém pomocí programu `pip`_, který je součástí standardní distribuce `pythonu`::

    sudo pip install edeposit.amqp.harvester

.. _pip: https://pip.readthedocs.org/en/latest/

Použití modulu
--------------
Podobně jako ostatní prvky projektu Edeposit je i tento modul součástí asynchronního distribuovaného systému, jehož jednotlivé komponenty spolu komunikují přes AMQP protokol. O to se stará modul `edeposit.amqp <http://edeposit-amqp.readthedocs.org/>`_.

`edeposit.amqp.harvester` poskytuje pouze rozhraní umožňující `sklízení` metadat, nikoliv script, které získané informace předává dál. Ten je možné najít v modulu `edeposit.amqp <http://edeposit-amqp.readthedocs.org/>`_, kde se nachází pod názvem `edeposit_amqp_harvester.py <http://edeposit-amqp.readthedocs.org/en/latest/api/harvester.html>`_.

Spuštěním tohoto scriptu dochází k "sklizení" dat ze všech podporovaných komponent a jejich odeslání na AMQP fronty tak, jak je to definováno v souboru ``settingy.py`` modulu `edeposit.amqp`. Data jsou odesílána ve formátu struktury :class:`.Publications`, která ve svém těle nese pole struktur :class:`.Publication` se sklizenými metadaty.

Filtrace dat
++++++++++++
Modul umožňuje a v základu používá filtraci již zpracovaných záznamů. V tomto režimu jsou všechny stažené výsledky porovnávány vůči lokální databázi (viz soubor definovaný v :attr:`harvester.settings.DUP_FILTER_FILE`) a odesílány jsou pouze ty, které ještě nebyly zpracovány.

Toto chování je možné změnit nastavením konfigurační proměnné :attr:`harvester.settings.USE_DUP_FILTER` na hodnotu ``False``.

Dostupný je také filtr, který výsledky porovnává vůči Alephu a propouští pouze ty záznamy, které zatím Aleph neobsahuje.

Tento filtr je v základě vypnut aby se předešlo zbytečné zátěži Alephu. Zapnout toto chování je možné nastavením konfigurační proměnné :attr:`harvester.settings.USE_ALEPH_FILTER` na hodnotu ``True``.

Testovací script
----------------
Pro potřeby uživatelského testování byl v modulu `edeposit.amqp.harvester` vytvořen testovací script, který "sklidí" všechna data a zobrazí je na standardní výstup.

Script je možné najít ve složce ``bin/`` pod názvem ``edeposit_harvester_test.py``.

Zde je ukázka nápovědy::

    $ ./edeposit_harvester_test.py -h
    usage: edeposit_harvester_test.py [-h] [-u] [-r]

    This script is used to read data from edeposit.amqp.harvester and print it to
    stdout.

    optional arguments:
      -h, --help      show this help message and exit
      -u, --unittest  Perform unittest.
      -r, --harvest   Harvest all data and send them to harvester queue.

Jak je vidět z nápovědy, script přijímá dva parametry ``--unittest`` pro spuštění
testu jednotlivých komponent pro sklízení dat a ``--harvest``, jenž stáhne všechna dostupná data a vypíše je na standardní výstup.

Výsledek spuštění s parametrem ``--harvest`` je možné najít například zde:

- :download:`_static/out.txt`

Stejná data jsou normálně odeslána přes AMQP.

Testování modulu
----------------
Všechny komponenty, které má smysl automaticky testovat jsou testovány scriptem ``run_tests.sh``, který se nachází v kořenovém adresáři projektu.

Tento script je postavený nad programem py.test, jenž je možné nainstalovat příkazem::

    sudo pip install pytest

Zde je ukázka běhu všech 116 testů::

    $ ./run_tests.sh -u
    ============================= test session starts ==============================
    platform linux2 -- Python 2.7.5 -- py-1.4.20 -- pytest-2.5.2
    collected 116 items 

    src/edeposit/amqp/harvester/tests/unittests/test_aleph_filter_unit.py ..
    src/edeposit/amqp/harvester/tests/unittests/test_autoparser.py .........
    src/edeposit/amqp/harvester/tests/unittests/test_dup_filter.py ...
    src/edeposit/amqp/harvester/tests/unittests/test_settings.py .
    src/edeposit/amqp/harvester/tests/unittests/test_structures.py ....
    src/edeposit/amqp/harvester/tests/unittests/autoparser/test_auto_utils.py ....
    src/edeposit/amqp/harvester/tests/unittests/autoparser/test_conf_reader.py ...
    src/edeposit/amqp/harvester/tests/unittests/autoparser/test_path_patterns.py ............
    src/edeposit/amqp/harvester/tests/unittests/autoparser/test_vectors.py ...
    src/edeposit/amqp/harvester/tests/unittests/scrappers/test_ben_cz.py .......................................
    src/edeposit/amqp/harvester/tests/unittests/scrappers/test_cpress_cz.py ..................
    src/edeposit/amqp/harvester/tests/unittests/scrappers/test_grada_cz.py ..........
    src/edeposit/amqp/harvester/tests/unittests/scrappers/test_utils.py ........

    ========================== 116 passed in 2.65 seconds ==========================
