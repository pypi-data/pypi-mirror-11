.. vim: set fileencoding=utf-8 :
.. @author: Manuel Guenther <Manuel.Guenther@idiap.ch>
.. @date:   Tue Aug 26 09:42:18 CEST 2014

.. _bob.db.avspoof:

==========================================
 AVspoof Database Verification Protocols
==========================================

.. todolist::

=======================================================
 Speaker recognition protocol on the AVspof Database
=======================================================

`AVspoof_` is intended to provide stable, non-biased spoofing attacks in order for researchers to test both their ASV systems and anti-spoofing algorithms. The attacks are created based on newly acquired audio recordings. The data acquisition process lasted approximately two months with 44 persons, each participating in several sessions configured in different environmental conditions and setups. After the collection of the data, the attacks, more precisely, replay, voice conversion and speech synthesis attacks were generated. 


If you use this package and/or its results, please cite the following publication:

1. The original paper is presented at the IEEE BTAS 2015:

   .. code-block:: latex

    @inproceedings{avspoof,
      author = {Serife Kucur Erg\"unay and Elie Khoury and Alexandros Lazaridis and S\'ebastien Marcel },
      title = {On the Vulnerability of Speaker Verification to Realistic Voice Spoofing},
      booktitle = {IEEE Intl. Conf. on Biometrics: Theory, Applications and Systems (BTAS)},
      year = {2015},
      url = {https://publidiap.idiap.ch/downloads//papers/2015/KucurErgunay_IEEEBTAS_2015.pdf},
    }

Getting the data
--------------------------

The original data can be downloaded directly from AVspoof_, which is free of charge but requires to sign the EULA. 


Documentation
------------------------

.. toctree::
   :maxdepth: 2

   guide
   py_api

Indices and tables
-------------------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _bob: https://www.idiap.ch/software/bob
.. _AVspoof: https://www.idiap.ch/dataset/avspoof
.. _nist sre 2012 evaluation: http://www.nist.gov/itl/iad/mig/sre12.cfm
.. _idiap: http://www.idiap.ch


