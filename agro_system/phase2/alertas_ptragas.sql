--------------------------------------------------------
--  Arquivo criado - sexta-feira-novembro-21-2025   
--------------------------------------------------------
--------------------------------------------------------
--  DDL for Table ALERTAS_PRAGAS
--------------------------------------------------------

  CREATE TABLE "RM566269"."ALERTAS_PRAGAS" 
   (	"CULTURA" VARCHAR2(100 BYTE), 
	"TEMPERATURA" NUMBER(5,2), 
	"UMIDADE" NUMBER, 
	"RISCO" VARCHAR2(50 BYTE), 
	"RECOMENDACAO" VARCHAR2(100 BYTE), 
	"DATA_REGISTRO" DATE, 
	"CIDADE" VARCHAR2(100 BYTE)
   ) SEGMENT CREATION IMMEDIATE 
  PCTFREE 10 PCTUSED 40 INITRANS 1 MAXTRANS 255 
 NOCOMPRESS LOGGING
  STORAGE(INITIAL 65536 NEXT 1048576 MINEXTENTS 1 MAXEXTENTS 2147483645
  PCTINCREASE 0 FREELISTS 1 FREELIST GROUPS 1
  BUFFER_POOL DEFAULT FLASH_CACHE DEFAULT CELL_FLASH_CACHE DEFAULT)
  TABLESPACE "TBSPC_ALUNOS" ;
REM INSERTING into RM566269.ALERTAS_PRAGAS
SET DEFINE OFF;
Insert into RM566269.ALERTAS_PRAGAS (CULTURA,TEMPERATURA,UMIDADE,RISCO,RECOMENDACAO,DATA_REGISTRO,CIDADE) values ('abacaxi','29,03','67','baixo','Nenhuma ação é necessária no momento',to_date('10/11/25','DD/MM/RR'),'manicore');
Insert into RM566269.ALERTAS_PRAGAS (CULTURA,TEMPERATURA,UMIDADE,RISCO,RECOMENDACAO,DATA_REGISTRO,CIDADE) values ('feijão','19,22','83','baixo','Nenhuma ação é necessária no momento',to_date('10/11/25','DD/MM/RR'),'contagem');
Insert into RM566269.ALERTAS_PRAGAS (CULTURA,TEMPERATURA,UMIDADE,RISCO,RECOMENDACAO,DATA_REGISTRO,CIDADE) values ('batata','20,01','78','médio','Monitore diariamente e considere a aplicação de defensivos preventivos',to_date('10/11/25','DD/MM/RR'),'belo horizonte');
Insert into RM566269.ALERTAS_PRAGAS (CULTURA,TEMPERATURA,UMIDADE,RISCO,RECOMENDACAO,DATA_REGISTRO,CIDADE) values ('abacaxi','20,01','78','baixo','Nenhuma ação é necessária no momento',to_date('10/11/25','DD/MM/RR'),'belo horizonte');
Insert into RM566269.ALERTAS_PRAGAS (CULTURA,TEMPERATURA,UMIDADE,RISCO,RECOMENDACAO,DATA_REGISTRO,CIDADE) values ('abacaxi','20,01','78','baixo','Nenhuma ação é necessária no momento',to_date('10/11/25','DD/MM/RR'),'belo horizonte');
Insert into RM566269.ALERTAS_PRAGAS (CULTURA,TEMPERATURA,UMIDADE,RISCO,RECOMENDACAO,DATA_REGISTRO,CIDADE) values ('arroz','20,04','79','baixo','Nenhuma ação é necessária no momento',to_date('10/11/25','DD/MM/RR'),'betim');
