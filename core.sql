SQLite format 3   @                                                                     -�   �    ��                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
	   	   � �                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      %ef137f148877
   � �                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      %	ef137f148877   � ����                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             5DJIAIndustrial Dow Jones NASDAQNASDAQ100 SPXS&P500 IBEX35IBEX35
   � ����                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          DJIA
NASDAQSPX		IBEX35   � ���                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       NYSENYSE NASDAQNASDAQ
 BMEBME
   � ���                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       NYSE
NASDAQ	BME                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              � 8 �w$�8�                                                                                                                                                                                                                                                                                                  S)sindexix_market_codemarketCREATE UNIQUE INDEX ix_market_code ON market (code)��tablemarketmarketCREATE TABLE market (
	id INTEGER NOT NULL, 
	code VARCHAR(30) NOT NULL, 
	name VARCHAR(100) NOT NULL, 
	PRIMARY KEY (id)
)Q'sindexix_index_codeindexCREATE UNIQUE INDEX ix_index_code ON "index" (code)��tableindexindexCREATE TABLE "index" (
	id INTEGER NOT NULL, 
	code VARCHAR(30) NOT NULL, 
	name VARCHAR(100) NOT NULL, 
	PRIMARY KEY (id)
)�)++�	tablealembic_versionalembic_versionCREATE TABLE alembic_version (
	version_num VARCHAR(32) NOT NULL, 
	CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
)=Q+ indexsqlite_autoindex_alembic_version_1alembic_version       �  � D� � Y Q Q                                                                                                                                                      �%	�)tablestockstockCREATE TABLE stock (
	id INTEGER NOT NULL, 
	code VARCHAR(30) NOT NULL, 
	name VARCHAR(100) NOT NULL, 
	market_id INTEGER NOT NULL, 
	index_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(index_id) REFERENCES "index" (id), 
	FOREIGN KEY(market_id) REFERENCES market (id)
)p/%�indexindex_date_uniqueindex_pricesCREATE UNIQUE INDEX index_date_unique ON index_prices (date, index_id)�d%%�tableindex_pricesindex_pricesCREATE TABLE index_prices (
	id INTEGER NOT NULL, 
	import_date DATETIME NOT NULL, 
	date DATE NOT NULL, 
	index_id INTEGER NOT NULL, 
	open_price FLOAT NOT NULL, 
	high_price FLOAT NOT NULL, 
	low_price FLOAT NOT NULL, 
	close_price FLOAT NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(index_id) REFERENCES "index" (id)
)   U                                                                                 
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 �    �                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                *
   Ct V�����M��|���o�ymb��W�AL�h6+�_ 
��2��������t�)�;�D� ���������z�                                                                                                                                                                                                                                      MMMCBACBCVXAC@WMT?DAL>F=JNJ<GM;MA:DIS9KO8ORCL7MCD6V5IBM4NKE3JPM2BABA1TWTR0TSLA/CSCO.PYPL-MSFT,INTC+NFLX*NVDA)AMZN(AAPL'GOOG&FB%
BME.MC$
VIS.MC#
TEF.MC"
TRE.MC!SGRE.MC 
SAN.MC
REP.MC
REE.MC
MRL.MC
MEL.MC
TL5.MC
MAP.MC
IDR.MC
ITX.MC
IBE.MC
IAG.MC
GRF.MC
GAS.MC
FER.MC
ELE.MC
ENG.MC
DIA.MC
COL.MCCLNX.MCCABK.MCBBVA.MC
BKT.MC
BKIA.MC	
SAB.MC
MTS.MC
AMS.MCAENA.MC
ACS.MC
ACX.MC
ANA.MC		ABE.MC                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 � ���                                                                                                                                                                                                                                                                                                                                                                                    l/!�indexstock_date_uniquestock_dataCREATE UNIQUE INDEX stock_date_unique ON stock_data (date, stock_id)�<!!�Ctablestock_datastock_dataCREATE TABLE stock_data (
	id INTEGER NOT NULL, 
	import_date DATETIME NOT NULL, 
	date DATE NOT NULL, 
	stock_id INTEGER NOT NULL, 
	price FLOAT NOT NULL, 
	expected_price FLOAT NOT NULL, 
	max_52 FLOAT NOT NULL, 
	per FLOAT NOT NULL, 
	growth_next_year FLOAT NOT NULL, 
	growth_next_five_year FLOAT NOT NULL, 
	dividend_yield FLOAT NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(stock_id) REFERENCES stock (id)
)O
'oindexix_stock_codestockCREATE UNIQUE INDEX ix_stock_code ON stock (code)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 * _ �����~cG2������lS>-�����vbK. � � � � � � � s _   *  NFLXNETFLIX)  NVDANVIDIA(  AMZNAMAZON'  AAPLAPPLE&  GOOGGOOGLE%  FBFACEBOOK$ 	 BME.MCBME# 		VIS.MCVISCOFA" !		TEF.MCTELEFONICA! /		TRE.MCTECNICAS_REUNIDAS  )		SGRE.MCSIEMENS_GAMESA 		SAN.MCSANTANDER 		REP.MCREPSOL '		REE.MCRED_ELECTRICA #		MRL.MCMERLIN_PROP %		MEL.MCMELIA_HOTELS 		TL5.MCMEDIASET 		MAP.MCMAPFRE 		IDR.MCINDRA 		ITX.MCINDITEX 		IBE.MCIBERDROLA 		IAG.MCIAG 		GRF.MCGRIFOLS #		GAS.MCGAS_NATURAL 		FER.MCFERROVIAL 		ELE.MCENDESA 		ENG.MCENAGAS 		DIA.MCDIA 		COL.MCCOLONIAL +		CLNX.MCCELLNEX_TELECOM 		CABK.MCCAIXABANK 		BBVA.MCBBVA
 		BKT.MCBANKINTER	 		BKIA.MCBANKIA )		SAB.MCBANCO_SABADELL '		MTS.MCARCELORMITTAL -		AMS.MCAMADEUS_IT_GROUP 		AENA.MCAENA 		ACS.MCACS 		ACX.MCACERINOX 		ANA.MCACCIONA 		ABE.MCABERTIS    ������ydTE7"������taM:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       C  MMM3MB + BACBANK_OF_AMERICAA  CVXCHEVRON@ ! CCITI_GROUP?  WMTWALMART> ) DALDELTA_AIRLINES=  FFORD< + JNJJOHNSON_JOHNSON; ) GMGENERAL_MOTORS:  MAMATERCARD9 # DISWALT_DISNEY8  KOCOCA_COLA7  ORCLORACLE6  MCDMCDONALDS5  VVISA4  IBMIBM3  NKENIKE2  JPMJP_MORGAN1  BABAALIBABA0  TWTRTWITTER/  TSLATESLA.  CSCOCISCO-  PYPLPAYPAL,  MSFTMICROSOFT+  INTCINTEL